#!/usr/bin/env python3
import argparse
import sys
import re
import pandas as pd

from collections import defaultdict

from lib.get_headers import read_header_json
from lib.get_items import get_items

def get_coverage_depth(qc_stats):

    lane_ids_cov_depth = defaultdict(lambda: None)

    with open(qc_stats, 'r') as stats:
        next(stats)
        for line in stats:
            lane_ids_cov_depth[line.split(',')[2]] = float(line.split(',')[14])

    return lane_ids_cov_depth


def write_qc_status(lane_ids, lane_ids_cov_depth, threshold, headers, output_file):

    headers.insert(0, 'lane_id')
    df = pd.DataFrame(columns=headers, index = [0])

    for ind, lane_id in enumerate(lane_ids):
        cov_depth = lane_ids_cov_depth[lane_id]
        df.loc[ind, headers[0]] = lane_id
        df.loc[ind, headers[1]] = cov_depth

        if cov_depth is not None:
            if cov_depth > threshold:
                df.loc[ind, headers[2]] = "PASS"
            else:
                df.loc[ind, headers[2]] = "FAIL"

    df.to_csv(output_file, sep = '\t', index = False)


def get_arguments():
    parser = argparse.ArgumentParser(description="Get coverage depth from Pathfind QC stats.")
    parser.add_argument("-l", "--lane_ids", required=True, type=str,
                        help="Text file of lane ids.")
    parser.add_argument("-q", "--qc_stats", required=True, type=str,
                        help="Pathfind QC stats file.")
    parser.add_argument("-t", "--threshold", required=True, type=int,
                        help="QC PASS/FAIL threshold for coverage depth i.e. if the coverage depth is GREATER THAN threshold, then PASS, otherwise FAIL.")
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
    lane_ids_cov_depth = get_coverage_depth(args.qc_stats)

    # Write lane id, number of contigs and PASS/FAIL status in tab file
    write_qc_status(lane_ids, lane_ids_cov_depth, args.threshold, header_dict["coverage_depth"], args.output_file)


if __name__ == '__main__':
    parser = get_arguments()
    args = parser.parse_args()
    sys.exit(main(args))
