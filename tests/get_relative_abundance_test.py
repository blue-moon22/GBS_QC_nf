from unittest import TestCase
from unittest.mock import patch, Mock, call, ANY

import os
from bin.get_relative_abundance import *

class GetRelativeAbundance(TestCase):
    TEST_LANE_ID = 'lane1'
    TEST_LANE_ID2 = 'lane2'
    TEST_DATA_DIR = 'tests/test_data'
    TEST_KRAKEN_REPORT = f'{TEST_DATA_DIR}/test_{TEST_LANE_ID}_kraken.report'
    TEST_KRAKEN_REPORT_MULTIPLE_LEADING_WHITESPACE  = f'{TEST_DATA_DIR}/test_{TEST_LANE_ID2}_kraken.report.multiple_leading_whitespace'
    TEST_KRAKEN_REPORT_EMPTY = f'{TEST_DATA_DIR}/test_empty_kraken.report'
    TEST_OUTPUT_FILE = f'tests/test_data/{TEST_LANE_ID}_relative_abundance.tab'
    TEST_OUTPUT_FILE2 = f'tests/test_data/{TEST_LANE_ID2}_relative_abundance.tab'

    def test_get_relative_abundance(self):
        actual = get_relative_abundance(self.TEST_KRAKEN_REPORT, "Streptococcus agalactiae")

        self.assertEqual(92.38, actual)

    def test_get_relative_abundance_multiple_leading_whitespace(self):
        """
        Tests parsing of kraken report when there is more than one whitespace prior to relative abundance number.
        This case is known to occur when relative abundance is <10.
        """
        actual = get_relative_abundance(self.TEST_KRAKEN_REPORT_MULTIPLE_LEADING_WHITESPACE, "Streptococcus agalactiae")

        self.assertEqual(2.38, actual)

    def test_get_relative_abundance_empty_kraken_report(self):
        actual = get_relative_abundance(self.TEST_KRAKEN_REPORT_EMPTY, "Streptococcus agalactiae")

        self.assertEqual(None, actual)

    def test_write_qc_status_pass(self):
        write_qc_status(self.TEST_LANE_ID, 70, 92.38, [ "rel_abundance", "rel_abundance_status"], self.TEST_OUTPUT_FILE)

        file = open(self.TEST_OUTPUT_FILE, "r")
        actual = "".join(file.readlines())
        os.remove(self.TEST_OUTPUT_FILE)

        self.assertEqual(actual, """lane_id\trel_abundance\trel_abundance_status\nlane1\t92.38\tPASS\n""")

    def test_write_qc_status_fail(self):
        write_qc_status(self.TEST_LANE_ID2, 70, 2.38, ["rel_abundance", "rel_abundance_status"], self.TEST_OUTPUT_FILE2)

        file = open(self.TEST_OUTPUT_FILE2, "r")
        actual = "".join(file.readlines())
        os.remove(self.TEST_OUTPUT_FILE2)

        self.assertEqual(actual, """lane_id\trel_abundance\trel_abundance_status\nlane2\t2.38\tFAIL\n""")

    def test_write_qc_status_none(self):
        write_qc_status(self.TEST_LANE_ID, 70, None, ["rel_abundance", "rel_abundance_status"], self.TEST_OUTPUT_FILE)

        file = open(self.TEST_OUTPUT_FILE, "r")
        actual = "".join(file.readlines())
        os.remove(self.TEST_OUTPUT_FILE)

        self.assertEqual(actual, """lane_id\trel_abundance\trel_abundance_status\nlane1\t\t\n""")

    def test_arguments(self):
        actual = get_arguments().parse_args(
            ['--lane_id', 'lane1', '--kraken_report', 'kraken_report', '--species', 'Streptococcus agalactiae', '--threshold', '70',
            '--headers', 'header_json', '--output_file', 'output_tab_file'])
        self.assertEqual(actual,
                         argparse.Namespace(lane_id='lane1', kraken_report='kraken_report', species='Streptococcus agalactiae',
                         threshold=70.0, headers='header_json', output_file='output_tab_file'))

    def test_arguments_short_options(self):
        actual = get_arguments().parse_args(
            ['-l', 'lane1', '-k', 'kraken_report', '-s', 'Streptococcus agalactiae', '-t', '70',
            '-j', 'header_json', '-o', 'output_tab_file'])
        self.assertEqual(actual,
                         argparse.Namespace(lane_id='lane1', kraken_report='kraken_report', species='Streptococcus agalactiae',
                         threshold=70.0, headers='header_json', output_file='output_tab_file'))


    @patch('bin.get_relative_abundance.get_arguments')
    @patch('bin.get_relative_abundance.read_header_json')
    @patch('bin.get_relative_abundance.get_relative_abundance')
    @patch('bin.get_relative_abundance.write_qc_status')
    def test_main(self, mock_write_qc_status, mock_get_relative_abundance, mock_read_header_json, mock_get_arguments):
        mock_get_arguments = get_arguments().parse_args(
            ['--lane_id', 'lane1', '--kraken_report', 'kraken_report', '--species', 'Streptococcus agalactiae', '--threshold', '70',
            '--headers', 'header_json', '--output_file', 'output_tab_file'])
        mock_read_header_json.return_value = {'relative_abundance': ['lane_id', 'rel_abundance', 'rel_abundance_status']}
        mock_get_relative_abundance.return_value = 92.38

        main()

        mock_read_header_json.call_args_list = call('header_json')
        mock_get_relative_abundance.call_args_list = call('kraken_report', 'Streptococcus agalactiae')
        mock_write_qc_status.call_args_list = call('lane1', 70.0, 92.38, ['lane_id', 'rel_abundance', 'rel_abundance_status'], 'output_tab_file')
