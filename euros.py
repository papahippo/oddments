#!/usr/bin/python3
"""
"""
import money
class Euros(money.Money):
    def __init__(self, amount='0', currency='EUR'):
        super().__init__(amount=amount, currency=currency)

def main():
    print(Euros(2.426).format())

if __name__ == '__main__':
    main()