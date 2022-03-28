process depth_of_coverage {

    input:
    path qc_stats
    path headers
    path lanes_file

    output:
    path "${output_file}"

    script:
    python_version = params.python_version
    cov_depth_threshold = params.cov_depth_threshold
    output_file = "depth_of_coverage.tab"

    """
    module load ISG/python/${python_version}

    get_coverage_depth.py \
        --lane_ids ${lanes_file} \
        --qc_stats ${qc_stats} \
        --threshold ${cov_depth_threshold} \
        --headers ${headers} \
        --output_file ${output_file}
    """
}
