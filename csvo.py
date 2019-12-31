#!/usr/bin/python3
"""
"""
import csv
from util import as_python_name


class Csvo:
    @classmethod
    def absorb(cls, infn):
        cls.instances = []
        with open(infn, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            cls.field_names = csv_reader.__next__()
            # cls.python_names = [('_' + name.replace(' ', '_')) for name in cls.field_names]
            cls.python_names = [as_python_name(name) for name in cls.field_names]
            print (cls.python_names)
            previous = None
            for row in csv_reader:
                #print(', '.join(row))
                instance = cls()
                instance.previous = previous
                for an, av in zip(cls.python_names, row):
                    instance.__setattr__(an, av)
                previous, instance = instance, instance.intake()
                if not instance:
                    continue

                instance.postprocess()
                cls.instances.append(instance)
                previous = instance

    @classmethod
    def exude(cls, outfn):
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
    def main(cls, infn=None, outfn=None):
        if infn:
            cls.absorb(infn)
        if outfn:
            cls.exude(outfn)

if __name__ == '__main__':
    Csvo.main('new_rates.csv') # for ad hoc testing wih existing csv; may change soon!
