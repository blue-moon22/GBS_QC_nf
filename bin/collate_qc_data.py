#!/usr/bin/env python3
import argparse
import sys
import pandas as pd

from collections import defaultdict


def write_summary_qc_report(summary_qc, complete_report, output_prefix):

    summary_report = pd.DataFrame()
    summary_report['lane_id'] = summary_qc.keys()
    summary_report['status'] = summary_qc.values()

    status_columns = ['lane_id']
    status_columns.extend([column for column in complete_report.columns if 'status' in column or 'version' in column])

    summary_report = summary_report.merge(complete_report[status_columns], how = 'inner', on='lane_id')

    summary_report.to_csv(f'{output_prefix}_summary.txt', sep = '\t', index = False)


def get_summary_qc(all_reports):

    summary_qc = defaultdict(lambda: 'PASS')
    for report in all_reports:
        with open(report, 'r') as file:
            next(file)
            for line in file:
                lane_id = line.split('\t')[0]
                status = line.split('\n')[0].split('\t')[2]
                if status == '':
                    summary_qc[lane_id] = ''

                if summary_qc[lane_id] == 'PASS':
                    if status == 'FAIL':
                        summary_qc[lane_id] = 'FAIL'
                    else:
                        summary_qc[lane_id] = 'PASS'

    return summary_qc


def get_complete_qc_report(all_reports, version_file):

    df = pd.DataFrame()

    for report in all_reports:
        if df.empty:
            df = pd.read_csv(report, sep = '\t')
        else:
            tmp_df = pd.read_csv(report, sep = '\t')
            df = df.merge(tmp_df, how = 'inner', on='lane_id')

    version = ''
    with open(version_file, 'r') as file:
        next(file)
        for line in file:
            version = line.replace("\n", "")

    df['version'] = version

    return df


def get_arguments():
    parser = argparse.ArgumentParser(description='Collate QC data to output complete and summary reports.')
    parser.add_argument('-i', '--qc_reports', required=True, nargs='*',
                        help='All QC reports.')
    parser.add_argument('-v', '--version', dest='version', required=True,
                        help='Input file with version of pipeline.')
    parser.add_argument('-o', '--output_prefix', required=True, type=str,
                        help='Output prefix of QC reports.')

    return parser


def main(args):
    # Write complete report
    complete_report = get_complete_qc_report(args.qc_reports, args.version)
    complete_report.to_csv(f'{args.output_prefix}_complete.txt', sep = '\t', index = False)

    # Get summary QC
    summary_qc = get_summary_qc(args.qc_reports)

    # Write summary QC
    write_summary_qc_report(summary_qc, complete_report, args.output_prefix)


if __name__ == '__main__':
    parser = get_arguments()
    args = parser.parse_args()
    sys.exit(main(args))
