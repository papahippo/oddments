#!/usr/bin/env python3
import inspect
print ("so far so good!")


class Aware:
    def __init__(self, *pp):
        # print ( inspect.getsourcelines(self))
        top = inspect.getouterframes(inspect.currentframe())[-1]
        print (*pp, top.code_context)
        print (top.lineno)


print ("the first...")
aw1 = Aware(42,
            54,
            99)

print ("the second...")

Aware(
    142, 156,
    167
)
