# covid19-aggregator

## Run script

Create a Python 3 virtualenv:

```
virtualenv -p python3 .virtualenv
source .virtualenv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the script (outputs will appear in the `output` dir):

```
python src/aggregate.py
```

## Run tests

Be sure you're in the Python 3 virtualenv, then run:

```
./run_tests.sh
```
