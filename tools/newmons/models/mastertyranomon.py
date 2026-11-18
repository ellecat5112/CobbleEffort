"""Master Tyranomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the master of the Tyranomon: a hulking grey dinosaur striped with red, a white belly
with a scar mark, a fanged grin, green leaf-like fins on its head and back, and huge white claws. 25 blocks tall. A
recoloured copy of the Dark Tyranomon builder (_variant.clone).

Front is -z, y is up. 46 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_T = clone("_darktyranomon", "mastertyranomon",
           base={"grey": (140, 140, 150), "grey_dark": (70, 70, 80), "grey_light": (200, 200, 210), "black": (190, 40, 40),
                 "black_dark": (120, 14, 18), "black_light": (230, 110, 100), "belly": (246, 246, 250)},
           shiny={"grey": (200, 170, 100), "grey_dark": (130, 100, 40), "grey_light": (240, 220, 160)})
HEIGHT = 46
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a hulking grey dinosaur striped with red, a white belly, green leaf fins and huge white claws"
build = _T.make("mastertyranomon", x=False)
