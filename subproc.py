#!/usr/bin/python3
"""
experimenting with subprocess module s alternative to ubiquitous (in my work!) os.system
"""
import os, subprocess
subprocess.run(('/usr/bin/touch', "funny'file"))
os.system('ls')

output = subprocess.check_output(('echo', 'hello world!'))
print("output was:", output )
with open("output.txt", 'wb') as out:
    out.write(output)
os.system("cat output.txt")

# ... so it seems that by using subprocess without a shell, I remove teh need to sue 'shlex.quote'
# to cater for quotes  (e.g. apostrophes) within filenames!
