"""Metal Tyranomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Dark Tyranomon rebuilt as a cyborg: a hulking black dinosaur half armoured in grey steel,
two great black horns curving up from its head, a steel left arm ending in a long black claw-cannon with red-tipped
claws, and a violet energy orb charging at its shoulder. 25 blocks tall.

Front is -z, y is up. 46 units tall; Perfect stage. The Dark Tyranomon body (_darktyranomon) with its own colours.
"""
from __future__ import annotations

from _boxmodel import rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, solid
from _route import pal
from _variant import clone

_T = clone("_darktyranomon", "metaltyranomon",
           base={"black": (44, 42, 48), "black_dark": (14, 12, 16), "black_light": (110, 110, 124),
                 "grey": (170, 174, 186), "grey_dark": (90, 94, 106), "grey_light": (220, 224, 234),
                 "belly": (150, 150, 160)},
           shiny={"black": (60, 70, 140), "black_dark": (20, 26, 70), "black_light": (130, 150, 220)})
HEIGHT = 46
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a hulking black cyborg dinosaur half armoured in grey steel, two great curving horns, a steel claw-cannon arm "
        "with red-tipped claws and a violet energy orb at its shoulder")
_EXTRA = {"steel": (190, 196, 210), "steel_dark": (90, 96, 110), "black": (30, 28, 34), "red": (220, 40, 40),
          "orb": (140, 110, 230, 200)}


def P(v):
    return pal(_EXTRA, {"orb": (110, 220, 160, 200), "steel": (240, 210, 120)}, v)


_body = _T.make("metaltyranomon", x=True)


def build():
    m = _body()
    for sx in (-1, 1):                                                                   # two great black horns
        pts = [(sx * 2.0, 33.0, -9.0), (sx * 4.6, 38.0, -8.0), (sx * 5.4, 43.0, -6.0), (sx * 4.4, 46.0, -4.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, "head", p0, p1, 3 - j, solid(P, "black"), extend=0.3)
    STEEL = metal(P, "steel", dark="steel_dark")
    rod(m, "arm_left", (5.4, 25.0, -5.9), (9.0, 19.0, -12.0), 4, STEEL, extend=0.6)      # steel claw-cannon arm
    rod(m, "arm_left", (9.0, 19.0, -12.0), (10.0, 17.0, -20.0), 5, solid(P, "black"), extend=0.6)
    for j in range(3):
        spike(m, "arm_left", (9.0 + (j - 1) * 1.6, 17.0, -22.0), (0, -0.2, -1), 1.2, 4.0, solid(P, "red"), tip=0.8)
    ball(m, "arm_right", (-9.0, 30.0, -4.0), 4.0, solid(P, "orb", glow=True), layers=4)  # charging energy orb
    return m
