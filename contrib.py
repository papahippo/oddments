#!/usr/bin/python3
"""
"""
import sys, os, csv, datetime

class Money_:
    currency_sign = '#'
    thousands_sep = ','
    cents_sep = '.'

    def __init__(self, s):
        if isinstance(s, (float, int)):
            self.as_cents = int(s*1000)
        else:
            s_bare = s[1:].strip()
            s_thousands, s_rest = ('0' + self.thousands_sep + s_bare).split(self.thousands_sep)[-2:]
            print (s_bare, '->', s_thousands, s_rest)
            s_whole ,s_frac = (s_rest + self.cents_sep + '00').split(self.cents_sep)[:2]
            self.as_cents = (int(s_thousands)*1000 + int(s_whole))*100 + int(s_frac)
            #print (self.as_cents)

    def __str__(self):
        s = str(self.as_cents)
        # not dealing with thousands yet!
        return self.currency_sign + s[:-2] + self.cents_sep + s[-2:]

class Euros(Money_):
    currency_sign = '€'
    thousands_sep = '.'
    cents_sep = ','

Money = Euros

class Csv:
    @classmethod
    def absorb(cls, infn):
        cls.instances = []
        with open(infn, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            cls.field_names = csv_reader.__next__()
            # attr_names = [('_' + name.lower().replace('-', '_')) for name in field_names]
            cls.python_names = [('_' + name.replace(' ', '_')) for name in cls.field_names]
            previous = None
            for row in csv_reader:
                #print(', '.join(row))
                instance = cls()
                instance.previous = previous
                for an, av in zip(cls.python_names, row):
                    instance.__setattr__(an, av)
                instance = instance.intake()
                if not instance:
                    continue

                instance.postprocess()
                cls.instances.append(instance)
                previous = instance

    @classmethod
    def exude(cls, outfn):
        if not outfn:
            return
        with open(outfn, 'w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=';')
            csv_writer.writerow(cls.field_names)
            # print(cls.instances)
            for inst in cls.instances:
                inst.giveout(csv_writer)

    def intake(self):
        return self

    def giveout(self, csv_writer):
        print('giveout', self.python_names)
        csv_writer.writerow([str(getattr(self, name)) for name in self.python_names])

    def postprocess(self):
        return


    @classmethod
    def main(cls, infn, outfn=None):
        cls.absorb(infn)
        cls.exude(outfn)

class ContribCsv(Csv):

    perCentIncrease = 10

    def postprocess(self):
        #for finame, pyname in zip(self.field_names, self.python_names):
        #    print(finame, pyname)
        for pyname in self.python_names:
            s = getattr(self, pyname)
            print(pyname, s)
            try:
                money = Money(s)
            except ValueError:
                continue
            #print(money.as_cents)
            money.as_cents *= (100 + self.perCentIncrease)
            money.as_cents //= 100
            print(money.as_cents, '-->', money)
            setattr(self, pyname, str(money))

    def intake(self):
        return self


if __name__ == '__main__':
    ContribCsv.main('old_rates.csv', 'new_rates.csv')
