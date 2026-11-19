"""Waru Seadramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Seadramon's wicked kin: a long coiling grey-white sea serpent banded with dark zigzags, a black
armoured head with a golden horn crest and blue eyes, and a ruff of crimson fin spines down its back. 25 blocks.

Front is -z, y is up. Perfect stage. Built by _seadramon.make(x=True), recoloured.
"""
from __future__ import annotations

from _digi import sized
from _seadramon import make

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a long coiling grey-white sea serpent with a black armoured head, a golden horn crest and crimson fin spines"
build = make("waruseadramon", x=True,
             colours={"teal": (200, 200, 210), "teal_dark": (70, 70, 84), "belly": (236, 236, 240), "red": (200, 30, 50),
                      "gold": (50, 50, 60), "gold_dark": (16, 16, 22), "eye": (60, 140, 240)},
             shiny_colours={"teal": (230, 190, 120), "teal_dark": (150, 110, 50)})
