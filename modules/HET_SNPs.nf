process HET_SNPs {

    input:
    path het_stats
    path headers
    path lanes_file

    output:
    path "${output_file}"

    script:
    python_version = params.python_version
    het_snps_threshold = params.het_snps_threshold
    output_file = "het_snps.tab"

    """
    tar -tvf ${het_stats}

    module load ISG/python/${python_version}

    get_het_snps.py \
        --lane_ids ${lanes_file} \
        --data_dir \$(pwd) \
        --threshold ${het_snps_threshold} \
        --headers ${headers} \
        --output_file ${output_file}
    """
}
