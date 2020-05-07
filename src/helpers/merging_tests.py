import unittest

from helpers import merging

class FunctionTests(unittest.TestCase):

  def test_merge_rows__only_one_row_with_data(self):
    rows = [({'Pop Tested': '',
              'Pop Tested Positive': '',
              'Pop Tested Negative': '',
              'Pop Deaths': '',
              'Staff Tested': '',
              'Staff Tested Positive': '',
              'Staff Tested Negative': '',
              'Staff Deaths': ''},
             'source_1'),
            ({'Pop Tested': '  60    ',  # whitespace shouldn't matter
              'Pop Tested Positive': '7  ',
              'Pop Tested Negative': '53',
              'Pop Deaths': '2',
              'Staff Tested': 'NA',
              'Staff Tested Positive': '3',
              'Staff Tested Negative': 'NA',
              'Staff Deaths': 'NA'},
             'source_2')]

    self.assertEqual(({'Pop Tested': 60,
                       'Pop Tested Positive': 7,
                       'Pop Tested Negative': 53,
                       'Pop Deaths': 2,
                       'Staff Tested': '',
                       'Staff Tested Positive': 3,
                       'Staff Tested Negative': '',
                       'Staff Deaths': '',
                       'Source': '',
                       'Notes': ''},
                      {'source_2'}),
                     merging.merge_rows(rows))

  def test_merge_rows__one_row_has_largest_values(self):
    rows = [({'Pop Tested': '20',
              'Pop Tested Positive': '3',
              'Pop Tested Negative': '17',
              'Pop Deaths': '0',
              'Staff Tested': '',
              'Staff Tested Positive': '1',
              'Staff Tested Negative': '',
              'Staff Deaths': ''},
             'source_1'),
            ({'Pop Tested': '60',
              'Pop Tested Positive': '7',
              'Pop Tested Negative': '53',
              'Pop Deaths': '2',
              'Staff Tested': 'NA',
              'Staff Tested Positive': '3',
              'Staff Tested Negative': 'NA',
              'Staff Deaths': 'NA'},
             'source_2')]

    self.assertEqual(({'Pop Tested': 60,
                       'Pop Tested Positive': 7,
                       'Pop Tested Negative': 53,
                       'Pop Deaths': 2,
                       'Staff Tested': '',
                       'Staff Tested Positive': 3,
                       'Staff Tested Negative': '',
                       'Staff Deaths': '',
                       'Source': '',
                       'Notes': ''},
                      {'source_2'}),
                     merging.merge_rows(rows))

  def test_merge_rows__different_rows_with_largest_values_for_different_columns(self):
    rows = [({'Pop Tested': '',
              'Pop Tested Positive': '',
              'Pop Tested Negative': '',
              'Pop Deaths': '',
              'Staff Tested': '20',
              'Staff Tested Positive': '5',
              'Staff Tested Negative': 'NA',
              'Staff Deaths': '1'},
             'source_1'),
            ({'Pop Tested': '60',
              'Pop Tested Positive': '7',
              'Pop Tested Negative': '53',
              'Pop Deaths': '2',
              'Staff Tested': 'NA',
              'Staff Tested Positive': '3',
              'Staff Tested Negative': 'NA',
              'Staff Deaths': 'NA'},
             'source_2')]

    self.assertEqual(({'Pop Tested': 60,
                       'Pop Tested Positive': 7,
                       'Pop Tested Negative': 53,
                       'Pop Deaths': 2,
                       'Staff Tested': 20,
                       'Staff Tested Positive': 5,
                       'Staff Tested Negative': '',
                       'Staff Deaths': 1,
                       'Source': '',
                       'Notes': ''},
                      {'source_2', 'source_1'}),
                     merging.merge_rows(rows))

  def test_merge_rows__conflicting_data_from_same_source(self):
    rows = [({'Pop Tested': '',
              'Pop Tested Positive': '',
              'Pop Tested Negative': '',
              'Pop Deaths': '',
              'Staff Tested': '20',
              'Staff Tested Positive': '5',
              'Staff Tested Negative': 'NA',
              'Staff Deaths': '1'},
             'source_1'),
            ({'Pop Tested': '60',
              'Pop Tested Positive': '7',
              'Pop Tested Negative': '53',
              'Pop Deaths': '2',
              'Staff Tested': 'NA',
              'Staff Tested Positive': '3',
              'Staff Tested Negative': 'NA',
              'Staff Deaths': 'NA'},
             'source_1')]

    self.assertEqual(({'Pop Tested': 60,
                       'Pop Tested Positive': 7,
                       'Pop Tested Negative': 53,
                       'Pop Deaths': 2,
                       'Staff Tested': 20,
                       'Staff Tested Positive': 5,
                       'Staff Tested Negative': '',
                       'Staff Deaths': 1,
                       'Source': '',
                       'Notes': ''},
                      {'source_1'}),
                     merging.merge_rows(rows))

  def test_merge_rows__no_rows_with_data(self):
    rows = [({'Pop Tested': '',
              'Pop Tested Positive': '',
              'Pop Tested Negative': '',
              'Pop Deaths': '',
              'Staff Tested': '',
              'Staff Tested Positive': '',
              'Staff Tested Negative': 'NA',
              'Staff Deaths': ''},
             'source_1'),
            ({'Pop Tested': '?',
              'Pop Tested Positive': '',
              'Pop Tested Negative': '',
              'Pop Deaths': '',
              'Staff Tested': 'NA',
              'Staff Tested Positive': '',
              'Staff Tested Negative': 'NA',
              'Staff Deaths': 'NA'},
             'source_2')]

    self.assertEqual(({'Pop Tested': '',
                       'Pop Tested Positive': '',
                       'Pop Tested Negative': '',
                       'Pop Deaths': '',
                       'Staff Tested': '',
                       'Staff Tested Positive': '',
                       'Staff Tested Negative': '',
                       'Staff Deaths': '',
                       'Source': '',
                       'Notes': ''},
                      set()),
                     merging.merge_rows(rows))

  def test_merge_rows__rows_include_merged_text_columns(self):
    rows = [({'Pop Tested': '',
              'Pop Tested Positive': '',
              'Pop Tested Negative': '',
              'Pop Deaths': '',
              'Staff Tested': '',
              'Staff Tested Positive': '',
              'Staff Tested Negative': '',
              'Staff Deaths': '1',
              'Notes': 'Notes from source_1'},
             'source_1'),
            ({'Pop Tested': '60',
              'Pop Tested Positive': '7',
              'Pop Tested Negative': '53',
              'Pop Deaths': '2',
              'Staff Tested': 'NA',
              'Staff Tested Positive': '3',
              'Staff Tested Negative': 'NA',
              'Staff Deaths': 'NA',
              'Source': 'Public records 1',
              'Notes': 'Notes from source_2'},
             'source_2'),
            ({'Pop Tested': '60',
              'Pop Tested Positive': '7',
              'Pop Tested Negative': '53',
              'Pop Deaths': '2',
              'Staff Tested': 'NA',
              'Staff Tested Positive': '3',
              'Staff Tested Negative': 'NA',
              'Staff Deaths': 'NA',
              'Source': 'Public records 2'},  # not included in output because source wasn't used
             'source_3')
            ]

    self.assertEqual(({'Pop Tested': 60,
                       'Pop Tested Positive': 7,
                       'Pop Tested Negative': 53,
                       'Pop Deaths': 2,
                       'Staff Tested': '',
                       'Staff Tested Positive': 3,
                       'Staff Tested Negative': '',
                       'Staff Deaths': 1,
                       'Source': 'Public records 1',
                       'Notes': 'Notes from source_1,Notes from source_2'
                       },
                      {'source_1', 'source_2'}),
                     merging.merge_rows(rows))
