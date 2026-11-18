"""Megalo Growmon (Orange) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): an orange cyborg dinosaur with black markings, a white mane, silver cyborg armour, a chest cannon, twin back cannons and long silver arm blades. 25 blocks tall. Built by _guilmon.make(stage="perfect").

Front is -z, y is up. 52 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _guilmon import make

HEIGHT = 52
SCALE, HITBOX = sized(25, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "an orange cyborg dinosaur with black markings, a white mane, silver cyborg armour, a chest cannon, twin back cannons and long silver arm blades"
build = make("megalogrowmonorange", "perfect", colours={'hide': (240, 160, 40), 'hide_dark': (180, 100, 14), 'hide_light': (255, 210, 120), 'mark': (40, 30, 24)}, shiny_colours={'hide': (60, 58, 66), 'hide_dark': (24, 22, 28)})
