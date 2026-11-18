"""Megalo Growmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): Megalo Growmon awakened by the X-Antibody: a lean red cyborg dinosaur with a pale ridged belly, a white mane, silver armour, twin back cannons and long blades. 25 blocks tall. Built by _guilmon.make(stage="perfect").

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
LOOK = "a lean red cyborg dinosaur with a pale ridged belly, a white mane, silver armour, twin back cannons and long blades"
build = make("megalogrowmonxantibody", "perfect", colours={'hide': (220, 60, 30), 'hide_dark': (140, 24, 10), 'hide_light': (255, 150, 110), 'belly': (240, 226, 214)}, shiny_colours={'hide': (60, 58, 66)})
