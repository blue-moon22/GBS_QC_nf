process number_of_contigs {

    input:
    path file_dest
    path headers
    path lanes_file

    output:
    path "${output_file}"

    script:
    python_version = params.python_version
    contig_no_threshold = params.contig_no_threshold
    assembler = params.assembler
    output_file = "number_of_contigs.tab"

    """
    module load ISG/python/${python_version}

    get_no_contigs.py \
        --lane_ids ${lanes_file} \
        --file_dest ${file_dest} \
        --threshold ${contig_no_threshold} \
        --assembler ${assembler} \
        --headers ${headers} \
        --output_file ${output_file}
    """
}
