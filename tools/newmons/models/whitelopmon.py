"""White Lopmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): a snow-white Lopmon: a small round white rabbit with a tiny horn, blue eyes, a cream belly and two huge
long white ears that sweep out like wings and split into three fingers at the tips. 1 block.

Front is -z, y is up. Child stage. Built by _lopmon.make, recoloured.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_L = clone("_lopmon", "whitelopmon",
           base={"brown": (248, 248, 252), "brown_dark": (200, 204, 220), "pink": (230, 236, 250),
                 "pink_dark": (180, 190, 220), "eye": (70, 130, 220), "horn": (250, 250, 250)},
           shiny={"brown": (250, 230, 200), "brown_dark": (210, 180, 140)})
HEIGHT = 16
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a snow-white round rabbit with a tiny horn, blue eyes and two huge long white ears that sweep out like wings"
build = _L.make("whitelopmon", x=False)
