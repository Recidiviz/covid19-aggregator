from constants import OUTPUT_COLUMNS

NUMERIC_COLUMNS = ['Pop Tested',
                   'Pop Tested Positive',
                   'Pop Tested Negative',
                   'Pop Deaths',
                   'Staff Tested',
                   'Staff Tested Positive',
                   'Staff Tested Negative',
                   'Staff Deaths']
TEXT_COLUMNS = ['Source',
                'Notes']

assert set(NUMERIC_COLUMNS).issubset(set(OUTPUT_COLUMNS))
assert set(TEXT_COLUMNS).issubset(set(OUTPUT_COLUMNS))


def get_value(row, column):
  """Returns the numeric value for a column in a row, or None."""
  try:
    return int(row[column])
  except (KeyError, ValueError):
    return None


def merge_column(column, rows_with_sources, sources_used):
  """Merges the values for an output column from multiple input rows into a single value."""
  rows_with_values = list(filter(lambda row_with_source: get_value(row_with_source[0], column) is not None,
                                 rows_with_sources))
  row = None
  if rows_with_values:
    # Use the largest count since it was probably recorded latest in the day
    row, source = max(rows_with_values,
                      key=lambda row_with_source: get_value(row_with_source[0], column))

  if row:
    sources_used.add(source)

  return get_value(row, column) if row else ''


def merge_rows(rows_with_sources):
  """Merges multiple input rows for the same date/facility into a single output row."""
  merged_row = {}
  sources_used = set()

  for column in NUMERIC_COLUMNS:
    merged_row[column] = merge_column(column, rows_with_sources, sources_used)

  for column in TEXT_COLUMNS:
    merged_row[column] = ','.join([row[column] for row, source_id in rows_with_sources
                                   if row.get(column) and source_id in sources_used])

  return merged_row, sources_used
