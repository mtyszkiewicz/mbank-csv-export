# mbank-csv-export

A toolkit for exporting and parsing mBank transaction data with minimal manual intervention.

This project addresses the gap in mBank OSS tools - while many can parse CSV data, few can reliably automate the extraction process. This toolkit handles both extraction and parsing in a modular fashion.

## Components

### `mbank-export`
Extracts raw transaction data from mBank's web interface:
- Uses Playwright for browser automation
- Saves browser state to minimize repeated authentication

### `mbank-parser`
Transforms raw transaction data into structured formats:
- Supports JSON and CSV output
- Built with Pydantic for robust type handling

## Installation

```shell
# using pip
pip install mbank-csv-export
# using poetry
poetry add mbank-csv-export
```

## Authentication

Set environment variables (recommended):
```
MBANK_USERNAME
MBANK_PASSWORD
```

Or pass credentials directly:
```shell
mbank --username username --password password
```

## CLI Examples

```shell
# Export last month's transactions as CSV
mbank-export | mbank-parser

# Export specific date range as raw data
mbank-export --date-from '2024-05-01' --date-to '2024-09-30' > raw-operations.txt

# Parse raw data to JSON
cat raw-operations.txt | mbank-parser --format json

# One-line export and parse to JSON
mbank-export --date-from '2024-05-01' --date-to '2024-09-30' | mbank-parser --format json
```

Use `--help` for more options.

## Library Usage

```python
from datetime import date
from mbank_csv_export import (
  MBank,
  OperationsParser,
  Operation,
  to_csv,
  to_json,
)

mbank = MBank(headless=False)
mbank.login(username="1111222233334444", password="***")
csv_content: str = mbank.export_operations_csv(
    date_from=date(2024, 5, 1),
    date_to=date(2024, 9, 30)
)

operation_parser = OperationParser()
operations: list[Operation] = operation_parser.parse(csv_content)

for operation in operations:
  print(operation)
print(to_json(operations))
```

## Contributing

Issues and PRs welcome. I have my notifications enabled for prompt responses.
