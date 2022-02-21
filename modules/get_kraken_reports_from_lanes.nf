process get_kraken_reports_from_lanes {

    input:
    path lanes_file

    output:
    path "${output_file}"

    script:
    pf_version=params.pf_version
    output_file="list_of_lanes_and_kraken_reports.txt"
    empty_kraken_report="empty_kraken.report"

    """
    #!/bin/bash
    
    module load pf/${pf_version}
    pf data -t file -i ${lanes_file} > file_dest.txt
    touch ${empty_kraken_report}
    num_lanes=\$(cat ${lanes_file} | wc -l)

    for ((i=1;i<=\${num_lanes};i++));
    do
        lane=\$(sed -n "\${i}p" ${lanes_file})
        file=\$(grep "\$lane\$" file_dest.txt)/kraken.report
        if [ -f "\${file}" ];
        then
            echo "\${lane}\t\${file}" >> tmp.txt
        else
            echo "\${lane}\t\${PWD}/${empty_kraken_report}" >> tmp.txt
        fi
    done
    mv tmp.txt ${output_file}
    """
}
