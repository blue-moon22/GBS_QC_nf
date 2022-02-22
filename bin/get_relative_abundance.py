#!/usr/bin/env python3
import argparse
import sys
import re
import pandas as pd

from lib.get_headers import read_header_json

def get_relative_abundance(kraken_report, species):
    """Get the relative abundance for a species from the kraken report"""

    rel_abnd = None
    with open(kraken_report, "r") as file:
        for line in file:
            if re.search(f'{species}$', line):
                rel_abnd = float(line.split('\t')[0].lstrip().split(' ')[0])
                break

    return rel_abnd


def write_qc_status(lane_id, threshold, rel_abnd, headers, output_file):
    headers.insert(0, 'lane_id')
    df = pd.DataFrame(columns=headers, index = [0])
    df.loc[0, headers[0]] = lane_id
    df.loc[0, headers[1]] = rel_abnd

    if rel_abnd is not None:
        if rel_abnd > threshold:
            df.loc[0, headers[2]] = "PASS"
        else:
            df.loc[0, headers[2]] = "FAIL"

    df.to_csv(output_file, sep = '\t', index = False)


def get_arguments():
    parser = argparse.ArgumentParser(description="Get species' relative abundance from kraken report")
    parser.add_argument("-l", "--lane_id", required=True, type=str,
                        help="Lane id")
    parser.add_argument("-k", "--kraken_report", required=True, type=str,
                        help="Kraken report file")
    parser.add_argument("-s", "--species", required=True, type=str,
                        help="Species name, e.g. 'Streptococcus agalactiae' or 'Streptococcus pneumoniae'")
    parser.add_argument("-t", "--threshold", required=True, type=float,
                        help="QC PASS/FAIL threshold for relative abundance i.e. if relative abundance GREATER THAN threshold, then PASS, otherwise FAIL.")
    parser.add_argument("-j", "--headers", required=True, type=str,
                        help="JSON of headers for QC report.")
    parser.add_argument("-o", "--output_file", required=True, type=str,
                        help="Output tab file.")

    return parser


def main():
    parser = get_arguments()
    args = parser.parse_args()

    # Get column headers from headers json
    header_dict = read_header_json(args.headers)

    # Get relative abundance from kraken report
    rel_abnd = get_relative_abundance(args.kraken_report, args.species)

    # Write lane id, relative abundance and PASS/FAIL status in tab file
    write_qc_status(args.lane_id, args.threshold, rel_abnd, header_dict["relative_abundance"], args.output_file)


if __name__ == '__main__':
    sys.exit(main())
