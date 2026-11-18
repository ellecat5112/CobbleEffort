"""Regulusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): an evil dragon-knight: a lean figure in black-and-magenta armour edged gold, a horned dragon helm
with a blue scarf mask, two vast ragged blue-black wings torn into lightning shapes, a long black tower shield etched
with gold runes, a black serpentine tail, and a golden trident below. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, local, metal, noise2, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a lean evil dragon-knight in black-and-magenta armour with a horned helm, ragged blue-black lightning wings and a rune tower shield"
BASE = {"black": (36, 32, 44), "black_dark": (12, 10, 16), "magenta": (190, 40, 150), "magenta_dark": (100, 14, 80),
        "gold": (230, 190, 70), "gold_dark": (150, 100, 20), "blue": (40, 60, 150), "blue_dark": (14, 20, 60),
        "eye": (250, 60, 90)}
SHINY = {"magenta": (60, 180, 200), "magenta_dark": (20, 100, 120), "blue": (150, 40, 40), "blue_dark": (60, 14, 14)}


def P(v):
    return pal(BASE, SHINY, v)


def platef(x, y, z, face, variant, box=None, **k):
    if (y % 6.0) < 1.6:
        return armour(P, "magenta", "magenta_dark")(x, y, z, face, variant, box=box, **k)
    return armour(P, "black", "black_dark", trim="gold", trim_w=0.2)(x, y, z, face, variant, box=box, **k)


GOLD = metal(P, "gold", dark="gold_dark")


def torn(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    f = (box.lo[0] + u) * 0.7
    return v / max(H, 1e-6) > 0.15 + 0.4 * abs(math.sin(f * 1.3)) * noise2(f, 2)


def shieldf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and (abs((y % 5.0) - 2.5) < 0.3 or abs(x - (box.lo[0] + box.size[0] / 2)) < 0.25):
        return tone(p["gold"], face), None
    return armour(P, "black", "black_dark", trim="gold", trim_w=0.3, trim_edges=("top", "bottom", "sides"))(
        x, y, z, face, variant, box=box, **k)


def build():
    m = Model("regulusmon")
    mats = {"skin": platef, "talon": GOLD, "claw": GOLD}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.85, claws=True, talons=True, digitigrade=True,
                 name="regulusmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.6, 3.4, 54.0, 60.0, platef, cut=1)
    m.round_box(hd, 0, -3.0, 2.8, 1.0, 53.6, 56.4, solid(P, "blue"), cut=0)                 # scarf mask
    m.box(hd, -1.8, 57.4, -4.5, 1.8, 58.2, -4.3, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 60.0, 0), (sx * 0.4, 1, 0.6), 1.4, 8.0, GOLD, tip=0.8)
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 50.0, 4.0))
        for j in range(5):                                                               # ragged lightning wings
            ang = math.radians(10 + j * 22)
            x0, x1 = sorted((sx * 3.0, sx * (3.0 + 28.0 - j * 3.0)))
            m.box(wb, x0, 47.0, 4.0 + j * 0.3, x1, 53.0, 4.0 + j * 0.3, cutout(torn, armour(P, "blue", "blue_dark")),
                  rotation=(0, -sx * 10, sx * (math.degrees(ang) - 30)), pivot=(sx * 3.0, 50.0, 4.0))
    w = a["arm_left"]["wrist"]                                                           # tower shield
    m.box(a["arm_left"]["bone"], w[0] + 1.0, w[1] - 18.0, w[2] - 6.0, w[0] + 2.0, w[1] + 10.0, w[2] + 2.0, shieldf)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (2.0, 22.0, 8.0), (-2.0, 12.0, 10.0), (0, 4.0, 6.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 3 - i, platef, extend=0.4)
    for f in (-1, 0, 1):                                                                 # golden trident tip
        spike(m, tl, (f * 1.4, 4.0, 6.0), (f * 0.3, -1, -0.2), 0.9, 4.0, GOLD, tip=0.8)
    return m
