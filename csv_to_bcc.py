#!/usr/bin/python3
"""
quickie (I hope!) based on earlier csv stuff. The goal is to
generate a bcc list of email addresses frm a csv file.
"""
import sys, os, csv, datetime

class Csv:
    @classmethod
    def absorb(cls, fn):
        with open(fn, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            field_names = csv_reader.__next__()
            attr_names = [('_' + name.lower().replace('-', '_')) for name in field_names]
            previous = None
            for row in csv_reader:
                if not row:
                    continue
                #print(', '.join(row))
                instance = cls()
                instance.previous = previous
                for an, av in zip(attr_names, row):
                    if not an:
                        continue
                    # print(an, ':', av)
                    instance.__setattr__(an, av)
                cls.postprocess(instance.intake())
                previous = instance

    @classmethod
    def postprocess(cls, instance):
        return

    @classmethod
    def main(cls, fn):
        cls.absorb(fn)

    def intake(self):
        return self

class CsvToBcc(Csv):
    bccList = []

    @classmethod
    def postprocess(cls, self):
        if not self._email:
            print("warning: no email address for '%s'" % self._name)
            return
        cls.bccList.append('<%s>%s' % (self._name, self._email))

    @classmethod
    def main(cls, fn):
        cls.absorb(fn)
        #print('Bcc:' + ','.join(cls.bccList))


class CsvToBccRuby(CsvToBcc):
    pass

if __name__ == '__main__':
    CsvToBccRuby.main('/home/gill/Vodawiko/ledenlijst01-01-2019-rest.csv')
