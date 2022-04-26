#!/usr/bin/env python3
import argparse
import sys
import os
import re
import pandas as pd

from collections import defaultdict

from lib.get_headers import read_header_json
from lib.get_items import get_items

def get_het_snps(data_dir):

    lane_ids_het_snps = defaultdict(lambda: None)

    for file in os.listdir(data_dir):
        if file.endswith("stats"):
            with open(f'{data_dir}/{file}', 'r') as stats:
                next(stats)
                for line in stats:
                    lane_id = file.rsplit('_', 1)[0]
                    lane_ids_het_snps[lane_id] = int(line.split('\t')[0])

    return lane_ids_het_snps


def write_qc_status(lane_ids, lane_ids_het_snps, threshold, headers, output_file):

    headers.insert(0, 'lane_id')
    df = pd.DataFrame(columns=headers, index = [0])

    for ind, lane_id in enumerate(lane_ids):
        het_snps = lane_ids_het_snps[lane_id]
        df.loc[ind, headers[0]] = lane_id
        df.loc[ind, headers[1]] = het_snps

        if het_snps is not None:
            if het_snps <= threshold:
                df.loc[ind, headers[2]] = "PASS"
            else:
                df.loc[ind, headers[2]] = "FAIL"

    df.to_csv(output_file, sep = '\t', index = False)


def get_arguments():
    parser = argparse.ArgumentParser(description="Get number of HET SNPs from Pathfind snp.")
    parser.add_argument("-l", "--lane_ids", required=True, type=str,
                        help="Text file of lane ids.")
    parser.add_argument("-d", "--data_dir", required=True, type=str,
                        help="Data directory.")
    parser.add_argument("-t", "--threshold", required=True, type=int,
                        help="QC PASS/FAIL threshold for HET SNPs i.e. if HET SNPs is LESS THAN OR EQUAL TO threshold, then PASS, otherwise FAIL.")
    parser.add_argument("-j", "--headers", required=True, type=str,
                        help="JSON of headers for QC report.")
    parser.add_argument("-o", "--output_file", required=True, type=str,
                        help="Output tab file.")

    return parser


def main(args):
    # Get lane ids
    lane_ids = get_items(args.lane_ids)

    # Get column headers from headers json
    header_dict = read_header_json(args.headers)

    # Get number of contigs
    lane_ids_het_snps = get_het_snps(args.data_dir)

    # Write lane id, number of contigs and PASS/FAIL status in tab file
    write_qc_status(lane_ids, lane_ids_het_snps, args.threshold, header_dict["het_snps"], args.output_file)


if __name__ == '__main__':
    parser = get_arguments()
    args = parser.parse_args()
    sys.exit(main(args))
