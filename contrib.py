#!/usr/bin/python3
"""
"""
import csvo
from euros import Euros as Money
from decimal import Decimal, InvalidOperation
from babel.numbers import parse_decimal


class ContribCsvo(csvo.Csvo):

    perCentIncrease = 10

    def postprocess(self):
        if not self._Jaar:
            return
        try:
            jaarGeld = Money(parse_decimal(self._Jaar.replace('€','')))
        except InvalidOperation:
            return
        jaarGeld *= Decimal((100 + self.perCentIncrease)/100)
        kwartaalGeld = jaarGeld / 4
        maandGeld = kwartaalGeld / 3

        self._Jaar = jaarGeld.format()
        self._Kwartaal = kwartaalGeld.format()
        self._Maand = maandGeld.format()

    def intake(self):
        return self


if __name__ == '__main__':
    ContribCsvo().main('old_rates.csv', 'new_rates.csv')
