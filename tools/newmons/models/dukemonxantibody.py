"""Dukemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Dukemon awakened by the X-Antibody, sleeker armour edged in teal, a spray of crimson crest blades, a glowing teal crystal lance and a sun-ringed shield with a great blue jewel.
35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from _digi import sized
from _dukemon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a sleek white-and-crimson knight with crimson crest blades, a crimson cape, a glowing teal lance and a sun-ringed blue jewel shield"
build = make("dukemonxantibody", "x")
