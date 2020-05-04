import datetime

RECIDIVIZ_DATA_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTbxP67VHDHQt4xvpNmzbsXyT0pSh_b1Pn7aY5Ac089KKYnPDT6PpskMBMvhOX_PA08Zqkxt4zNn8_y/pub?gid=0&single=true&output=csv'
MAPPINGS_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT95DUfwcHbauuuMScd1Jb9u3vLCdfCcieXrRthNowoSbrmeWF3ibv06LkfcDxl1Vd97S5aujvnHdZX/pub?gid=1112897899&single=true&output=csv'

OUTPUT_START_DATE = datetime.date(2020, 3, 31)

OUTPUT_COLUMNS = ['Date',
                  'Facility Type',
                  'State',
                  #'County',
                  'Canonical Facility Name',
                  'Pop Tested',
                  'Pop Tested Positive',
                  'Pop Tested Negative',
                  'Pop Deaths',
                  'Staff Tested',
                  'Staff Tested Positive',
                  'Staff Tested Negative',
                  'Staff Deaths',
                  'Source',
                  'Compilation',
                  'Notes'
                  ]

SOURCE_FACILITY_NAME_COLUMN = 'Source Facility Name'

COLUMN_MAPPINGS = {
  'covidprisondata.com': {'State': 'State',
                          'Facility': SOURCE_FACILITY_NAME_COLUMN,
                          'Scrape Date': 'Date',
                          'Inmates Positive': 'Pop Tested Positive',
                          'Inmates Negative': 'Pop Tested Negative',
                          #'Inmates Pending': '',  # TODO: Determine what to do with this.
                          'Inmates Tested': 'Pop Tested',
                          #'Inmates Recovered': '',
                          'Inmates Deaths': 'Pop Deaths'},
  'UCLA Law Behind Bars': {#'Facility': '',  # facility type, e.g., "Prison"
                           'State': 'State',  # Federal facilities have value of "Federal" for this column
                           'Name': SOURCE_FACILITY_NAME_COLUMN,
                           'Staff Confirmed': 'Staff Tested Positive',
                           'Residents confirmed': 'Pop Tested Positive',
                           'Staff Deaths': 'Staff Deaths',
                           'Resident Deaths': 'Pop Deaths',
                           'Date': 'Date'},
  'Recidiviz': {'As of...? (Date)': 'Date',
                #'Facility Type': '',
                'State': 'State',
                #'County': '',
                'Facility': SOURCE_FACILITY_NAME_COLUMN,
                'Population Tested': 'Pop Tested',
                'Population Tested Positive': 'Pop Tested Positive',
                'Population Tested Negative': 'Pop Tested Negative',
                'Population Deaths': 'Pop Deaths',
                'Staff Tested': 'Staff Tested',
                'Staff Tested Positive': 'Staff Tested Positive',
                'Staff Tested Negative': 'Staff Tested Negative',
                'Staff Deaths': 'Staff Deaths',
                'Source': 'Source',
                'Notes': 'Notes'
                }
}


for dataset_id, dataset in COLUMN_MAPPINGS.items():
  mapped_columns = set(dataset.values())
  assert len(dataset.values()) == len(mapped_columns), 'Duplicate mappings in dataset %s' % (dataset_id)
  assert mapped_columns.issubset(set(OUTPUT_COLUMNS + [SOURCE_FACILITY_NAME_COLUMN])), 'Invalid mappings in dataset %s' % (dataset_id)
