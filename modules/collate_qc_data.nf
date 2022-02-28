process collate_qc_data {

    input:
    path read_qc_report
    path assembly_qc_report

    output:
    path("qc_report_complete.tab"), emit: complete
    path("qc_report_summary.tab"), emit: summary

    script:
    python_version = params.python_version

    """
    module load ISG/python/${python_version}

    collate_qc_data.py \
        --qc_reports ${read_qc_report} ${assembly_qc_report} \
        --output_prefix "qc_report"
    """
}
