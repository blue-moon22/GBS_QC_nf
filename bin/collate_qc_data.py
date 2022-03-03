#!/usr/bin/env python3
import argparse
import sys
import pandas as pd

from collections import defaultdict


def write_summary_qc_report(summary_qc, output_prefix):

    with open(f'{output_prefix}_summary.tab', 'w') as out:
        out.write('lane_id\tstatus\n')
        for lane_id, status in summary_qc.items():
            out.write(f'{lane_id}\t{status}\n')


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


def write_complete_qc_report(all_reports, output_prefix):

    df = pd.DataFrame()

    for report in all_reports:
        if df.empty:
            df = pd.read_csv(report, sep = '\t')
        else:
            tmp_df = pd.read_csv(report, sep = '\t')
            df = df.merge(tmp_df, how = 'inner', on='lane_id')
    
    df.to_csv(f'{output_prefix}_complete.tab', sep = '\t', index = False)


def get_arguments():
    parser = argparse.ArgumentParser(description='Collate QC data to output complete and summary reports.')
    parser.add_argument('-i', '--qc_reports', required=True, nargs='*',
                        help='All QC reports.')
    parser.add_argument('-o', '--output_prefix', required=True, type=str,
                        help='Output prefix of QC reports.')

    return parser


def main(args):
    # Write complete report
    write_complete_qc_report(args.qc_reports, args.output_prefix)

    # Get summary QC
    summary_qc = get_summary_qc(args.qc_reports)

    # Write summary QC
    write_summary_qc_report(summary_qc, args.output_prefix)


if __name__ == '__main__':
    parser = get_arguments()
    args = parser.parse_args()
    sys.exit(main(args))
