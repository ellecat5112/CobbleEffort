"""Duramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
living holy sword, a lean golden knight whose arms, crest and shoulders are flared golden blades, a slit-visored
helm, blade-legs ending in golden talons and a huge golden broadsword, with a sweep of blue light round it. 25 blocks
tall.

Front is -z, y is up. 70 units tall; Perfect stage.
"""
from _digi import sized
from _duramon import make

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a lean golden blade knight with flared blade shoulders and crest, golden talons, a huge golden broadsword and a "
        "sweep of blue light")
build = make("duramon")
