process get_proportion_HET_SNPs {

    input:
    path lanes_file

    output:
    path "${output_file}"

    script:
    pf_version=params.pf_version
    output_file="all_stats.tar"
    """
    #!/bin/bash

    module load pf/${pf_version}
    pf snp -t file -i ${lanes_file} | grep .gz\$ > vcf_files.txt

    num=\$(cat ${lanes_file} | wc -l)

    for ((i=1;i<=\${num};i++))
    do
        lane=\$(sed -n "\${i}p" ${lanes_file})
        vcf_file=\$(grep "/\${lane}/" vcf_files.txt | sort -r | head -n 1)
        if [ \${vcf_file} ]
        then
            gunzip -c \${vcf_file} > tmp.vcf
            filtervcf_v4.py tmp.vcf \${lane} 50
            rm *.vcf
        fi
    done
    tar -cf ${output_file} *stats
    touch ${output_file}
    """
}
