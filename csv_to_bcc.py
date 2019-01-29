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

    csv_headers = (
"First Name,Last Name,Display Name,Nickname,Primary Email,Secondary Email,Screen Name,"
"Work Phone,Home Phone,Fax Number,Pager Number,Mobile Number,"
"Home Address,Home Address 2,Home City,Home County,Home Post Code,Home Country,"
"Work Address,Work Address 2,Work City,Work County,Work Post Code,Work Country,"
"Job Title,Department,Organisation,Web Page 1,Web Page 2,"
"Birth Year,Birth Month,Birth Day,Custom 1,Custom 2,Custom 3,Custom 4,Notes,"
    )


    @classmethod
    def put_headers(cls):
        pass
    @classmethod
    def main(cls, fn):
        with open('/home/gill/Vodawiko/Vodawiko_leden.csv', 'w') as cls.csvOut:
            print(cls.csv_headers, file=cls.csvOut)
            cls.absorb(fn)

    @classmethod
    def postprocess(cls, self):
        if not self._email:
            print("warning: no email address for '%s'" % self._name)
        dob = self._dob
        print(','*2 + self._name + ','*2 + self._email + ','*4 + self._phone + ','*4
              + self._address +','*2 + ','+ self._gemeente + ','*2 + self._postcode  +
              ','*12 + '19'+ dob[-2:] + ',' + dob[3:5] + ',' + dob[0:2] + ','*5,
              file=cls.csvOut)

class CsvToBccVodawiko2019(CsvToBccVodawiko):
    pass

if __name__ == '__main__':
    CsvToBccVodawiko2019().main('/home/gill/Vodawiko/ledenlijst01-01-2019-bare.csv')
