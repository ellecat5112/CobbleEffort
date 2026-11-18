"""Medieval Dukemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the dark-age knight version of Dukemon: the Royal Knight's build in blackened armour with
red trim and gold edges, a long red cape, and its lance and shield. 35 blocks tall. A recoloured copy of the Dukemon
builder (_variant.clone).

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_D = clone("_dukemon", "medievaldukemon",
           base={"white": (70, 70, 84), "white_dark": (24, 24, 32), "white_light": (140, 140, 160), "silver": (150, 154, 166),
                 "silver_dark": (60, 64, 76), "teal": (90, 240, 120, 220)},
           shiny={"white": (240, 230, 200), "white_dark": (180, 160, 120), "red": (40, 60, 160)})
HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a Royal Knight in blackened armour with red trim and gold edges, a long red cape, a lance and a shield"
build = _D.make("medievaldukemon")
