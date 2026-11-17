"""Erlangmon: Blast Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Erlangmon in Blast Mode, sleek in violet and white armour with a gold crescent halo, long flowing pale-blue ribbon-hair and a towering crystal trident.
35 blocks tall.

Front is -z, y is up. 68 units tall; Ultimate stage.
"""
from _digi import sized
from _erlangmon import make

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a sleek violet-and-white armoured warrior with a gold crescent halo, flowing pale-blue ribbon-hair and a towering crystal trident"
build = make("erlangmonblastmode", blast=True)
