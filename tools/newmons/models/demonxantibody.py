"""Demon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Demon awakened by the X-Antibody, hulking in crimson crystal armour with giant crystal claws, red horns, violet bat wings and a burning golden ring of flame behind its head.
35 blocks tall.

Front is -z, y is up. 72 units tall; Ultimate stage.
"""
from _digi import sized
from _demon import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking demon in crimson crystal armour with giant crystal claws, red horns, violet bat wings and a golden flame ring"
build = make("demonxantibody", "x")
