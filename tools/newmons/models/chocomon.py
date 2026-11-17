"""Chocomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a glossy brown blob baby with two little horns, floppy ears, big black eyes and a small smile. Baby II.

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

from _blobbaby import make
from _digi import sized

HEIGHT = 20
SCALE, HITBOX = sized(0.5, HEIGHT, 0.5)
KIND = "floater"
K = 4
LOOK = "a glossy brown blob baby with two little horns, floppy ears, big black eyes and a small smile"
BASE = {'body': (190, 140, 100), 'body_dark': (130, 90, 60), 'body_light': (230, 200, 170), 'eye': (20, 20, 24), 'white': (255, 255, 255), 'blush': (250, 150, 170)}
SHINY = {'body': (240, 200, 220), 'body_dark': (200, 150, 180), 'body_light': (255, 236, 244)}

build = make("chocomon", BASE, SHINY, horns=True, ears=True)
