process relative_abundance {

    input:
    path file_dest
    path headers
    path lanes_file

    output:
    path "${output_file}"

    script:
    python_version = params.python_version
    rel_abund_threshold = params.rel_abund_threshold
    species = params.species
    output_file = "relative_abundance.tab"

    """
    module load ISG/python/${python_version}

    get_relative_abundance.py \
        --lane_ids ${lanes_file} \
        --file_dest ${file_dest} \
        --threshold ${rel_abund_threshold} \
        --species ${species} \
        --headers ${headers} \
        --output_file ${output_file}
    """
}
