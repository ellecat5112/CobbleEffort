"""Gold Numemon (Ultimate) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): a Numemon of shining gold flying on great golden feathered wings, with bloodshot eyes on stalks, a huge
mouth of big square teeth, a lolling tongue and a pearl necklace. Ultimate stage, 35 blocks tall.

Front is -z, y is up. 36 units tall. Built by _numemon.make("gold", wings=True).
"""
from __future__ import annotations

from _digi import sized
from _numemon import make

HEIGHT = 36
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "a golden Numemon flying on great golden feathered wings, with eyes on stalks, a huge toothy mouth and a pearl necklace"
build = make("goldnumemonultimate", "gold", wings=True, shiny_look={"slime": (210, 214, 226), "slime_dark": (120, 124, 138),
                                                   "slime_light": (250, 250, 255), "spot": (150, 150, 170),
                                                   "gold": (220, 224, 236), "gold_dark": (130, 134, 146)})
