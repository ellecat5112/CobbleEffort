"""Nise Agumon Hakase (a Digimon of the CobbleEffort: Digital crossover; after the official art on wikimon.net): the
"fake" Agumon Hakase: Agumon's body in blue with a pale belly, a black academic gown, a black mortarboard with a gold
tassel and a pointer topped with a little pink bat. 1 block tall.

Front is -z, y is up. 23 units tall; Child stage. Agumon's body (_agumon.build_agumon, hakase=True) loaded fresh with
its own colours, the way _greyvar recolours Greymon (never patching the shared palette).
"""
from __future__ import annotations

from _digi import sized
from _greyvar import _fresh

HEIGHT = 23
SCALE, HITBOX = sized(1, HEIGHT, 1.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a blue Agumon in a black academic gown and mortarboard with a gold tassel, holding a pointer topped with a pink bat"

_d = _fresh("_digi", "niseagumonhakase")
_d.BASE.update({"orange": (80, 110, 200), "orange_dark": (40, 60, 150), "belly": (180, 200, 240), "stripe": (30, 40, 100),
                "coat": (40, 40, 46), "coat_dark": (20, 20, 24), "cap": (30, 30, 36), "tassel": (240, 200, 60),
                "metal_light": (240, 130, 180)})
_d.SHINY.update({"orange": (120, 180, 120), "orange_dark": (60, 120, 60), "belly": (210, 240, 210),
                 "coat": (120, 30, 40), "coat_dark": (70, 14, 20)})
_a = _fresh("_agumon", "niseagumonhakase")
for _k in ("P", "claw_fan", "eye", "solid", "teeth_row"):
    setattr(_a, _k, getattr(_d, _k))


def build():
    return _a.build_agumon("niseagumonhakase", hakase=True)
