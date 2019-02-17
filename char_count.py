#!/usr/bin/python3

s = "my test string with some repeats"

dickie = {}
for c in s:
    dickie[c] = 1 + dickie.setdefault(c, 0)

print(dickie) # A simple print of a dictionary object gives quite useful output

for key, val in sorted(dickie.items()):
    print ("'%c' (%s) occurs %d time(s)" % (key, hex(ord(key)), val))
