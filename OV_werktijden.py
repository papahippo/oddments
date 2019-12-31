#!/usr/bin/python3
"""
Deduce worked hours from csv downloaded from OV website.
This has been quickly reworked around the 'Csvo' (comma-separated values object) class.
If rewoking properly, I might try to use teh 'exude' and 'giveout' functions of class 'Csvo'.
"""
import sys, os, csv, datetime
from csvo import Csvo


class OvCsvo(Csvo):
    max_per_day = 8.0
    last_week_number = -1  # impossible
    held_over = 0.0
    period_cumulative = 0.0
    werkStations =  {}
    lunchMinutes = 30

    def intake(self):
        # print(self._Datum, end=' ... ')
        arriveMinutes = self.previous and self.werkStations.get(self.previous._Bestemming)
        departMinutes = self.werkStations.get(self._Vertrek)
        if not (
            (self.previous is not None)
            and arriveMinutes
            and (self.previous._Transactie == "Check-uit")
            and departMinutes
            and (self._Transactie == "Check-in")
        ):
            return None
        cls = self.__class__
        # print (self._Datum, self.previous._Check_uit, self._Check_in)
        self.datetime_out, datetime_back_in = [ datetime.datetime.strptime(date_s + '+' + time_s, '%d-%m-%Y+%H:%M')
                                           for date_s, time_s in ((self.previous._Datum, self.previous._Check_uit),
                                                                  (self._Datum, self._Check_in))]
        time_at_dest = datetime_back_in - self.datetime_out
        # print ("time at dest, arriveMinutes, departMinutes  =", time_at_dest, arriveMinutes, departMinutes)
        self.time_worked = time_at_dest - datetime.timedelta(minutes=(self.lunchMinutes + arriveMinutes + departMinutes))
        if self.time_worked <= datetime.timedelta():
            return None # quick fix for bug not looked at yet!
        this_week_number = self.datetime_out.isocalendar()[1]
        if cls.last_week_number != this_week_number:
            cls.cumulative_this_week = 0.0
            cls.last_week_number = this_week_number
            print ("------------"*4)
        hours_worked = self.time_worked.total_seconds() / 3600
        bookable_raw = hours_worked + cls.held_over
        bookable_smooth = min(bookable_raw - (bookable_raw % 0.25), cls.max_per_day)
        cls.held_over = bookable_raw - bookable_smooth
        print (self.datetime_out.strftime("%d-%m-%Y (%A)"), "time worked = %s = %.2f hours, bookable hours=%.2f" %
               (str(self.time_worked)[:-3], hours_worked, bookable_smooth))
        cls.cumulative_this_week += bookable_smooth
        cls.period_cumulative += bookable_smooth
        print ("week %d cumulative = %.2f hours , preiod cumulative = %.2f hours" %
               (this_week_number, cls.cumulative_this_week, cls.period_cumulative))
        return self

class OvCsvoUltimaker(OvCsvo):
    werkStations =  {"Geldermalsen": 10, "'s-Hertogenbosch": 34}


if __name__ == '__main__':
    OvCsvoUltimaker.main('/home/gill/Hippos/_2018/Acco2018/Q4/transacties_18122018213743.csv')
