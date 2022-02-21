from unittest import TestCase
from unittest.mock import patch, Mock, call, ANY

from lib.get_headers import *

class GetHeaders(TestCase):
    TEST_HEADER_FILE = 'tests/test_data/test_headers.json'

    def test_read_header_json(self):
        actual = read_header_json(self.TEST_HEADER_FILE)

        self.assertEqual(actual, {'gc_coverage': ['gc_coverage', 'gc_coverage_status'],
                                    'relative_abundance': ['rel_abundance', 'rel_abundance_status']})
