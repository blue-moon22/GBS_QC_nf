process contig_gc_content {

    input:
    path file_dest
    path headers
    path lanes_file

    output:
    path "${output_file}"

    script:
    python_version = params.python_version
    gc_content_lower_threshold = params.gc_content_lower_threshold
    gc_content_higher_threshold = params.gc_content_higher_threshold
    assembler = params.assembler
    output_file = "contig_gc_content.tab"

    """
    module load ISG/python/${python_version}

    get_gc_content.py \
        --lane_ids ${lanes_file} \
        --file_dest ${file_dest} \
        --lower_threshold ${gc_content_lower_threshold} \
        --higher_threshold ${gc_content_higher_threshold} \
        --assembler ${assembler} \
        --headers ${headers} \
        --output_file ${output_file}
    """
}
