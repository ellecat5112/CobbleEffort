"""Chronomon: Holy Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the god of time in its holy form: a white bird-god in a robe painted with a red sun, a masked face with a red crest, striped trousers and enormous wings of white paper strips. 35 blocks tall.

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
LOOK = "the god of time in its holy form: a white bird-god in a robe painted with a red sun, a masked face with a red crest, striped trousers and enormous wings of white paper strips"

build = make("chronomonholymode", holy=True)
