#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This was an incubator for a technique that I have since integrated into project:
git@github.com:papahippo/phileas.git (sub-package phileas.admin.entity).
"""
import eyeD3

class Aware:
    prev_lineno = -1

    def __init__(self, *pp):
        # print ( inspect.getsourcelines(self))
        last_lineno = inspect.getouterframes(inspect.currentframe())[-1].lineno
        self.lineno_range = (Aware.prev_lineno+1, last_lineno + 1)
        Aware.prev_lineno = last_lineno


if __name__ == "__main__":
    # class 'Aware' is probably best used as a mix-in, but for this example,
    # let's keep it simple.

    aw1 = Aware(42,
                54,
                99)

    aw2 = Aware(
        142, 156,
        167
    )
    print ([aw.lineno_range for aw in (aw1, aw2)])
