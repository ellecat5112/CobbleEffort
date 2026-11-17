"""Bombermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a tattered bomber. A gaunt figure wrapped in ragged off-white bandages and cloth strips that trail
away in tatters, black straps buckled round its chest and limbs, a hooded bandaged head with two short black horns
and a glowing red visor slit, black gloves, and little black bomb-spiders dangling from long fuse cords that loop
round it, their fuses alight. 25 blocks tall.

Front is -z, y is up. 62 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import cutout, fabric, leather, local, noise2, solid
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(25, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a gaunt figure in ragged off-white bandages and trailing tatters, black straps, a hooded head with black "
        "horns and a glowing red visor, and black bomb-spiders dangling from lit fuse cords")
BASE = {"cloth": (232, 228, 214), "cloth_dark": (170, 162, 140), "black": (34, 32, 38), "black_light": (90, 88, 100),
        "visor": (240, 60, 40), "visor_light": (255, 200, 120), "spark": (255, 200, 60), "cord": (40, 40, 46)}
SHINY = {"cloth": (60, 60, 70), "cloth_dark": (24, 24, 30), "black": (220, 200, 160), "black_light": (250, 236, 200),
         "visor": (60, 220, 120)}


def P(v):
    return pal(BASE, SHINY, v)


CLOTH = fabric(P, "cloth", "cloth_dark", axis="y", period=1.6)
STRAP = leather(P, "black", "black_light")


def wrapped(x, y, z, face, variant, box=None, **k):
    """Bandage wrapping: diagonal strips with dark gaps between them."""
    p = P(variant)
    t = (y + 0.5 * (x + z)) % 2.0
    if t < 0.22:
        return tone(p["cloth_dark"], face), None
    return CLOTH(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 57.0 < y < 58.4 and abs(x) < 2.4:
        c = p["visor_light"] if abs(y - 57.7) < 0.25 else p["visor"]
        return c, c
    return wrapped(x, y, z, face, variant, box=box, **k)


def rag(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = v / max(H, 1e-6)
    return t > 0.2 * noise2((box.lo[0] + u) * 1.3, 4.0) + 0.1 * abs(math.sin(u * 2.1))


def spider(m, bone, c):
    """A little black bomb-spider: a round body, eight thin legs and a lit fuse."""
    ball(m, bone, c, 1.6, solid(P, "black"), layers=3)
    for i in range(4):
        for sx in (-1, 1):
            rod(m, bone, (c[0] + sx * 1.2, c[1], c[2] - 1.2 + i * 0.8),
                (c[0] + sx * 3.0, c[1] - 1.6, c[2] - 2.0 + i * 1.3), 1, solid(P, "black"), extend=0)
    m.box(bone, c[0] - 0.4, c[1] + 1.4, c[2] - 0.4, c[0] + 0.4, c[1] + 2.4, c[2] + 0.4, solid(P, "spark", glow=True))


def build():
    m = Model("bombermon")
    mats = {"skin": wrapped, "pelvis": STRAP, "hand": solid(P, "black"), "finger": solid(P, "black"),
            "foot": STRAP, "toe": STRAP}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=0.9, name="bombermon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0.0, 2.8, 3.0, 54.0, 61.4, headf, cut=1)
    m.round_box(hd, 0, 0.8, 3.4, 3.4, 58.0, 62.4, wrapped, cut=1)                         # the hood
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 61.6, 0), (sx * 0.7, 1, 0.3), 1.4, 3.0, solid(P, "black"), tip=0.4)
    for y in (46.0, 41.0, 36.0):                                                          # straps
        m.round_box(bd, 0, 0.2, 5.0 if y > 40 else 4.2, 3.8, y - 0.6, y + 0.6, STRAP, cut=1)
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):
        ab = a[nm]
        p0 = ab.get("elbow", ab.get("knee"))
        m.round_box(ab["bone"], p0[0], p0[2], 2.2, 2.2, p0[1] - 0.8, p0[1] + 0.6, STRAP, cut=1)
        for j in range(3):                                                                # trailing tatters
            m.box(ab["bone"], p0[0] - 1.4, p0[1] - 9.0 - j, p0[2] + 1.0 + j * 0.4, p0[0] + 1.4, p0[1] - 1.0,
                  p0[2] + 1.0 + j * 0.4, cutout(rag, CLOTH), rotation=(14 + j * 10, j * 30, 0), pivot=p0)
    # a ragged cloth mantle
    cb = m.bone("cap", bd, (0, 52, 3))
    cape(m, cb, 52.0, 14.0, 40.0, CLOTH, z=4.0, flare=1.2, panels=7, sweep=(0, 6), seed=7)
    # fuse cords looping round it with bomb-spiders on their ends
    for k, (sx, y, z) in enumerate(((1, 44.0, -2.0), (-1, 36.0, 2.0), (1, 26.0, 4.0), (-1, 54.0, -1.0))):
        cb2 = m.bone(f"cord_{k}", bd, (sx * 4.0, y, z))
        pts = [(sx * 4.0, y, z)]
        for i in range(1, 7):
            th = i * 0.55
            pts.append((sx * (4.0 + 2.6 * i), y + 4.0 * math.sin(th) - i * 0.6, z - 4.0 * math.cos(th) + 4.0))
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, cb2, p0, p1, 1, solid(P, "cord"), extend=0.3)
        spider(m, cb2, (pts[-1][0], pts[-1][1] - 2.0, pts[-1][2]))
    return m
