"""Gulus Gammamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Gammamon grown into a lean, upright black dragon-man traced with magenta, a long horn
and swept horns tipped red, a ragged blue cloak-scarf streaming behind it, red bands, violet claws and a blue-flamed
tail. Adult stage, 15 blocks tall.

Front is -z, y is up. 64 units tall. Built by _gammamon.make(stage="adult") with its own colours.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_G = clone("_gammamon", "gulusgammamon",
           base={"white": (40, 36, 48), "white_dark": (14, 12, 18), "red": (230, 50, 150), "horn": (200, 200, 210)},
           shiny={"white": (236, 236, 244), "white_dark": (170, 172, 190)})
HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean upright black dragon-man traced with magenta, long horns, a streaming blue scarf, violet claws and a blue-flamed tail"
build = _G.make("gulusgammamon", "adult")
