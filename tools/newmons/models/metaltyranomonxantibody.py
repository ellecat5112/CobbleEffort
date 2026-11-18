"""Metal Tyranomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard
after the official art on wikimon.net): Metal Tyranomon changed by the X-Antibody: a hunched cyborg dinosaur of dark
gunmetal hide banded red, a shaggy steel-grey mane, glowing cyan eyes, a great hooked steel horn-blade arching over its
head, long steel claw fingers on both hands, steel spikes down its back and a red-lit cannon on its shoulder. 25
blocks tall.

Front is -z, y is up. 50 units tall; Perfect stage. The Dark Tyranomon body (_darktyranomon) with its own colours.
"""
from __future__ import annotations

from _boxmodel import rod, spike
from _digi import sized
from _digidetail import metal, solid, strands
from _route import pal
from _variant import clone

_T = clone("_darktyranomon", "metaltyranomonxantibody",
           base={"black": (60, 62, 74), "black_dark": (22, 22, 30), "black_light": (120, 124, 140),
                 "grey": (160, 40, 50), "grey_dark": (90, 14, 20), "grey_light": (220, 100, 100),
                 "belly": (120, 30, 40)},
           shiny={"black": (200, 200, 210), "black_dark": (120, 120, 130), "black_light": (250, 250, 255)})
HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a hunched gunmetal cyborg dinosaur banded red, a shaggy steel mane, cyan eyes, a great hooked horn-blade over "
        "its head, long steel claws, back spikes and a shoulder cannon")
_EXTRA = {"steel": (196, 200, 214), "steel_dark": (90, 94, 108), "mane": (170, 176, 190), "mane_dark": (90, 94, 108),
          "cyan": (80, 230, 230), "red": (240, 50, 40)}


def P(v):
    return pal(_EXTRA, {"steel": (240, 210, 120), "mane": (240, 220, 160)}, v)


_body = _T.make("metaltyranomonxantibody", x=True)


def build():
    m = _body()
    STEEL = metal(P, "steel", dark="steel_dark")
    pts = [(0, 33.0, -9.0), (2.0, 41.0, -6.0), (2.0, 48.0, -1.0), (0.0, 50.0, 4.0), (-1.0, 47.0, 7.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                    # hooked horn-blade
        rod(m, "head", p0, p1, 1, STEEL, extend=0.3, t2=max(1, 4 - j))
    for i in range(7):                                                                  # shaggy steel mane
        spike(m, "head", ((i - 3) * 1.0, 33.0, -6.0 + abs(i - 3) * 0.4), ((i - 3) * 0.3, 0.6, 1), 1.4, 7.0,
              strands(P, "mane", "mane_dark"), tip=0.8)
    for sx in (-1, 1):
        m.box("head", min(sx * 2.6, sx * 3.0), 31.6, -13.0, max(sx * 2.6, sx * 3.0), 32.4, -11.6,
              solid(P, "cyan", glow=True))
    for arm, sx in (("arm_left", 1), ("arm_right", -1)):                                # long steel claw fingers
        for f in range(4):
            spike(m, arm, (sx * 8.0 + (f - 1.5) * 1.0, 19.0, -10.0), (sx * 0.2, -0.6, -1), 0.9, 8.0, STEEL, tip=0.8)
    for j in range(5):                                                                  # back spikes
        spike(m, "body", (0, 30.0 - j * 3.0, 0.0 + j * 2.6), (0, 1, 0.6), 1.6, 6.0 - j * 0.6, STEEL, tip=0.8)
    rod(m, "body", (5.0, 30.0, 2.0), (8.0, 36.0, -6.0), 3, STEEL, extend=0.4)          # shoulder cannon
    m.box("body", 7.0, 35.0, -7.2, 9.0, 37.0, -6.9, solid(P, "red", glow=True))
    return m
