"""Platinum Numemon (a Digimon of the CobbleEffort: Digital crossover; after the official art on wikimon.net): a
platinum-silver Numemon flying on great golden feathered wings, with eyes on stalks, a huge gaping mouth of square
teeth, a lolling tongue and a pearl necklace. 35 blocks tall.

Front is -z, y is up. 36 units tall; Ultimate stage. Built by _numemon.make(look="platinum", wings=True).
"""
from _digi import sized
from _numemon import make

HEIGHT = 36
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "a platinum-silver Numemon on great golden feathered wings, with eyes on stalks, a huge toothy mouth and a pearl necklace"
build = make("platinumnumemon", "platinum", wings=True, shiny_look={"slime": (240, 200, 120), "slime_dark": (170, 130, 50),
                                                           "slime_light": (255, 240, 190), "spot": (200, 160, 80)})
