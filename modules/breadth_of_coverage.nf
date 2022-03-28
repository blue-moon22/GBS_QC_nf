process breadth_of_coverage {

    input:
    path qc_stats
    path headers
    path lanes_file

    output:
    path "${output_file}"

    script:
    python_version = params.python_version
    cov_breadth_threshold = params.cov_breadth_threshold
    output_file = "breadth_of_coverage.tab"

    """
    module load ISG/python/${python_version}

    get_coverage_breadth.py \
        --lane_ids ${lanes_file} \
        --qc_stats ${qc_stats} \
        --threshold ${cov_breadth_threshold} \
        --headers ${headers} \
        --output_file ${output_file}
    """
}
