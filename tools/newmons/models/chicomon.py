"""Chicomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a glossy pale blue blob baby with big black eyes, a small smile and one swept tuft. Baby I.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

from _blobbaby import make
from _digi import sized

HEIGHT = 18
SCALE, HITBOX = sized(0.35, HEIGHT, 0.5)
KIND = "floater"
K = 4
LOOK = "a glossy pale blue blob baby with big black eyes, a small smile and one swept tuft"
BASE = {'body': (150, 200, 250), 'body_dark': (80, 140, 220), 'body_light': (220, 240, 255), 'eye': (20, 20, 24), 'white': (255, 255, 255), 'blush': (250, 150, 170)}
SHINY = {'body': (250, 200, 120), 'body_dark': (220, 140, 60), 'body_light': (255, 236, 190)}

build = make("chicomon", BASE, SHINY, tuft=True)
