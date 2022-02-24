process get_file_destinations {

    input:
    path lanes_file

    output:
    path "${output_file}"

    script:
    pf_version=params.pf_version
    output_file="file_dest.txt"

    """
    #!/bin/bash
    
    module load pf/${pf_version}
    pf data -t file -i ${lanes_file} > ${output_file}
    """
}
