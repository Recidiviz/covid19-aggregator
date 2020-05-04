import csv
import datetime
import os

import constants
from helpers import data
from helpers import merging


def load_data_dir(dir_name):
  return data.combine_all_csvs(os.path.join(os.path.dirname(__file__), '../data', dir_name))


def write_unknown_facilities(unknown_facilities):
  with open(os.path.join(os.path.dirname(__file__), '../output/unknown_facilities.csv'), 'w', encoding='utf-8') as f:
    csv_writer = csv.writer(f)

    csv_writer.writerow(['State', 'Facility name', 'Source using this name'])
    for row in set(unknown_facilities):
      csv_writer.writerow(row)

def write_merged_data(merged_data):
  with open(os.path.join(os.path.dirname(__file__), '../output/merged_data.csv'), 'w', encoding='utf-8') as f:
    csv_writer = csv.DictWriter(f, fieldnames=constants.OUTPUT_COLUMNS)

    csv_writer.writeheader()

    for row in merged_data:
      csv_writer.writerow(row)


def aggregate():
  name_mapper = data.Mapper(data.fetch_csv(constants.MAPPINGS_URL))

  datasets = {'covidprisondata.com': load_data_dir('covidprisondata.com'),
              'UCLA Law Behind Bars': load_data_dir('ucla'),
              'Recidiviz': data.fetch_csv(constants.RECIDIVIZ_DATA_URL, as_dicts=True)}

  all_unknown_facilities = []

  for dataset_id, dataset in datasets.items():
    print('Num rows in %s: %s' % (dataset_id, len(dataset)))

    standardized_dataset, unknown_facilities = data.standardize_dataset(dataset, dataset_id, name_mapper)

    datasets[dataset_id] = data.key_dataset(standardized_dataset)
    all_unknown_facilities += unknown_facilities

  write_unknown_facilities(all_unknown_facilities)

  current_date = constants.OUTPUT_START_DATE
  more_data = True

  merged_rows = []
  all_facilities = name_mapper.get_all_facilities()

  while more_data:
    more_data = False

    for facility_state, facility_name, facility_type in all_facilities:
      rows_with_sources = []
      lookup_key = data.get_row_key(current_date, facility_state, facility_name)

      for dataset_id, dataset in datasets.items():
        rows_with_sources += [(row, dataset_id) for row in dataset.get(lookup_key, [])]

      if not more_data and rows_with_sources:
        more_data = True

      if rows_with_sources:
        merged_row, sources_used = merging.merge_rows(rows_with_sources)

        merged_row.update({'Date': str(current_date),
                           'State': facility_state,
                           'Facility Type': facility_type,
                           'Canonical Facility Name': facility_name,
                           'Compilation': ','.join(sources_used)})

        merged_rows.append(merged_row)

    current_date += datetime.timedelta(days=1)

  write_merged_data(merged_rows)


if __name__ == '__main__':
  aggregate()
