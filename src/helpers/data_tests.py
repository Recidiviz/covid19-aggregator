import os
import unittest

from helpers import data

class MapperTests(unittest.TestCase):

  def setUp(self):
    self.mapper = data.Mapper(data.load_csv(os.path.join(os.path.dirname(__file__), 'test_data/name_mappings.csv')))

  def test_init_mapper(self):
    expected_mapping = {'illinois:administrative united states penitentiary, thomson': {'type': 'Federal Prisons',
                                                                                        'state': 'Illinois',
                                                                                        'name': 'Administrative United States Penitentiary, Thomson'},
                        'federal:administrative united states penitentiary, thomson': {'type': 'Federal Prisons',
                                                                                       'state': 'Illinois',
                                                                                       'name': 'Administrative United States Penitentiary, Thomson'},
                        'pennsylvania:united states penitentiary, allenwood': {'type': 'Federal Prisons',
                                                                               'state': 'Pennsylvania',
                                                                               'name': 'United States Penitentiary, Allenwood'},
                        'federal:united states penitentiary, allenwood': {'type': 'Federal Prisons',
                                                                          'state': 'Pennsylvania',
                                                                          'name': 'United States Penitentiary, Allenwood'},
                        'pennsylvania:alp': {'type': 'Federal Prisons',
                                             'state': 'Pennsylvania',
                                             'name': 'United States Penitentiary, Allenwood'},
                        'federal:alp': {'type': 'Federal Prisons',
                                        'state': 'Pennsylvania',
                                        'name': 'United States Penitentiary, Allenwood'},
                        'florida:united states penitentiary, coleman i & ii': {'type': 'Federal Prisons',
                                                                               'state': 'Florida',
                                                                               'name': 'United States Penitentiary, Coleman I & II'},
                        'federal:united states penitentiary, coleman i & ii': {'type': 'Federal Prisons',
                                                                               'state': 'Florida',
                                                                               'name': 'United States Penitentiary, Coleman I & II'},
                        'florida:col': {'type': 'Federal Prisons',
                                        'state': 'Florida',
                                        'name': 'United States Penitentiary, Coleman I & II'},
                        'federal:col': {'type': 'Federal Prisons',
                                        'state': 'Florida',
                                        'name': 'United States Penitentiary, Coleman I & II'},
                        'florida:cop': {'type': 'Federal Prisons',
                                        'state': 'Florida',
                                        'name': 'United States Penitentiary, Coleman I & II'},
                        'federal:cop': {'type': 'Federal Prisons',
                                        'state': 'Florida',
                                        'name': 'United States Penitentiary, Coleman I & II'},
                        'virginia:augusta correctional center': {'type': 'State Prisons',
                                                                 'state': 'Virginia',
                                                                 'name': 'Augusta Correctional Center'},
                        'virginia:appalachian men‰ûªs ccap': {'type': 'State Prisons',
                                                              'state': 'Virginia',
                                                              'name': 'Augusta Correctional Center'},
                        'virginia:baskerville correctional center': {'type': 'State Prisons',
                                                                     'state': 'Virginia',
                                                                     'name': 'Baskerville Correctional Center'},
                        'virginia:central virginia correctional unit #13': {'type': 'State Prisons',
                                                                            'state': 'Virginia',
                                                                            'name': 'Central Virginia Correctional Unit #13'},
                        "virginia:chesterfield women's ccap": {'type': 'State Prisons',
                                                               'state': 'Virginia',
                                                               'name': "Chesterfield Women's CCAP"},
                        'virginia:chesterfield women‰ûªs ccap': {'type': 'State Prisons',
                                                                 'state': 'Virginia',
                                                                 'name': "Chesterfield Women's CCAP"},
                        'virginia:cold springs correctional unit': {'type': 'State Prisons',
                                                                    'state': 'Virginia',
                                                                    'name': 'Cold Springs Correctional Unit'},
                        'virginia:cold springs correctional unit #10': {'type': 'State Prisons',
                                                                        'state': 'Virginia',
                                                                        'name': 'Cold Springs Correctional Unit'},
                        'virginia:culpeper correctional facility for women': {'type': 'State Prisons',
                                                                              'state': 'Virginia',
                                                                              'name': 'Culpeper Correctional Facility for Women'},
                        'virginia:cold springs ccap': {'type': 'State Prisons',
                                                       'state': 'Virginia',
                                                       'name': 'Culpeper Correctional Facility for Women'}}

    self.assertEqual(expected_mapping,
                     self.mapper._state_and_facility_name_to_canonical_facility)

    self.assertEqual({(info['state'], info['name'], info['type']) for info in expected_mapping.values()},
                     self.mapper.get_all_facilities())

  def test_init_mapper__conflicts(self):
    with self.assertRaises(data.ValidationError) as cm:
      self.mapper = data.Mapper(data.load_csv(os.path.join(os.path.dirname(__file__),
                                                           'test_data/name_mappings__with_conflicts.csv')))

    self.assertEqual('Conflicting lookup key: florida:col',
                     str(cm.exception))

  def test_get_canonical_facility_name__simple(self):
    self.assertEqual('Baskerville Correctional Center',
                     self.mapper.get_canonical_facility_name('Virginia', 'Baskerville Correctional Center'))

  def test_get_canonical_facility_name__different_casing_and_whitespace(self):
    self.assertEqual('Baskerville Correctional Center',
                     self.mapper.get_canonical_facility_name('virginia', ' Baskerville correctional center  '))

  def test_get_canonical_facility_name__alternate_name(self):
    self.assertEqual('United States Penitentiary, Coleman I & II',
                     self.mapper.get_canonical_facility_name('Florida', 'COL'))

  def test_get_canonical_facility__unknown_facility(self):
    with self.assertRaises(data.UnknownFacilityError) as cm:
      self.mapper.get_canonical_facility_name('Virginia', 'COL')

    self.assertEqual("('Virginia', 'COL')",
                     str(cm.exception))
