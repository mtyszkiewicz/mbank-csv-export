from datetime import date

import pytest

from mbank_csv_export.parser import Account, Operation, OperationsParser


@pytest.fixture
def parser():
    return OperationsParser()

@pytest.fixture
def sample_csv_content():
    return """Nazwa konta - Konto Osobiste;
Waluta - PLN;
Konto Osobiste - 11112222333344445555;
#Data operacji;#Opis operacji;#Rachunek;#Kategoria;#Kwota;
2023-05-01;Zakupy w sklepie XYZ;11112222333344445555;Zakupy;-100,50 PLN;
2023-05-02;Wypłata z bankomatu;11112222333344445555;Wypłata;-200,00 PLN;
2023-05-03;Przelew od Jana Kowalskiego;11112222333344445555;Przychód;1500,75 PLN;
"""

def test_parse_header(parser):
    header = "Nazwa konta - Konto Osobiste;\nWaluta - PLN;\nKonto Osobiste - 11112222333344445555;\n"
    result = parser._parse_header(header)
    assert result == [Account(name="Konto Osobiste", number="11112222333344445555")]

def test_parse_single_operation(parser):
    raw_operation = '2023-05-01;Zakupy w sklepie XYZ;11112222333344445555;Zakupy;-100,50 PLN;'
    result = parser._parse_single_operation(raw_operation)
    assert result == Operation(
        operation_date=date(2023, 5, 1),
        operation_description="Zakupy w sklepie XYZ",
        account_number="11112222333344445555",
        operation_name="Zakupy",
        transaction_amount=-100.50,
        transaction_currency="PLN"
    )

def test_parse(parser, sample_csv_content):
    result = parser.parse(sample_csv_content)
    assert len(result) == 3
    assert result[0] == Operation(
        operation_date=date(2023, 5, 1),
        operation_description="Zakupy w sklepie XYZ",
        account_number="11112222333344445555",
        operation_name="Zakupy",
        transaction_amount=-100.50,
        transaction_currency="PLN"
    )
    assert result[1] == Operation(
        operation_date=date(2023, 5, 2),
        operation_description="Wypłata z bankomatu",
        account_number="11112222333344445555",
        operation_name="Wypłata",
        transaction_amount=-200.00,
        transaction_currency="PLN"
    )
    assert result[2] == Operation(
        operation_date=date(2023, 5, 3),
        operation_description="Przelew od Jana Kowalskiego",
        account_number="11112222333344445555",
        operation_name="Przychód",
        transaction_amount=1500.75,
        transaction_currency="PLN"
    )

def test_parse_empty_input(parser):
    with pytest.raises(ValueError):
        parser.parse("")

def test_parse_invalid_operation(parser):
    invalid_csv = """Nazwa konta - Konto Osobiste;
Waluta - PLN;
Konto Osobiste - 11112222333344445555;
#Data operacji;#Opis operacji;#Rachunek;#Kategoria;#Kwota;
2023-05-01;Invalid operation;
"""
    with pytest.raises(ValueError, match="Could not properly unpack operations."):
        parser.parse(invalid_csv)

def test_parse_with_redacted_account_number(parser):
    csv_with_redacted = """Nazwa konta - Konto Osobiste;
Waluta - PLN;
Konto Osobiste - 11112222333344445555;
#Data operacji;#Opis operacji;#Rachunek;#Kategoria;#Kwota;
2023-05-01;Zakupy w sklepie XYZ;"Konto Osobiste 1111 ... 5555";Zakupy;-100,50 PLN;
"""
    result = parser.parse(csv_with_redacted)
    assert result[0].account_number == "11112222333344445555"