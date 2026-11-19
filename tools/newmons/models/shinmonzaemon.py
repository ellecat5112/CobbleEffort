"""Shin Monzaemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a monstrous patchwork teddy bear: a huge hulking body of starry violet-and-blue galaxy
plush patched with brown fur and bandages, a zip across its belly, a small bear head with a fanged grin and a burning
pink flame, red claws, a pink heart pad on its fist, and two vast melting wings of starry galaxy. 35 blocks.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, fabric, fur, local, metal, noise2, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a hulking patchwork teddy bear of starry galaxy plush and brown fur, a zipped belly, a fanged grin and vast melting galaxy wings"
BASE = {"violet": (90, 50, 170), "blue": (40, 40, 140), "star": (250, 240, 255), "pink": (240, 100, 180),
        "brown": (130, 90, 60), "brown_dark": (80, 50, 30), "red": (210, 40, 50), "steel": (200, 204, 216),
        "bandage": (236, 230, 214), "tooth": (250, 250, 240), "flame": (255, 140, 210)}
SHINY = {"violet": (40, 120, 90), "blue": (20, 70, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def galaxyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if math.sin(x * 2.3 + y * 1.1) * math.sin(z * 1.9 - y * 0.7) > 0.95:
        return p["star"], p["star"]
    n = noise2(x * 0.2 + z * 0.15, y * 0.2, 6)
    return tone(p["violet"] if n > 0.45 else p["blue"], face), None


FUR = fur(P, "brown", "brown_dark", length=1.4)


def melt(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    f = (box.lo[0] + u) * 0.6
    return v / max(H, 1e-6) > 0.25 * abs(math.sin(f)) + 0.15 * noise2(f, 9)


def build():
    m = Model("shinmonzaemon")
    top = m.bone("shinmonzaemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 26.0, 0), 13.0, galaxyf, layers=7, ry=14.0)                              # hulking body
    m.round_box(bd, 6.0, -1.0, 6.0, 12.0, 16.0, 30.0, FUR, cut=3)                            # brown patch
    m.box(bd, -0.6, 14.0, -13.4, 0.6, 32.0, -12.8, metal(P, "steel"))                          # zip
    m.round_box(bd, 0, 0, 12.6, 12.6, 20.0, 22.0, solid(P, "bandage"), cut=4)
    hd = m.bone("head", bd, (0, 40, -4))
    ball(m, hd, (0, 44.0, -6.0), 4.6, FUR, layers=4)
    for sx in (-1, 1):
        ball(m, hd, (sx * 3.6, 48.0, -6.0), 1.6, FUR, layers=2)
    m.box(hd, -2.6, 41.0, -10.8, 2.6, 42.4, -10.4, solid(P, "red"))
    for j in range(5):
        spike(m, hd, (-2.0 + j, 42.4, -10.6), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
    spike(m, hd, (1.6, 48.4, -6.0), (0.3, 1, 0), 1.6, 5.0, solid(P, "flame", glow=True), tip=0.8)
    for sx in (-1, 1):                                                                   # melting galaxy wings
        for j in range(4):
            x0, x1 = sorted((sx * 8.0, sx * (34.0 - j * 4.0)))
            m.box(bd, x0, 26.0 + j * 4.0, 8.0 + j * 0.3, x1, 38.0 + j * 4.0, 8.0 + j * 0.3, cutout(melt, galaxyf),
                  rotation=(0, -sx * 15, sx * (10 - j * 8)), pivot=(sx * 8.0, 32.0, 8.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 12.0, 32.0, 0))
        rod(m, ab, (sx * 12.0, 32.0, 0), (sx * 18.0, 20.0, -6.0), 6, galaxyf if sx > 0 else FUR, extend=0.8)
        ball(m, ab, (sx * 18.6, 18.0, -7.0), 4.0, FUR, layers=3)
        m.box(ab, sx * 18.6 - 1.4, 16.6, -11.2, sx * 18.6 + 1.4, 19.4, -10.8, solid(P, "pink"))
        for f in range(4):
            spike(m, ab, (sx * 18.6 + (f - 1.5) * 1.6, 15.0, -9.0), (0, -1, -0.4), 1.0, 4.0, solid(P, "red"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 6.0, 14.0, 0))
        m.round_box(lg, sx * 6.0, 0, 5.0, 5.0, 2.0, 16.0, galaxyf, cut=2)
        for f in range(3):
            spike(m, lg, (sx * 6.0 + (f - 1) * 2.4, 1.0, -4.6), (0, -0.2, -1), 1.2, 3.0, solid(P, "red"), tip=0.8)
    return m
