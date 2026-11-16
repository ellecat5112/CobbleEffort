"""Atlur Kabuterimon (Blue) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): a hulking beetle-beast. A rounded violet-blue carapace with a red dome on its head,
forked horns, an open fanged maw with a skeletal pale chest plate below it, red ridged cheek plates, and six long
jointed violet arms and legs ending in clawed hands. 25 blocks tall.

Front is -z, y is up. 46 units tall; Perfect stage. make(red=True): Atlur Kabuterimon (Red) (crimson carapace,
green dome).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, gem, metal, skin, solid
from _route import pal, tone

HEIGHT = 46
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a hulking beetle-beast with a violet-blue carapace, a red dome on its head, forked horns, a fanged maw over a "
        "skeletal chest plate and six long jointed clawed limbs")
BASE = {"shell": (70, 60, 170), "shell_dark": (30, 24, 90), "shell_light": (140, 130, 230), "dome": (220, 40, 50),
        "dome_light": (255, 150, 150), "cheek": (200, 70, 80), "bone": (236, 230, 210), "bone_dark": (170, 160, 140),
        "mouth": (110, 20, 30), "tooth": (250, 250, 246), "claw": (60, 54, 120)}
SHINY = {"shell": (60, 140, 90), "shell_dark": (20, 70, 40), "shell_light": (140, 220, 160), "dome": (240, 200, 60),
         "dome_light": (255, 240, 170)}
RED = {"shell": (180, 30, 30), "shell_dark": (100, 10, 10), "shell_light": (240, 110, 100), "dome": (80, 200, 170),
       "dome_light": (200, 250, 240), "claw": (80, 70, 140)}
RED_SHINY = {"shell": (60, 60, 70), "shell_dark": (24, 24, 30), "shell_light": (130, 130, 150),
             "dome": (240, 120, 200), "dome_light": (255, 210, 240)}


def make(name, red=False):
    B = dict(BASE, **(RED if red else {}))
    S = RED_SHINY if red else SHINY

    def P(v):
        return pal(B, S, v)

    SHELL = armour(P, "shell", "shell_dark", light="shell_light", seams=(1.6,))
    LIMB = metal(P, "shell", dark="shell_dark", light="shell_light", streak=2.4)
    BONE = armour(P, "bone", "bone_dark", seams=(1.2,))

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 22, 0))
        ball(m, bd, (0, 24.0, 4.0), 13.0, SHELL, layers=8, squash=1.1)                  # the great carapace
        hd = m.bone("head", bd, (0, 24, -8))
        ball(m, hd, (0, 26.0, -10.0), 6.4, SHELL, layers=5)
        ball(m, hd, (0, 31.0, -9.0), 3.4, gem(P, "dome", "dome_light", glow=False), layers=3)   # red dome
        m.box(hd, -4.4, 19.0, -16.4, 4.4, 24.0, -12.0, solid(P, "mouth"))                # fanged maw
        for i in range(6):
            x = -3.6 + i * 1.45
            spike(m, hd, (x, 24.0, -16.0), (0, -1, -0.2), 1.0, 2.2, solid(P, "tooth"))
            spike(m, hd, (x + 0.7, 19.2, -16.0), (0, 1, -0.2), 1.0, 1.6, solid(P, "tooth"))
        for sx in (-1, 1):
            m.box(hd, min(sx * 4.0, sx * 7.0), 22.0, -14.0, max(sx * 4.0, sx * 7.0), 28.0, -10.0, solid(P, "cheek"))
            pts = [(sx * 3.0, 30.0, -12.0), (sx * 6.0, 36.0, -14.0), (sx * 9.0, 40.0, -12.0)]   # forked horns
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 2, LIMB, extend=0.3)
            spike(m, hd, pts[1], (sx * 1, 0.4, -0.3), 1.2, 3.6, LIMB)
        for j in range(4):                                       # skeletal chest plate
            m.box(bd, -4.0 + j * 0.3, 10.0 + j * 2.4, -12.0, 4.0 - j * 0.3, 11.6 + j * 2.4, -10.0, BONE)
        m.box(bd, -0.6, 10.0, -12.4, 0.6, 19.0, -11.6, BONE)
        for i, (yy, zz) in enumerate(((28.0, -6.0), (20.0, -2.0), (16.0, 6.0))):          # six jointed limbs
            for sx in (1, -1):
                nm = (f"arm_{'left' if sx > 0 else 'right'}" if i == 0 else
                      f"leg_{'front' if i == 1 else 'back'}_{'left' if sx > 0 else 'right'}")
                lg = m.bone(nm, top if i else bd, (sx * 9.0, yy, zz))
                if i == 0:
                    knee = (sx * 18.0, yy + 8.0, zz - 4.0)
                    hand = (sx * 24.0, yy + 4.0, zz - 10.0)
                else:
                    knee = (sx * 19.0, yy + 6.0, zz - 2.0)
                    hand = (sx * 22.0, 1.0, zz - 4.0)
                rod(m, lg, (sx * 9.0, yy, zz), knee, 3, LIMB, extend=0.5)
                rod(m, lg, knee, hand, 3, LIMB, extend=0.5)
                for d in ((sx * 0.6, -0.3, -1), (sx * 0.3, 0.4, -1), (sx * 1, -0.4, 0.2)):
                    spike(m, lg, hand, d, 1.2, 3.2, solid(P, "claw"))
        return m
    return build, P


build, P = make("atlurkabuterimonblue")
