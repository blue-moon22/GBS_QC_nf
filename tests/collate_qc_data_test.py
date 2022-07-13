from unittest import TestCase

import os

from collections import defaultdict
from bin.collate_qc_data import *
import numpy as np


class CollateQCData(TestCase):
    TEST_DATA_DIR = 'tests/test_data'
    TEST_REL_ABND = f'{TEST_DATA_DIR}/test_relative_abundance.tab'
    TEST_CONTIG_NO = f'{TEST_DATA_DIR}/test_contig_number.tab'
    TEST_OUTPUT_PREFIX = f'{TEST_DATA_DIR}/qc_report'
    TEST_OUTPUT_PREFIX2 = f'{TEST_DATA_DIR}/qc_report2'
    TEST_VERSION = f'{TEST_DATA_DIR}/version.txt'


    def test_get_complete_qc_report(self):

        actual = get_complete_qc_report([self.TEST_REL_ABND, self.TEST_CONTIG_NO], self.TEST_VERSION)

        self.assertEqual(actual.to_dict()['lane_id'], {
            0: 'test_lane1',
            1: 'test_lane2',
            2: 'test_lane3',
            3: 'test_lane4'})

    def test_get_summary_qc(self):

        actual = get_summary_qc([self.TEST_REL_ABND, self.TEST_CONTIG_NO])

        self.assertEqual(actual, {'test_lane1': 'PASS', 'test_lane2': 'FAIL', 'test_lane3': 'FAIL', 'test_lane4': ''})

    def test_write_summary_qc_report(self):
        summary_qc = defaultdict(lambda: 'PASS')
        summary_qc['test_lane1'] = 'PASS'
        summary_qc['test_lane2'] = 'FAIL'
        summary_qc['test_lane3'] = 'FAIL'
        summary_qc['test_lane4'] = ''

        complete_report = get_complete_qc_report([self.TEST_REL_ABND, self.TEST_CONTIG_NO], self.TEST_VERSION)

        write_summary_qc_report(summary_qc, complete_report, self.TEST_OUTPUT_PREFIX)

    def test_arguments(self):
        actual = get_arguments().parse_args(
            ['--qc_reports', 'report1', 'report2', '--version', 'version', '--output_prefix', 'output_txt_file'])
        self.assertEqual(actual, argparse.Namespace(qc_reports=['report1', 'report2'], version='version', output_prefix='output_txt_file'))

    def test_arguments_short_options(self):
        actual = get_arguments().parse_args(
            ['-i', 'report1', 'report2', '-v', 'version', '-o', 'output_txt_file'])
        self.assertEqual(actual, argparse.Namespace(qc_reports=['report1', 'report2'], version='version', output_prefix='output_txt_file'))

    def test_main(self):
        args = get_arguments().parse_args(
            ['--qc_reports', self.TEST_REL_ABND, self.TEST_CONTIG_NO, '--version', self.TEST_VERSION, '--output_prefix', self.TEST_OUTPUT_PREFIX2])

        main(args)

        file = open(f'{self.TEST_OUTPUT_PREFIX2}_summary.txt', "r")
        actual = "".join(file.readlines())
        os.remove(f'{self.TEST_OUTPUT_PREFIX2}_summary.txt')

        self.assertEqual(actual, """lane_id\tstatus\trel_abundance_status\tcontig_no_status\tversion\ntest_lane1\tPASS\tPASS\tPASS\tv0.0.0\ntest_lane2\tFAIL\tFAIL\tFAIL\tv0.0.0\ntest_lane3\tFAIL\tFAIL\tPASS\tv0.0.0\ntest_lane4\t\t\tFAIL\tv0.0.0\n""")

        file = open(f'{self.TEST_OUTPUT_PREFIX2}_complete.txt', "r")
        actual = "".join(file.readlines())
        os.remove(f'{self.TEST_OUTPUT_PREFIX2}_complete.txt')

        self.assertEqual(actual, """lane_id\trel_abundance\trel_abundance_status\tcontig_no\tcontig_no_status\tversion\ntest_lane1\t92.38\tPASS\t1\tPASS\tv0.0.0\ntest_lane2\t2.38\tFAIL\t500\tFAIL\tv0.0.0\ntest_lane3\t70.0\tFAIL\t3\tPASS\tv0.0.0\ntest_lane4\t\t\t501\tFAIL\tv0.0.0\n""")
