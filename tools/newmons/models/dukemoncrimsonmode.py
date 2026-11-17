"""Dukemon: Crimson Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Dukemon in Crimson Mode, its armour turned red and gold, with a lance and shield of white light and ten white feathered wings of light.
35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from _digi import sized
from _dukemon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a red-and-gold armoured knight with a lance and shield of white light and ten white feathered wings"
build = make("dukemoncrimsonmode", "crimson")
