"""Cocomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a glossy tan blob baby with two little horns, a long tapering tail, big black eyes and a small smile. Baby I.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

from _blobbaby import make
from _digi import sized

HEIGHT = 18
SCALE, HITBOX = sized(0.35, HEIGHT, 0.5)
KIND = "floater"
K = 4
LOOK = "a glossy tan blob baby with two little horns, a long tapering tail, big black eyes and a small smile"
BASE = {'body': (200, 160, 130), 'body_dark': (140, 100, 70), 'body_light': (240, 210, 190), 'eye': (20, 20, 24), 'white': (255, 255, 255), 'blush': (250, 150, 170)}
SHINY = {'body': (170, 210, 160), 'body_dark': (110, 160, 100), 'body_light': (220, 245, 210)}

build = make("cocomon", BASE, SHINY, horns=True, tail=True)
