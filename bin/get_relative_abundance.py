#!/usr/bin/env python3
import argparse
import sys
import re
import pandas as pd

from lib.get_headers import read_header_json
from lib.get_items import get_items

def search_rel_abund(kraken_report, species):

    rel_abnd = None
    try:
        with open(kraken_report, "r") as file:
            for line in file:
                if re.search(f'{species}$', line):
                    rel_abnd = float(line.split('\t')[0].lstrip().split(' ')[0])
                    break

    except:
        print("Kraken report does not exist.")

    return rel_abnd


def get_relative_abundance(file_dest, lane_ids, species):
    """Get the relative abundance for a species from the kraken report"""

    lane_ids_rel_abnds = []
    for lane_id in lane_ids:
        kraken_report = [f'{dest}/kraken.report' for dest in file_dest if f'/{lane_id}/' in f'{dest}/kraken.report']
        if kraken_report:
            rel_abnd = search_rel_abund(kraken_report[0], species)
        else:
            rel_abnd = None

        lane_ids_rel_abnds.append((lane_id, rel_abnd))

    return lane_ids_rel_abnds


def write_qc_status(lane_ids_rel_abnds, threshold, headers, output_file):

    headers.insert(0, 'lane_id')
    df = pd.DataFrame(columns=headers, index = [0])

    for ind, lane_id_rel_abnd in enumerate(lane_ids_rel_abnds):
        rel_abnd = lane_id_rel_abnd[1]
        df.loc[ind, headers[0]] = lane_id_rel_abnd[0]
        df.loc[ind, headers[1]] = rel_abnd

        if rel_abnd is not None:
            if rel_abnd > threshold:
                df.loc[ind, headers[2]] = "PASS"
            else:
                df.loc[ind, headers[2]] = "FAIL"

    df.to_csv(output_file, sep = '\t', index = False)


def get_arguments():
    parser = argparse.ArgumentParser(description="Get species' relative abundance from kraken report")
    parser.add_argument("-l", "--lane_ids", required=True, type=str,
                        help="Text file of lane ids.")
    parser.add_argument("-d", "--file_dest", required=True, type=str,
                        help="Desinations for kraken report files.")
    parser.add_argument("-s", "--species", required=True, type=str,
                        help="Species name, e.g. 'Streptococcus agalactiae' or 'Streptococcus pneumoniae'")
    parser.add_argument("-t", "--threshold", required=True, type=float,
                        help="QC PASS/FAIL threshold for relative abundance i.e. if relative abundance GREATER THAN threshold, then PASS, otherwise FAIL.")
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
    lane_ids_rel_abnds = get_relative_abundance(file_dest, lane_ids, args.species)

    # Write lane id, relative abundance and PASS/FAIL status in tab file
    write_qc_status(lane_ids_rel_abnds, args.threshold, header_dict["relative_abundance"], args.output_file)


if __name__ == '__main__':
    parser = get_arguments()
    args = parser.parse_args()
    sys.exit(main(args))
