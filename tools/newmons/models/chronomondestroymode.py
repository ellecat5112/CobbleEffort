"""Chronomon: Destroy Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the god of time in its destroying form: a crimson demon-dragon god with a black sun disc on its chest, huge red clawed hands, a crown of violet spines and vast black blade-wings lined with glowing lights. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _chronomon import make
from _digi import sized

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the god of time in its destroying form: a crimson demon-dragon god with a black sun disc on its chest, huge red clawed hands, a crown of violet spines and vast black blade-wings lined with glowing lights"

build = make("chronomondestroymode", holy=False)
