"""Examon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Examon awakened by the X-Antibody, its knight form standing upright in silver and gold armour studded with red jewels, red membrane wings, a green light blade and a blazing blue core.
35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from _digi import sized
from _examon import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "an upright silver-and-gold dragon knight with red jewels, red membrane wings, a green light blade and a blazing blue core"
build = make("examonxantibody", x=True)
