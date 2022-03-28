process percentage_HET_SNPs {

    input:
    path qc_stats
    path headers
    path lanes_file

    output:
    path "${output_file}"

    script:
    python_version = params.python_version
    percentage_het_snps_threshold = params.percentage_het_snps_threshold
    output_file = "percentage_het_snps.tab"

    """
    module load ISG/python/${python_version}

    get_percentage_het_snps.py \
        --lane_ids ${lanes_file} \
        --qc_stats ${qc_stats} \
        --threshold ${percentage_het_snps_threshold} \
        --headers ${headers} \
        --output_file ${output_file}
    """
}
