#!/usr/bin/python3
"""
Deduce worked hours from csv downloaded from OV website.
Work in progress!
"""
import sys, os, csv, datetime

class Csv:
    def absorb(cls, fn):
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
                cls.postprocess(instance.intake())
                previous = instance
    absorb = classmethod(absorb)

    def postprocess(cls, instance):
        return
    postprocess = classmethod(postprocess)

    def main(cls, fn):
        cls.absorb(fn)
    main = classmethod(main)

    def intake(self):
        print("what!?", self._datum, end=' ... ')


class OvCsv(Csv):
    last_week_number = -1  # impossible

    def postprocess(cls, instance):
        if not instance:
            return
        this_week_number = instance.datetime_out.isocalendar()[1]
        if cls.last_week_number != this_week_number:
            cls.cumulative_this_week = datetime.timedelta()
            cls.last_week_number = this_week_number
            print ("------------"*4)
        print (instance.datetime_out.strftime("%d-%m-%Y (%A)"), "time worked = %s = %.1f hours" %
               (str(instance.time_worked)[:-3], instance.time_worked.total_seconds() / 3600))
        cls.cumulative_this_week = cls.cumulative_this_week + instance.time_worked
        print ("week %d cumulative = %s = %.1f hours" % (this_week_number, str(cls.cumulative_this_week)[:-3],
                                                         cls.cumulative_this_week.total_seconds() / 3600))
    postprocess = classmethod(postprocess)


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
        # print (self._datum, self.previous._check_uit, self._check_in)
        self.datetime_out, datetime_back_in = [ datetime.datetime.strptime(date_s + '+' + time_s, '%d-%m-%Y+%H:%M')
                                           for date_s, time_s in ((self.previous._datum, self.previous._check_uit),
                                                                  (self._datum, self._check_in))]
        time_at_dest = datetime_back_in - self.datetime_out
        #print ("time at dest =", time_at_dest)
        self.time_worked = time_at_dest - datetime.timedelta(minutes=50)
        if self.time_worked <= datetime.timedelta():
            return None # quick fix for bug not looked at yet!
        return self

class OVcsvOct2018(OvCsv):
    werkLocatie = "Geldermalsen"


if __name__ == '__main__':
    OVcsvOct2018.main('/home/gill/Hippos/_2018/Acco2018/Q3/transacties_04102018123951.csv')
