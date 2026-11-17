"""Durandamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
holy sword perfected, a slim black-and-gold sword knight with glowing rose eyes, a crown of curved blade horns, a
golden lance-sword taller than itself and a great ring of blue light circling it. 35 blocks tall.

Front is -z, y is up. 86 units tall; Ultimate stage.
"""
from _digi import sized
from _duramon import make

HEIGHT = 86
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a slim black-and-gold sword knight with rose eyes, a crown of curved blade horns, a towering golden lance-sword "
        "and a great ring of blue light")
build = make("durandamon", durandal=True)
