"""Dukemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the crimson Royal Knight, in white armour with crimson plates, a crested helm with trailing antennae, a long crimson cape, the lance Gram and the great round shield Aegis.
35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from _digi import sized
from _dukemon import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a white-and-crimson armoured knight with a crested helm, a long crimson cape, a silver cone lance and a great round silver shield"
build = make("dukemon")
