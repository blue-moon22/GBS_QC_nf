#!/usr/bin/env python3
import argparse
import sys
import re
import pandas as pd

from lib.get_headers import read_header_json
from lib.get_items import get_items

def count_contigs(contig_fasta):

    contig_no = None
    try:
        with open(contig_fasta, "r") as file:
            contig_no = 0
            for line in file:
                if line[0] == '>':
                    contig_no += 1

    except:
        print(f'${contig_fasta} does not exist.')

    return contig_no


def get_contig_number(file_dest, lane_ids, assembler):

    lane_ids_contig_no = []
    for lane_id in lane_ids:
        contig_fasta = [f'{dest}/{assembler}_assembly/contigs.fa' for dest in file_dest if f'/{lane_id}/' in f'{dest}/{assembler}_assembly/contigs.fa']
        if contig_fasta:
            contig_no = count_contigs(contig_fasta[0])
        else:
            contig_no = None

        lane_ids_contig_no.append((lane_id, contig_no))

    return lane_ids_contig_no


def write_qc_status(lane_ids_contig_no, threshold, headers, output_file):

    headers.insert(0, 'lane_id')
    df = pd.DataFrame(columns=headers, index = [0])

    for ind, lane_id_contig_no in enumerate(lane_ids_contig_no):
        contig_no = lane_id_contig_no[1]
        df.loc[ind, headers[0]] = lane_id_contig_no[0]
        df.loc[ind, headers[1]] = contig_no

        if contig_no is not None:
            if contig_no < threshold:
                df.loc[ind, headers[2]] = "PASS"
            else:
                df.loc[ind, headers[2]] = "FAIL"

    df.to_csv(output_file, sep = '\t', index = False)


def get_arguments():
    parser = argparse.ArgumentParser(description="Get number of contigs from contigs FASTA.")
    parser.add_argument("-l", "--lane_ids", required=True, type=str,
                        help="Text file of lane ids.")
    parser.add_argument("-d", "--file_dest", required=True, type=str,
                        help="Desinations for kraken report files.")
    parser.add_argument("-a", "--assembler", required=True, type=str,
                        help="Assembler, e.g. velvet or spades")
    parser.add_argument("-t", "--threshold", required=True, type=int,
                        help="QC PASS/FAIL threshold for number of contigs i.e. if number of contigs is LESS THAN threshold, then PASS, otherwise FAIL.")
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

    # Get relative abundance from kraken report
    lane_ids_contig_no = get_contig_number(file_dest, lane_ids, args.assembler)

    # Write lane id, relative abundance and PASS/FAIL status in tab file
    write_qc_status(lane_ids_contig_no, args.threshold, header_dict["contig_number"], args.output_file)


if __name__ == '__main__':
    parser = get_arguments()
    args = parser.parse_args()
    sys.exit(main(args))
