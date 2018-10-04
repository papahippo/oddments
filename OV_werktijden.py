#!/usr/bin/python3
"""
Deduce worked hours from csv downloaded from OV website.
Work in progress!
"""
import sys, os, csv, datetime

class Csv:
    def absorb(cls, fn):
        print (cls)
        with open(fn, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            field_names = csv_reader.__next__()
            attr_names = [('_' + name.lower().replace('-', '_')) for name in field_names]
            previous = None
            for row in csv_reader:
                #print(', '.join(row))
                instance = cls()
                instance.previous = previous
                for an, av in zip(attr_names, row):
                    instance.__setattr__(an, av)
                instance.intake()
                previous = instance
    absorb = classmethod(absorb)

    def main(cls, fn):
        cls.absorb(fn)
    main = classmethod(main)

    def intake(self):
        print("what!?", self._datum, end=' ... ')


class OvCsv(Csv):

    def intake(self):
        # print(self._datum, end=' ... ')
        if not (
            (self.previous is not None)
            and (self.previous._bestemming == self.werkLocatie)
            and (self.previous._transactie == "Check-uit")
            and (self._vertrek == self.werkLocatie)
            and (self._transactie == "Check-in")
        ):
            return None
        print (self._datum, self.previous._check_uit, self._check_in)
        datetime_out = datetime.datetime.strptime(self.previous._datum + '+' + self.previous._check_uit,
                                                  '%d-%m-%Y+%H:%M')

class OVcsvOct2018(OvCsv):
    werkLocatie = "Geldermalsen"


if __name__ == '__main__':
    OVcsvOct2018.main('/home/gill/Hippos/_2018/Acco2018/Q3/transacties_04102018123951.csv')
