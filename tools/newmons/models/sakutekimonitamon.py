"""Sakuteki Monitamon (a Digimon of the CobbleEffort: Digital crossover; built after the tiny game sprite on
wikimon.net, its only picture): a scouting Monitamon in a dark camouflage-grey suit with a glowing green radar screen.
1 block. Child stage (no level on wikimon; by analogy with Monitamon). Monitamon's body with its own colours.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_M = clone("monitamon", "sakutekimonitamon",
           base={"olive": (80, 86, 96), "olive_dark": (34, 36, 44), "screen": (30, 90, 50), "screen_light": (120, 250, 150),
                 "orange": (90, 110, 60)},
           shiny={"olive": (170, 140, 90), "olive_dark": (100, 76, 40)})
HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a scouting Monitamon in a dark camouflage-grey suit with a glowing green radar screen"
build = _M.build
