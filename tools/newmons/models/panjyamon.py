"""Panjyamon (a Digimon of the CobbleEffort: Digital crossover; after the official art on wikimon.net): the snow lion warrior: a muscular white-furred lion-man with a shaggy pale mane, dark green trousers, a leather belt with a pouch and big clawed feet.
25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage. Leomon's body (_leomon.make) with its own colours.
"""
from _digi import sized
from _variant import clone

_L = clone("_leomon", "panjyamon",
           base={"tan": (236, 240, 250), "tan_dark": (170, 180, 210), "tan_light": (255, 255, 255),
                 "mane": (220, 226, 240), "mane_dark": (150, 160, 190), "black": (60, 80, 60), "black_dark": (24, 34, 24),
                 "plate": (80, 110, 190), "plate_dark": (30, 50, 120)},
           shiny={"tan": (240, 220, 160), "mane": (240, 200, 120), "mane_dark": (180, 130, 50)})
HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "the snow lion warrior: a muscular white-furred lion-man with a shaggy pale mane, dark green trousers, a leather belt with a pouch and big clawed feet"
build = _L.make("panjyamon", x=False)
