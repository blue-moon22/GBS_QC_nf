#!/usr/bin/env python3
import argparse
import sys
import re
import pandas as pd

from collections import defaultdict

from lib.get_headers import read_header_json
from lib.get_items import get_items

def get_percentage_het_snps(qc_stats):

    lane_ids_perc_het_snps = defaultdict(lambda: None)

    with open(qc_stats, 'r') as stats:
        next(stats)
        for line in stats:
            lane_ids_perc_het_snps[line.split(',')[2]] = float(line.split(',')[26])

    return lane_ids_perc_het_snps


def write_qc_status(lane_ids, lane_ids_perc_het_snps, threshold, headers, output_file):

    headers.insert(0, 'lane_id')
    df = pd.DataFrame(columns=headers, index = [0])

    for ind, lane_id in enumerate(lane_ids):
        perc_het_snps = lane_ids_perc_het_snps[lane_id]
        df.loc[ind, headers[0]] = lane_id
        df.loc[ind, headers[1]] = perc_het_snps

        if perc_het_snps is not None:
            if perc_het_snps < threshold:
                df.loc[ind, headers[2]] = "PASS"
            else:
                df.loc[ind, headers[2]] = "FAIL"

    df.to_csv(output_file, sep = '\t', index = False)


def get_arguments():
    parser = argparse.ArgumentParser(description="Get percentage HET SNPs (of total SNPs) from Pathfind QC stats.")
    parser.add_argument("-l", "--lane_ids", required=True, type=str,
                        help="Text file of lane ids.")
    parser.add_argument("-q", "--qc_stats", required=True, type=str,
                        help="Pathfind QC stats file.")
    parser.add_argument("-t", "--threshold", required=True, type=int,
                        help="QC PASS/FAIL threshold for percentage HET SNPs i.e. if the percentage HET SNPs is LESS THAN threshold, then PASS, otherwise FAIL.")
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
    lane_ids_perc_het_snps = get_percentage_het_snps(args.qc_stats)

    # Write lane id, number of contigs and PASS/FAIL status in tab file
    write_qc_status(lane_ids, lane_ids_perc_het_snps, args.threshold, header_dict["percentage_het_snps"], args.output_file)


if __name__ == '__main__':
    parser = get_arguments()
    args = parser.parse_args()
    sys.exit(main(args))
