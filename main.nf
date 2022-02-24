/*
 * Nextflow pipeline for QCing Group B Strep
 *
 */

// Enable DSL 2
nextflow.enable.dsl=2

// Import modules
include {relative_abundance} from './modules/relative_abundance.nf'
include {get_file_destinations} from './modules/get_file_destinations.nf'

// Workflow for reads QC
workflow reads_qc {
    take:
    file_dest_ch
    headers_ch
    lanes_ch

    main:        
    relative_abundance(file_dest_ch, headers_ch, lanes_ch)

    emit:
    relative_abundance.out
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

    // Run reads QC
    headers_ch = Channel.fromPath( params.headers, checkIfExists: true )
    reads_qc(get_file_destinations.out, headers_ch, lanes_ch)

    // Collate QC reports
    reads_qc.out
    .collectFile(name: file("${params.qc_report}"), keepHeader: true, sort: true)
}
