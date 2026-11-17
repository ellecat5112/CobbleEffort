"""Enbarrmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the spectral warhorse. A lean, long-legged horse of segmented gunmetal armour with gold trim and
spikes, a narrow armoured head with red eyes and swept horn-blades, a red-and-gold heraldic saddle cloth, ghostly
pale-blue flames trailing from its fetlocks and mane, and a curved blade of a tail. 25 blocks tall.

Front is -z, y is up. 46 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, cutout, fabric, flame_inside, local, metal, solid
from _route import pal, tone

HEIGHT = 46
SCALE, HITBOX = sized(25, HEIGHT, 3.2)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean long-legged horse of segmented gunmetal armour with gold trim and spikes, red eyes, swept horn-blades, a "
        "heraldic saddle cloth and ghostly blue flames at its fetlocks")
BASE = {"gun": (90, 92, 104), "gun_dark": (34, 34, 42), "gun_light": (170, 172, 188), "gold": (230, 186, 60),
        "gold_dark": (150, 110, 20), "red": (180, 30, 40), "red_dark": (100, 10, 20), "eye": (250, 50, 40),
        "ghost": (180, 220, 250, 170), "ghost_core": (240, 250, 255, 210), "mouth": (40, 30, 40), "tooth": (220, 220, 220)}
SHINY = {"gun": (220, 220, 230), "gun_dark": (140, 140, 156), "gun_light": (255, 255, 255), "red": (40, 80, 180)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "gun", "gun_dark", light="gun_light", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark")


def ghostf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["ghost_core"] if v / max(H, 1e-6) < 0.3 else p["ghost"]
    return c, c[:3]


def flames(m, bone, at, w, h, seed):
    for ang in (0, 90):
        m.box(bone, at[0] - w / 2, at[1], at[2], at[0] + w / 2, at[1] + h, at[2],
              cutout(flame_inside(3, 0.0, seed), ghostf), rotation=(0, ang, 0), pivot=at)


def build():
    m = Model("enbarrmon")
    mats = {"skin": PLATE, "belly": PLATE, "neck": PLATE, "head": PLATE, "snout": PLATE, "jaw": PLATE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": PLATE, "leg_lower": PLATE,
            "paw": GOLD, "claw": GOLD, "tail": PLATE}
    a = quadruped(m, mats, "enbarrmon", length=30.0, body_y=24.0, body_rx=4.6, body_ry=5.0, chest_bulk=1.2,
                  neck=((0, 30, -13), (0, 38, -17), (0, 42, -19)), head_len=9.0, head_w=2.4, head_h=3.0, snout=0.8,
                  mouth_open=4, teeth=0, leg_len=20.0, leg_bulk=1.0, toes=1, claws=False,
                  tail=((0, 26, 15), (0, 22, 20), (0, 16, 22)), tail_r=(1.0, 0.8, 0.6))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.6,
              solid(P, "eye", glow=True))
        pts = [(sx * 1.4, ey + 1.6, ez + 2.0), (sx * 2.4, ey + 6.0, ez + 5.0), (sx * 2.6, ey + 9.0, ez + 9.0)]
        for p0, p1 in zip(pts, pts[1:]):                                          # swept horn-blades
            rod(m, hd, p0, p1, 1, GOLD, extend=0.4, t2=2)
        x0, x1 = sorted((sx * 4.6, sx * 5.2))                                      # heraldic saddle cloth
        m.box(bd, x0, 16.0, -6.0, x1, 26.0, 8.0, fabric(P, "red", "red_dark"))
        m.box(bd, x0 - 0.05, 19.0, -1.0, x1 + 0.05, 23.0, 3.0, GOLD)
        for j in range(3):                                                         # spikes
            spike(m, bd, (sx * 4.4, 28.0, -8.0 + j * 7.0), (sx * 0.8, 1, 0), 1.0, 3.6, GOLD, tip=0.25)
    for i in range(5):                                                             # ghostly mane
        flames(m, a["neck"], (0, 36.0 + i * 1.4, -14.0 - i * 1.2), 2.6, 4.0, i)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        w = a[nm]["wrist"]
        flames(m, a[nm]["bone"], (w[0], 1.0, w[2] + 1.0), 3.0, 5.0, len(nm))
    e = a["tail_pts"][-1]                                                          # curved blade tail
    pts = [e, (e[0], e[1] - 4.0, e[2] + 3.0), (e[0], e[1] - 6.0, e[2] + 7.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, a["tail"], p0, p1, 1, metal(P, "gun_light", dark="gun_dark"), extend=0.4, t2=3)
    return m
