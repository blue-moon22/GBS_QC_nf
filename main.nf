/*
 * Nextflow pipeline for QCing Group B Strep
 *
 */

// Enable DSL 2
nextflow.enable.dsl=2

// Import modules
include {get_file_destinations} from './modules/get_file_destinations.nf'
include {relative_abundance} from './modules/relative_abundance.nf'
include {number_of_contigs} from './modules/number_of_contigs.nf'
include {collate_qc_data} from './modules/collate_qc_data.nf'
include {contig_gc_content} from './modules/contig_gc_content.nf'

// Workflow for reads QC
workflow reads_qc {
    take:
    file_dest_ch
    headers_ch
    lanes_ch

    main:
    relative_abundance(file_dest_ch, headers_ch, lanes_ch)
    qc_report = relative_abundance.out

    emit:
    qc_report
}

// Workflow for assemblies QC
workflow assemblies_qc {
    take:
    file_dest_ch
    headers_ch
    lanes_ch

    main:
    number_of_contigs(file_dest_ch, headers_ch, lanes_ch)
    contig_gc_content(file_dest_ch, headers_ch, lanes_ch)

    number_of_contigs.out
    .combine(contig_gc_content.out)
    .set { qc_report }

    emit:
    qc_report
}

// Main Workflow
workflow {

    main:
    // Reads QC
    // Create read pairs channel
    if (params.lanes) {
        lanes_ch = Channel.fromPath( params.lanes, checkIfExists: true )
        get_file_destinations(lanes_ch)

    } else {
        println("Error: You must specify a text file of lanes as --lanes <file with list of lanes>")
        System.exit(1)
    }

    headers_ch = Channel.fromPath( params.headers, checkIfExists: true )
    // Run reads QC
    reads_qc(get_file_destinations.out, headers_ch, lanes_ch)

    // Run assembly QC
    assemblies_qc(get_file_destinations.out, headers_ch, lanes_ch)

    // Collate QC reports
    collate_qc_data(reads_qc.out.qc_report, assemblies_qc.out.qc_report)

    results_dir = file(params.qc_reports_directory)
    results_dir.mkdir()

    collate_qc_data.out.complete
    .subscribe { it -> it.copyTo(results_dir) }

    collate_qc_data.out.summary
    .subscribe { it -> it.copyTo(results_dir) }
}
