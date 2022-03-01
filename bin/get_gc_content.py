#!/usr/bin/env python3
import argparse
import sys
import re
import pandas as pd

from lib.get_headers import read_header_json
from lib.get_items import get_items

def gc_content(contig_fasta):

    acount = 0
    ccount = 0
    gcount = 0
    tcount = 0

    gc_content_value = None
    try:
        with open(contig_fasta, "r") as file:
            for line in file:
                if line[0] != '>':
                    acount += len(re.findall("A",line))
                    ccount += len(re.findall("C",line))
                    gcount += len(re.findall("G",line))
                    tcount += len(re.findall("T",line))

        gc_content_value = round((acount + gcount)*100 / float(acount + ccount + gcount + tcount), 1)

    except:
        print(f'${contig_fasta} does not exist.')

    return gc_content_value


def get_gc_content(file_dest, lane_ids, assembler):

    lane_ids_gc_content = []
    for lane_id in lane_ids:
        contig_fasta = [f'{dest}/{assembler}_assembly/contigs.fa' for dest in file_dest if f'/{lane_id}/' in f'{dest}/{assembler}_assembly/contigs.fa']
        if contig_fasta:
            gc_content_value = gc_content(contig_fasta[0])
        else:
            gc_content_value = None

        lane_ids_gc_content.append((lane_id, gc_content_value))

    return lane_ids_gc_content


def write_qc_status(lane_ids_gc_content, lower_threshold, higher_threshold, headers, output_file):

    headers.insert(0, 'lane_id')
    df = pd.DataFrame(columns=headers, index = [0])

    for ind, lane_id_gc_content in enumerate(lane_ids_gc_content):
        contig_no = lane_id_gc_content[1]
        df.loc[ind, headers[0]] = lane_id_gc_content[0]
        df.loc[ind, headers[1]] = contig_no

        if contig_no is not None:
            if contig_no >= lower_threshold and contig_no <= higher_threshold:
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
    parser.add_argument("-lt", "--lower_threshold", required=True, type=int,
                        help="QC PASS/FAIL lower threshold for gc content i.e. if number of contigs is GREAT THAN OR EQUAL to lower threshold, then PASS, otherwise FAIL.")
    parser.add_argument("-ht", "--higher_threshold", required=True, type=int,
                        help="QC PASS/FAIL higher threshold for gc content i.e. if number of contigs is LESS THAN OR EQUAL to higher threshold, then PASS, otherwise FAIL.")
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

    # Get GC content from contigs
    lane_ids_gc_content = get_gc_content(file_dest, lane_ids, args.assembler)

    # Write lane id, GC content and PASS/FAIL status in tab file
    write_qc_status(lane_ids_gc_content, args.lower_threshold, args.higher_threshold, header_dict["contig_gc_content"], args.output_file)


if __name__ == '__main__':
    parser = get_arguments()
    args = parser.parse_args()
    sys.exit(main(args))
