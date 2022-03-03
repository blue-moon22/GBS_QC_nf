process collate_qc_data {

    input:
    path read_qc_report
    tuple file(number_of_contigs), file(contig_gc_content), file(genome_length)

    output:
    path("qc_report_complete.tab"), emit: complete
    path("qc_report_summary.tab"), emit: summary

    script:
    python_version = params.python_version

    """
    module load ISG/python/${python_version}

    collate_qc_data.py \
        --qc_reports ${read_qc_report} ${number_of_contigs} ${contig_gc_content} ${genome_length} \
        --output_prefix "qc_report"
    """
}
