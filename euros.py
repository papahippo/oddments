#!/usr/bin/python3
"""
"""
import money
from decimal import Decimal, InvalidOperation
from babel.numbers import parse_decimal


class Euros(money.Money):
    def __init__(self, amount='0', currency='EUR'):
        if isinstance(amount, str) and amount[:1]=='€':
            amount = parse_decimal(amount[1:])
        super().__init__(amount=amount, currency=currency)

def main():
    answer = Euros('€001.234,5678').format()
    print(f"Euros('€001.234,5678').format() gives answer '{answer}'")
    assert (answer == '€ 1.234,57')

if __name__ == '__main__':
    main()