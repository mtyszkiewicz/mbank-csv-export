import json
import re
import sys
from argparse import ArgumentParser
from pathlib import Path

accounts_regexp = re.compile(r"(?P<account_name>[\w ]+) - (?P<account_number>\d+);")

def parse_mbank_operations(csv_content: str) -> list[dict]:
    result = []
    header, data = csv_content.split("#Data operacji;#Opis operacji;#Rachunek;#Kategoria;#Kwota;\n")
    data
    for account_name, account_number in accounts_regexp.findall(header):
        data = data.replace(f'"{account_name.strip()} {account_number[:4]} ... {account_number[-4:]}"', account_number)
    
    for line in data.splitlines():
        try:
            operation_date, operation_description, account_number, operation_name, transaction_amount, *_ = line.split(";")
        except ValueError:
            print(line.split(";"))
            return

        operation_description = re.sub(r'\s{2,}', '  ', operation_description).removeprefix('"').removesuffix('  "')
        result.append({
            "operation_date": operation_date,
            "operation_description": operation_description,
            "account_number": account_number,
            "operation_name": operation_name,
            "transaction_amount": transaction_amount
        })
    return result

def to_csv(operations: list[dict]) -> str:
    if len(operations) == 0:
        return ""  
    columns = ",".join(operations[0].keys())
    values = "\n".join(",".join(d.values()) for d in operations)
    return f"{columns}\n{values}"

        
def main():
    argparser = ArgumentParser(
        prog="mbank-parser"
    )
    argparser.add_argument(
        "--input", "-i",
        type=str, default="-", help="input file path"
    )
    argparser.add_argument(
        "--output", "-o",
        type=str, default="-", help="output file path"
    )
    argparser.add_argument(
        "--format",
        type=str, 
        choices=["json", "csv"],
        default="csv"
    )
    args = argparser.parse_args()

    if args.input != "-" and not Path(args.input).exists():
        print("Error: Input path does not exist.")

    if args.input == "-":
        csv_content: str = sys.stdin.read()
    else:
        csv_content: str = Path(args.input).read_text()

    operations: list[dict] = parse_mbank_operations(csv_content)

    if args.format == "json":
        operations_formatted: str = json.dumps(operations)
    elif args.format == "csv":
        operations_formatted: str = to_csv(operations)

    if args.output == "-":
        print(operations_formatted)
    else:
        Path(args.output).write_text(operations_formatted)