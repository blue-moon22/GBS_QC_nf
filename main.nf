/*
 * Nextflow pipeline for QCing Group B Strep
 *
 */

// Enable DSL 2
nextflow.enable.dsl=2

// Import modules
include {relative_abundance} from './modules/relative_abundance.nf'
include {get_kraken_reports_from_lanes} from './modules/get_kraken_reports_from_lanes.nf'

// Workflow for reads QC
workflow reads_qc {
    take:
    kraken_reports_ch
    headers_ch

    main:
    kraken_reports_ch
    .splitCsv(header:false, sep:"\t")
    .map { row -> tuple(row[0], file(row[1])) }
    .combine(headers_ch)
    .set { lane_kraken_report_ch }
        
    relative_abundance(lane_kraken_report_ch)

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
        get_kraken_reports_from_lanes(lanes_ch)

    } else {
        println("Error: You must specify a text file of lanes as --lanes <file with list of lanes>")
        System.exit(1)
    }

    // Run reads QC
    headers_ch = Channel.fromPath( params.headers, checkIfExists: true )
    reads_qc(get_kraken_reports_from_lanes.out, headers_ch)

    // Collate QC reports
    reads_qc.out
    .collectFile(name: file("${params.qc_report}"), keepHeader: true, sort: true)
}
