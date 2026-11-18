"""Gallantmon Chaos Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official toy shown
on wikimon.net): Chaos Dukemon's toy-only mode: a knight in deep blue armour with silver plates, a long translucent
blue lance, a white shield and ten translucent blue wings. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built on _dukemon.make(look="crimson") with its own colours.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_D = clone("_dukemon", "gallantmonchaosmode",
           base={"red": (40, 70, 200), "red_dark": (14, 26, 110), "red_light": (120, 160, 250),
                 "gold": (210, 214, 226), "gold_dark": (110, 114, 128), "light": (110, 170, 255, 170)},
           shiny={"red": (60, 60, 70), "red_dark": (20, 20, 26), "red_light": (130, 130, 150),
                  "light": (200, 60, 70, 170)})
HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a knight in deep blue armour with silver plates, a long translucent blue lance and ten translucent blue wings"
build = _D.make("gallantmonchaosmode", "crimson")
