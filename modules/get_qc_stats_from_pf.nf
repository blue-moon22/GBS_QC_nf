process get_qc_stats_from_pf {

    input:
    path lanes_file

    output:
    path "${output_file}"

    script:
    pf_version=params.pf_version
    output_file="${lanes_file}.pathfind_stats.csv"

    """
    #!/bin/bash

    module load pf/${pf_version}
    pf data -s -t file -i ${lanes_file}
    """
}
