#!/usr/bin/python3
"""
"""
import csv
class Money_:
    """
This Money class is not fully implemented. The package you get by 'pip install money' is quite possibly better but I
couldn't get it to "behave" as I wanted.
    """
    currency_sign = '#'
    thousands_sep = ','
    cents_sep = '.'

    def __init__(self, s):
        if isinstance(s, (float, int)):
            self.as_cents = s*100.
        else:
            s_bare = s[1:].strip()
            s_thousands, s_rest = ('0' + self.thousands_sep + s_bare).split(self.thousands_sep)[-2:]
            #print (s_bare, '->', s_thousands, s_rest)
            s_whole ,s_frac = (s_rest + self.cents_sep + '00').split(self.cents_sep)[:2]
            self.as_cents = (int(s_thousands)*1000. + int(s_whole))*100. + int(s_frac[:2])

    def __str__(self):
        s = str(round(self.as_cents))
        # not dealing with thousands yet!
        print(self.as_cents, '->', s)
        return self.currency_sign + s[:-2] + self.cents_sep + s[-2:]

    def __iadd__(self, other):
        self.as_cents += other*100.
        return self

    def __isub__(self, other):
        self.as_cents -= other*100.
        return self

    def __imul__(self, other):
        self.as_cents *= other
        return self

    def __mul__(self, other):
        return Money((self.as_cents*other)/100.0)

    def __truediv__(self, other):
        return Money(self.as_cents/(other*100.0))


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
        csv_writer.writerow([getattr(self, name) for name in self.python_names])

    def postprocess(self):
        return


    @classmethod
    def main(cls, infn, outfn=None):
        cls.absorb(infn)
        cls.exude(outfn)

class ContribCsv(Csv):

    perCentIncrease = 10

    def postprocess(self):
        try:
            jaarGeld = Money(self._Jaar)
        except ValueError:
            return
        jaarGeld *= ((100 + self.perCentIncrease)/100)
        jaarGeld -= 0.005
        kwartaalGeld = jaarGeld / 4
        kwartaalGeld += 0.003  # this is a real fudge; .005 is logical but gives wrong looking output!
        maandGeld = kwartaalGeld / 3
        maandGeld += 0.003  # this is a real fudge; .005 is logical but gives wrong looking output!

        self._Jaar = str(jaarGeld)
        self._Kwartaal = str(kwartaalGeld)
        self._Maand = str(maandGeld)

    def intake(self):
        return self


if __name__ == '__main__':
    ContribCsv.main('old_rates.csv', 'new_rates.csv')
