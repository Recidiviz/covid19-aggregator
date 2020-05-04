from collections import defaultdict
import csv
from datetime import datetime
import os
import requests

import constants


def fetch_csv(url, as_dicts=False):
  download = requests.get(url)

  decoded_content = download.content.decode('utf-8')

  return list((csv.DictReader if as_dicts else csv.reader)(decoded_content.splitlines(), delimiter=','))


def load_csv(path, as_dicts=False):
  try:
    with open(path, encoding='utf-8') as f:
      reader = csv.DictReader(f) if as_dicts else csv.reader(f)

      return [row for row in reader]
  except:
    print('Error reading CSV at %s' % (path))

    raise


def combine_all_csvs(dir_path):
  column_names = None
  combined_rows = []

  for file_name in os.listdir(dir_path):
    if not file_name.lower().endswith('.csv'):
      continue

    rows = load_csv(os.path.join(dir_path, file_name), as_dicts=True)

    if column_names and rows[0].keys() != column_names:
      raise ValidationError('Header of %s does not match header of sibling CSV' % (file_name))
    else:
      column_names = rows[0].keys()

    combined_rows += rows[1:]

  return combined_rows


class UnknownFacilityError(Exception):
  pass


class ValidationError(Exception):
  pass


class Mapper:

  def __init__(self, mappings_csv_rows):
    # TODO: Validate order of mappings CSV headers.

    self._state_and_facility_name_to_canonical_facility = {}
    self._facilities = set()
    for row in mappings_csv_rows[1:]:
      self._add_to_mapping(row)

      if row[0] == 'Federal Prisons':
        # some data sources use "Federal" as the value for "State" when it's a federal facility
        self._add_to_mapping(row, state_key_override='Federal')

  def _add_to_mapping(self, row, state_key_override=None):
    row = [c.strip() for c in row]
    state = (state_key_override or row[1]).strip().lower()
    names = set([name.strip() for name in row[3:] if name and name.strip()])
    facility_info = {'type': row[0],
                     'state': row[1],
                     'name': row[3]}
    self._facilities.add((row[1], row[3], row[0]))

    for name in names:
      lookup_key = self._get_lookup_key(state, name)
      if lookup_key in self._state_and_facility_name_to_canonical_facility:
        raise ValidationError('Conflicting lookup key: %s' % (lookup_key))

      self._state_and_facility_name_to_canonical_facility[lookup_key] = facility_info

  @staticmethod
  def _get_lookup_key(state, name):
    return '%s:%s' % (state.strip().lower(), name.strip().lower())

  def get_canonical_facility_name(self, state, facility_name):
    lookup_key = self._get_lookup_key(state, facility_name)

    facility = self._state_and_facility_name_to_canonical_facility.get(lookup_key)

    if not facility:
      raise UnknownFacilityError((state, facility_name))

    return facility['name']

  def get_all_facilities(self):
    return self._facilities


def standardize_dataset(rows, source_id, name_mapper):
  """Takes raw data from a source and standardizes its keys.

  Args:
    rows: Array of CSV row dicts.

  Returns:
    Tuple of:
    - Array of CSV row dicts whose keys conform to the column names for the aggregated output.
    - Any unknown facilities that appeared in the data.

  Raises:
    KeyError: If expected columns are missing in the provided rows.
  """
  standardized_dataset = []
  unknown_facilities = []

  for row in [{standard_key: row[source_key] for source_key, standard_key in constants.COLUMN_MAPPINGS[source_id].items()}
              for row in rows]:
    try:
      row['Canonical Facility Name'] = name_mapper.get_canonical_facility_name(row['State'],
                                                                               row[constants.SOURCE_FACILITY_NAME_COLUMN])

      # TODO: Define date parsing logic in the dataset-specific config. For the moment, all sources use the
      #       format '5/1/20' or '5/1/2020' or '2020-05-01'.
      try:
        row['Date'] = datetime.strptime(row['Date'], '%m/%d/%y').date()
      except ValueError:
        try:
          row['Date'] = datetime.strptime(row['Date'], '%m/%d/%Y').date()
        except ValueError:
          row['Date'] = datetime.strptime(row['Date'], '%Y-%m-%d').date()

      standardized_dataset.append(row)
    except UnknownFacilityError:
      unknown_facilities.append((row['State'].strip(), row[constants.SOURCE_FACILITY_NAME_COLUMN].strip(), source_id))

  return standardized_dataset, unknown_facilities


def get_row_key(date, facility_state, facility_name):
  return '%s:%s:%s' % (date,
                       facility_state.strip().lower(),
                       facility_name.strip().lower())


def key_dataset(rows):
  """Keys dataset by date+state+facility (canonical name)."""
  keyed_data = defaultdict(list)

  for row in rows:
    keyed_data[get_row_key(row['Date'], row['State'], row['Canonical Facility Name'])].append(row)

  return keyed_data
