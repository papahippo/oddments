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

class CsvToBccVodawiko(Csv):

    csv_headers = [
"First Name",       "Last Name",            "Display Name",         "Nickname",
"Primary Email",    "Secondary Email",      "Screen Name",          "Work Phone",
"Home Phone",       "Fax Number",           "Pager Number",         "Mobile Number",
"Home Address",     "Home Address 2",       "Home City",            "Home County",
"Home Post Code",   "Home Country",         "Work Address",         "Work Address 2",
"Work City",        "Work County",          "Work Post Code",       "Work Country",
"Job Title",        "Department",           "Organisation",         "Web Page 1",
"Web Page 2",       "Birth Year",           "Birth Month",          "Birth Day",
"Custom 1",         "Custom 2",             "Custom 3",             "Custom 4",
"Notes",
    ]


    @classmethod
    def put_headers(cls):
        print(','.join(cls.csv_headers), file=cls.csvOut)

    @classmethod
    def main(cls, fn):
        with open('/home/gill/Vodawiko/Vodawiko_leden.csv', 'w') as cls.csvOut:
            cls.put_headers()
            cls.absorb(fn)

    @classmethod
    def postprocess(cls, self):
        if not self._email:
            print("warning: no email address for '%s'" % self._name)
        dob = self._dob
        blank = ''
        print(','.join([
#            "First Name", "Last Name", "Display Name", "Nickname",
             blank,         blank,      self._name,     blank,
#            "Primary Email", "Secondary Email", "Screen Name", "Work Phone",
             self._email,   blank,               blank,         blank,
#            "Home Phone", "Fax Number", "Pager Number", "Mobile Number",
             self._phone,   blank,        blank,         blank,
#            "Home Address", "Home Address 2", "Home City", "Home County",
             self._address,  blank,            self._gemeente, blank,
#            "Home Post Code", "Home Country", "Work Address", "Work Address 2",
             self._postcode, blank,            blank,           blank,
#            "Work City", "Work County", "Work Post Code", "Work Country",
             blank,       blank,         blank,            blank,
#            "Job Title", "Department", "Organisation", "Web Page 1",
             blank,       blank,        blank,          blank,
#            "Web Page 2", "Birth Year", "Birth Month", "Birth Day",
             blank,        '19'+ dob[-2:], dob[3:5],    dob[0:2],
#            "Custom 1", "Custom 2", "Custom 3", "Custom 4",
             blank,      blank,      blank,      blank,
#            "Notes",
             blank,
             ]),
              file=cls.csvOut)

class CsvToBccVodawiko2019(CsvToBccVodawiko):
    pass

if __name__ == '__main__':
    CsvToBccVodawiko2019().main('/home/gill/Vodawiko/ledenlijst01-01-2019-bare.csv')
