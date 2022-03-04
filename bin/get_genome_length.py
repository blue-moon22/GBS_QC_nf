#!/usr/bin/env python3
import argparse
import sys
import re
import pandas as pd

from lib.get_headers import read_header_json
from lib.get_items import get_items

def count_nucl(contig_fasta):

    nucl_no = None
    try:
        with open(contig_fasta, "r") as file:
            nucl_no = 0
            for line in file:
                if line[0] != '>':
                    nucl_no += len(line.split('\n')[0])

    except:
        print(f'${contig_fasta} does not exist.')

    return nucl_no


def get_genome_length(file_dest, lane_ids, assembler):

    lane_ids_nucl_no = []
    for lane_id in lane_ids:
        contig_fasta = [f'{dest}/{assembler}_assembly/contigs.fa' for dest in file_dest if f'/{lane_id}/' in f'{dest}/{assembler}_assembly/contigs.fa']
        if contig_fasta:
            nucl_no_value = count_nucl(contig_fasta[0])
        else:
            nucl_no_value = None

        lane_ids_nucl_no.append((lane_id, nucl_no_value))

    return lane_ids_nucl_no


def write_qc_status(lane_ids_nucl_no, lower_threshold, higher_threshold, headers, output_file):

    headers.insert(0, 'lane_id')
    df = pd.DataFrame(columns=headers, index = [0])

    for ind, lane_id_nucl_no in enumerate(lane_ids_nucl_no):
        nucl_no = lane_id_nucl_no[1]
        df.loc[ind, headers[0]] = lane_id_nucl_no[0]
        df.loc[ind, headers[1]] = nucl_no

        if nucl_no is not None:
            if nucl_no > lower_threshold and nucl_no < higher_threshold:
                df.loc[ind, headers[2]] = "PASS"
            else:
                df.loc[ind, headers[2]] = "FAIL"

    df.to_csv(output_file, sep = '\t', index = False)


def get_arguments():
    parser = argparse.ArgumentParser(description="Get length of genome from contigs FASTA.")
    parser.add_argument("-l", "--lane_ids", required=True, type=str,
                        help="Text file of lane ids.")
    parser.add_argument("-d", "--file_dest", required=True, type=str,
                        help="Desinations for kraken report files.")
    parser.add_argument("-a", "--assembler", required=True, type=str,
                        help="Assembler, e.g. velvet or spades")
    parser.add_argument("-lt", "--lower_threshold", required=True, type=int,
                        help="QC PASS/FAIL lower threshold for genome length i.e. the genome length must be GREATER THAN lower threshold to PASS.")
    parser.add_argument("-ht", "--higher_threshold", required=True, type=int,
                        help="QC PASS/FAIL higher threshold for genome length i.e. the genome length must be LESS THAN higher threshold to PASS.")
    parser.add_argument("-j", "--headers", required=True, type=str,
                        help="JSON of headers for QC report.")
    parser.add_argument("-o", "--output_file", required=True, type=str,
                        help="Output tab file.")

    return parser


def main(args):
    # Get lane ids
    lane_ids = get_items(args.lane_ids)

    # Get file destinations
    file_dest = get_items(args.file_dest)

    # Get column headers from headers json
    header_dict = read_header_json(args.headers)

    # Get genome length from contigs
    lane_ids_nucl_no = get_genome_length(file_dest, lane_ids, args.assembler)

    # Write lane id, genome length and PASS/FAIL status in tab file
    write_qc_status(lane_ids_nucl_no, args.lower_threshold, args.higher_threshold, header_dict["genome_length"], args.output_file)


if __name__ == '__main__':
    parser = get_arguments()
    args = parser.parse_args()
    sys.exit(main(args))