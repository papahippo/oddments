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
    max_per_day = 8.0
    last_week_number = -1  # impossible
    held_over = 0.0
    period_cumulative = 0.0
    werkStations =  {}
    lunchMinutes = 30

    def postprocess(cls, instance):
        if not instance:
            return
        this_week_number = instance.datetime_out.isocalendar()[1]
        if cls.last_week_number != this_week_number:
            cls.cumulative_this_week = 0.0
            cls.last_week_number = this_week_number
            print ("------------"*4)
        hours_worked = instance.time_worked.total_seconds() / 3600
        bookable_raw = hours_worked + cls.held_over
        bookable_smooth = min(bookable_raw - (bookable_raw % 0.25), cls.max_per_day)
        cls.held_over = bookable_raw - bookable_smooth
        print (instance.datetime_out.strftime("%d-%m-%Y (%A)"), "time worked = %s = %.2f hours, bookable hours=%.2f" %
               (str(instance.time_worked)[:-3], hours_worked, bookable_smooth))
        cls.cumulative_this_week += bookable_smooth
        cls.period_cumulative += bookable_smooth
        print ("week %d cumulative = %.2f hours , preiod cumulative = %.2f hours" %
               (this_week_number, cls.cumulative_this_week, cls.period_cumulative))
    postprocess = classmethod(postprocess)


    def intake(self):
        # print(self._datum, end=' ... ')
        arriveMinutes = self.previous and self.werkStations.get(self.previous._bestemming)
        departMinutes = self.werkStations.get(self._vertrek)
        if not (
            (self.previous is not None)
            and arriveMinutes
            and (self.previous._transactie == "Check-uit")
            and departMinutes
            and (self._transactie == "Check-in")
        ):
            return None
        # print (self._datum, self.previous._check_uit, self._check_in)
        self.datetime_out, datetime_back_in = [ datetime.datetime.strptime(date_s + '+' + time_s, '%d-%m-%Y+%H:%M')
                                           for date_s, time_s in ((self.previous._datum, self.previous._check_uit),
                                                                  (self._datum, self._check_in))]
        time_at_dest = datetime_back_in - self.datetime_out
        # print ("time at dest, arriveMinutes, departMinutes  =", time_at_dest, arriveMinutes, departMinutes)
        self.time_worked = time_at_dest - datetime.timedelta(minutes=(self.lunchMinutes + arriveMinutes + departMinutes))
        if self.time_worked <= datetime.timedelta():
            return None # quick fix for bug not looked at yet!
        return self

class OVcsvDec2018(OvCsv):
    werkStations =  {"Geldermalsen": 10, "'s-Hertogenbosch": 34}


if __name__ == '__main__':
    OVcsvDec2018.main('/home/gill/Hippos/_2018/Acco2018/Q4/transacties_18122018213743.csv')
