"""Shared builder for Chronomon (CobbleEffort: Digital; hand-built after the official art on wikimon.net), the god of
time, in its two modes.

"destroy": Destroy Mode, a crimson demon-dragon god with a black sun disc on its chest, a red-and-white sash, baggy
blue trousers, huge red clawed hands and taloned feet, a crown of violet spines, and two vast black blade-wings
lined with glowing yellow and cyan lights.
"holy": Holy Mode, a white bird-god in a white robe painted with a red sun, a pale masked face with a red crest, red-
and-violet striped trousers with gold buckles, and enormous wings of countless white paper strips.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import Bulge, armour, fabric, local, metal, skin, solid, torso_bulges
from _route import pal, tone

DESTROY = {"skin": (200, 40, 40), "skin_dark": (110, 14, 18), "skin_light": (250, 120, 110), "white": (240, 240, 246),
           "blue": (50, 80, 170), "blue_dark": (20, 34, 100), "black": (30, 30, 38), "black_light": (90, 90, 106),
           "spine": (130, 100, 200), "light1": (250, 220, 60), "light2": (80, 230, 250), "claw": (40, 40, 48),
           "sun": (20, 20, 26), "gold": (230, 190, 60), "eye": (250, 220, 60), "vein": (230, 90, 80)}
HOLY = {"skin": (246, 246, 250), "skin_dark": (190, 194, 210), "skin_light": (255, 255, 255), "white": (250, 250, 252),
        "blue": (200, 50, 60), "blue_dark": (110, 60, 160), "black": (40, 40, 46), "black_light": (200, 204, 216),
        "spine": (220, 40, 50), "light1": (250, 250, 255), "light2": (220, 224, 236), "claw": (190, 196, 220),
        "sun": (210, 30, 40), "gold": (230, 190, 60), "eye": (220, 30, 40), "vein": (200, 200, 210)}
SHINY_D = {"skin": (60, 60, 70), "skin_dark": (24, 24, 30), "skin_light": (140, 140, 160), "blue": (180, 40, 40)}
SHINY_H = {"skin": (250, 230, 170), "skin_dark": (210, 180, 100), "white": (255, 240, 190), "sun": (40, 90, 210)}


def make(name, holy=False):
    base = HOLY if holy else DESTROY

    def P(v):
        return pal(base, dict(base, **(SHINY_H if holy else SHINY_D)), v)

    SKIN = skin(P, "skin", dark="skin_dark", light="skin_light", var=0.03,
                bulges=[Bulge("north", sx * 10.0, 42.0, 2.2, 4.0, light=0.35, shadow=0.45) for sx in (-1, 1)])

    def chestf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            d = math.hypot(x, y - 45.0)
            if d < 3.0:
                return tone(p["sun"] if (d < 2.0 or holy) else p["gold"], face), None
            if holy and d < 5.0 and abs(math.sin(math.atan2(y - 45.0, x) * 6)) > 0.7:
                return tone(p["sun"], face), None                     # sun rays
            if abs(x - (51.0 - y) * 0.5) < 0.9 and not holy:
                return tone(p["white"], face), None                   # sash
        if holy:
            return fabric(P, "white", "skin_dark", axis="y", period=2.4)(x, y, z, face, variant, box=box, **k)
        return skin(P, "skin", dark="skin_dark", light="skin_light", bulges=torso_bulges(0, 51.0, 6.0, abs_rows=4),
                    var=0.03)(x, y, z, face, variant, box=box, **k)

    def trouserf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if holy and (x * 0.8 + z * 0.3) % 3.0 < 1.4:
            return tone(p["blue_dark"], face), None
        return fabric(P, "blue", "blue_dark", axis="y", period=2.4)(x, y, z, face, variant, box=box, **k)

    def stripsf(x, y, z, face, variant, box=None, **k):
        """Holy wings: countless white paper strips with grey edges."""
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        if (u * 1.4) % 2.0 < 0.2 or (v * 0.9 + u * 0.3) % 3.0 < 0.2:
            return tone(p["black_light"], face), None
        return tone(p["white"], face), None

    def bladef(x, y, z, face, variant, box=None, **k):
        """Destroy wings: black blades with glowing lights along their length."""
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        if abs(v - H / 2) < 0.8 and (u % 5.0) < 1.6:
            c = p["light1"] if int(u / 5.0) % 2 else p["light2"]
            return c, c
        return armour(P, "black", "black", light="black_light")(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": SKIN, "chest": chestf, "abs": chestf, "pelvis": trouserf, "thigh": trouserf, "knee": trouserf,
                "shin": trouserf, "calf": trouserf, "claw": solid(P, "claw"), "talon": solid(P, "claw"),
                "foot": SKIN if not holy else solid(P, "black_light")}
        a = humanoid(m, mats, bulk=1.3, arm_bulk=1.45, leg_bulk=1.3, digitigrade=True, claws=True, talons=True,
                     name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.8, 3.0, 54.4, 61.0, SKIN, cut=1)
        if holy:
            m.box(hd, -2.0, 55.0, -6.0, 2.0, 58.4, -3.0, SKIN)                     # beaked mask
            spike(m, hd, (0, 55.6, -6.0), (0, -0.4, -1), 1.6, 2.6, solid(P, "gold"))
        else:
            m.box(hd, -2.0, 54.6, -6.4, 2.0, 57.4, -3.0, SKIN)
        m.box(hd, -2.0, 58.0, -3.6, 2.0, 58.6, -3.3, solid(P, "eye", glow=True))
        for i in range(7):                                                         # crown of spines / red crest
            ang = math.radians(-60 + i * 20)
            spike(m, hd, (2.4 * math.sin(ang), 60.4, -0.4), (math.sin(ang) * 0.6, 1, 0.3), 1.4,
                  6.0 if not holy else 4.0, solid(P, "spine"), tip=0.3)
        for nm in ("arm_left", "arm_right"):                                       # huge hands
            h = a[nm]["hand"]
            m.round_box(a[nm]["bone"], h[0], h[2], 3.0, 3.0, h[1] - 3.0, h[1] + 2.0, SKIN, cut=1)
        wb = m.bone("wings", bd, (0, 50, 4))
        for sx in (-1, 1):
            if holy:                                                               # paper-strip wings
                for j in range(12):
                    ang = 70 - j * 12
                    x0, x1 = sorted((sx * 3.0, sx * (22.0 + (j % 3) * 4.0)))
                    m.box(wb, x0, 48.0, 5.0 + j * 0.3, x1, 52.0, 5.0 + j * 0.3, stripsf,
                          rotation=(0, 0, sx * ang), pivot=(sx * 3.0, 50.0, 5.0 + j * 0.3))
            else:                                                                  # black blade-wings
                for j, (ang, ln) in enumerate(((35, 30.0), (10, 26.0))):
                    x0, x1 = sorted((sx * 3.0, sx * ln))
                    m.box(wb, x0, 48.0, 5.0 + j, x1, 52.0, 6.4 + j, bladef, rotation=(0, sx * 10, sx * ang),
                          pivot=(sx * 3.0, 50.0, 5.0 + j))
                for j in range(6):
                    spike(m, wb, (sx * 3.0, 54.0, 5.0), (sx * (0.2 + j * 0.15), 1, 0.2), 1.0, 10.0 + j, solid(P, "spine"),
                          tip=0.3)
        return m
    return build
