# covid19-aggregator

You can find the latest aggregated data file
at https://raw.githubusercontent.com/Recidiviz/covid19-aggregator/master/output/merged_data.csv.

## Setup

Create a Python 3 virtualenv:

```
virtualenv -p python3 .virtualenv
source .virtualenv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

## Performing daily run

### Update inputs

Fetch the latest file(s) from each source (e.g., covidprisondata.com) and add them to the source's directory
under the `data/` directory (e.g., `data/covidprisondata.com`).

Note that some sources, like Recidiviz, are fetched automatically from a URL specified in `constants.py`.

### Run the script

```
python src/aggregate.py
```

Outputs will be put in the `output` dir.

### Commit the new inputs and outputs to GitHub

This will overwrite the previously committed files in `output/`.

## Run tests

Be sure you're in the Python 3 virtualenv, then run:

```
./run_tests.sh
```
