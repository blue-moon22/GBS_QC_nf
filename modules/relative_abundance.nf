process relative_abundance {

    input:
    tuple val(lane_id), file(kraken_report), file(headers)

    output:
    path "${output_file}"

    script:
    python_version = params.python_version
    rel_abund_threshold = params.rel_abund_threshold
    species = params.species
    output_file = "${lane_id}_relative_abundance.tab"

    """
    module load ISG/python/${python_version}

    get_relative_abundance.py \
        --lane_id ${lane_id} \
        --kraken_report ${kraken_report} \
        --threshold ${rel_abund_threshold} \
        --species ${species} \
        --headers ${headers} \
        --output_file ${output_file}
    """
}
