"""Lynxmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
Armor Digimon of courage's flame: a lean lynx made of fire, its whole body orange-red fur striped dark and wreathed in
licking flames, a snarling lynx face with tufted ears, a flaming mane and tail, and silver claws on its paws. 15
blocks long.

Front is -z, y is up. 28 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import cutout, flame_inside, fur, local, metal, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
LOOK = "a lean lynx made of fire, orange-red striped fur wreathed in flames, tufted ears, a flaming mane and tail and silver claws"
BASE = {"orange": (240, 120, 40), "orange_dark": (170, 50, 14), "stripe": (110, 30, 14), "silver": (220, 224, 234),
        "silver_dark": (110, 114, 126), "eye": (250, 220, 60), "mouth": (160, 30, 30), "tooth": (250, 248, 236),
        "fire": (255, 170, 40, 210), "fire_core": (255, 245, 180, 240)}
SHINY = {"orange": (80, 150, 240), "orange_dark": (30, 70, 170), "fire": (120, 200, 255, 210)}


def P(v):
    return pal(BASE, SHINY, v)


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "up") and abs(math.sin(z * 0.9 + y * 0.4)) > 0.92:
        return tone(p["stripe"], face), None
    return fur(P, "orange", "orange_dark", length=1.0)(x, y, z, face, variant, box=box, **k)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def build():
    m = Model("lynxmon")
    mats = {"skin": coatf, "belly": coatf, "neck": coatf, "head": coatf, "snout": coatf, "jaw": coatf,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": coatf, "leg_lower": coatf, "paw": coatf,
            "claw": metal(P, "silver", dark="silver_dark"), "tail": coatf}
    a = quadruped(m, mats, "lynxmon", length=24.0, body_y=12.0, body_rx=4.0, body_ry=4.2, chest_bulk=1.2,
                  neck=((0, 15, -11), (0, 17, -14)), head_len=8.0, head_w=3.0, head_h=3.2, snout=0.6, mouth_open=16,
                  teeth=4, leg_bulk=1.1, toes=3, tail=((0, 14, 12), (0, 17, 17), (0, 20, 20)), tail_r=(1.6, 1.4, 1.2))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    hc = a["head_c"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.6,
              solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.8, hc[1] + 2.4, hc[2] + 1.4), (sx * 0.3, 1, 0.2), 1.4, 3.6, coatf, tip=0.8)
        spike(m, hd, (sx * 2.4, hc[1] + 5.8, hc[2] + 1.8), (sx * 0.3, 1, 0.2), 0.8, 1.6, solid(P, "stripe"), tip=0.8)
    F = cutout(flame_inside(4, 0.1, 8), firef)
    for j, (zz, h) in enumerate(((-10.0, 8.0), (-5.0, 9.0), (0.0, 8.0), (5.0, 7.0), (10.0, 6.0))):   # flames along back
        for rot in (0, 90):
            m.box(bd, -2.6, 15.0, zz, 2.6, 15.0 + h, zz, F, rotation=(0, rot, 0), pivot=(0, 15.0, zz))
    tp = a["tail_pts"][-1]
    for rot in (0, 90):
        m.box(a["tail"], tp[0] - 2.0, tp[1], tp[2], tp[0] + 2.0, tp[1] + 7.0, tp[2], F, rotation=(0, rot, 0), pivot=tp)
    return m
