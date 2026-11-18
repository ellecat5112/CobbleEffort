"""Greymon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): Greymon awakened by the X-Antibody: a golden-yellow tyrant with blue stripes, a cream belly, a brown helmet with long white horns and silver claws.
The Agumon line's Greymon body with its own colours (_greyvar.make). Adult stage, 15 blocks tall.

Front is -z, y is up. 41 units tall; baseScale 6.0 like Greymon.
"""
from __future__ import annotations

from _greyvar import make

SCALE = 6.0
HITBOX = [1.6, 2.55]
KIND = "biped"
K = 3
HEIGHT = 41
ANIM = {"leg_amp": 14}
LOOK = "Greymon awakened by the X-Antibody: a golden-yellow tyrant with blue stripes, a cream belly, a brown helmet with long white horns and silver claws"
build = make("greymonxantibody", base={'orange': (240, 190, 50), 'orange_dark': (190, 140, 20), 'belly': (250, 236, 190), 'stripe': (60, 150, 210), 'helmet': (130, 70, 50), 'helmet_dark': (80, 40, 24), 'horn': (240, 240, 236), 'horn_tip': (255, 255, 255), 'claw': (220, 224, 234)}, shiny={'orange': (160, 160, 170), 'orange_dark': (100, 100, 110)})
