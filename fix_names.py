#!/usr/bin/python3
"""
special script to fix up file names in a MEW archive sheet music directory
"""
import sys, os, time, random, signal

for old_name in os.listdir():
    nameless = old_name[16:]
    try:
        nameless = nameless[:nameless.index(' - 2023')]
    except ValueError:
        pass
    new_name = 'Et_maintenant-' + nameless.replace(' ', '_')+'.pdf'
    print( f"old_name:{old_name}  new_name:{new_name}")
    os.rename(old_name, new_name)