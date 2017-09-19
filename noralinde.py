#!/usr/bin/env python3
"""
'Game' to help learning of drama texts.
"""
import random
class Play:
    texts = [('first test cue', 'first test answer'),
            ('second test cue', 'second test answer'),]

    def quiz(self):
        random.seed()
        prev_ix = -1
        while 1:
            ix = random.randrange(len(self.texts))
            if ix == prev_ix:
                continue
            prev_ix = ix
            cue, text = self.texts[ix]
            s = input("(%u.) %s" %(ix, cue))
            if s=='q':
                break
            print("%s" %(text))

class Noraline(Play):
    texts = [("WACHT, JAN!", """
Ron? Klaas? Wat doen jullie hier?
                """),
             ("door de tranen heen zei hij:","""
Ik moet de hele tijd alles stelen.
                """),
             ("Waarom moet je alles stelen?", """"
Ik kan niet anders. Ooit was ik vingervlug op de toetsen van mijn trompet.
Maar sinds het verbod op muziek weet ik mij geen raad met die vingervlugheid.
Mijn vingers doen wat ze zelf willen. Ik moet stelen.
                """),
             ("Jullie moeten alle drie met ons mee terug naar Noralinde.", """"
Waarom zouden we? Straks worden we onthoofd?
                                          """),
             ("IK WIL NIET LANGER WOEST ZIJN.", """"
En ik ben moe van het alsmaar moeten stelen.
               """),
             ("DRIE HOOFDEN WORDEN AFGEHAKT VANDAAG! SCHULDIG! SCHULDIG! SCHULDIG!", """"
[Jan, Ron, Klaas:] Dick!
               """),
             ]

Noraline().quiz()
