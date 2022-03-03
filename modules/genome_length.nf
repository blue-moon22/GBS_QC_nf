process genome_length {

    input:
    path file_dest
    path headers
    path lanes_file

    output:
    path "${output_file}"

    script:
    python_version = params.python_version
    genome_len_lower_threshold = params.genome_len_lower_threshold
    genome_len_higher_threshold = params.genome_len_higher_threshold
    assembler = params.assembler
    output_file = "genome_length.tab"

    """
    module load ISG/python/${python_version}

    get_genome_length.py \
        --lane_ids ${lanes_file} \
        --file_dest ${file_dest} \
        --lower_threshold ${genome_len_lower_threshold} \
        --higher_threshold ${genome_len_higher_threshold} \
        --assembler ${assembler} \
        --headers ${headers} \
        --output_file ${output_file}
    """
}
