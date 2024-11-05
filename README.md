# mbank-csv-export

Hey, looking for mBank operations export automation tool? Then you've came to the right place!

Many projects successfully attempt to parse mBank CSV operations, but few reliably automate the extraction process. 
I decided to develop solutions for both of those problems, but in a modular fashion, letting you choose to use just one.

`mbank-export` only exports transactions from mBank. It return an unparsed content string.
 - Uses Playwright to automate browser interaction.
 - Saves browser state to maintain session continuity, minimizing the need for repeated mobile authentication.

`mbank-parser` parses the transactions and converts them to a desired data format.
 - Currently supported output formats are json and csv.
 - Uses Pydantic under the hood for good developer experience when used as a library.

## Installation
```shell
pip install mbank-csv-export
```

## Auth
Set `MBANK_USERNAME` and `MBANK_PASSWORD` environment variables or quick start by running `mbank --username username --password password`.

## CLI
```shell
# Export last month operations, parse and format as clean csv:  
mbank-export | mbank-parser

# Export raw operations data from 2024-05-01 to 2024-09-30:  
mbank-export --date-from '2024-05-01' --date-to '2024-09-30' > raw-operations.txt

# Then parse and format those raw operations into json:  
cat raw-operations.txt | mbank-parser --format json

# Or in one line:  
mbank-export --date-from '2024-05-01' --date-to '2024-09-30' | mbank-parser --format json
```

## Python package
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







