"""Bryweludramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the twin-flame armour dragon. A lean crimson-and-black armoured dragon on four clawed
legs, gold-edged plates studded with blue jewels, a long armoured tail, and two long serpentine necks: one ending in
a head wreathed in roaring orange fire, the other in blue fire. 35 blocks tall.

Front is -z, y is up. 46 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import lerp, quadruped
from _digidetail import armour, cutout, flame_inside, gem, local, solid
from _route import pal, tone

HEIGHT = 46
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean crimson-and-black armoured dragon on four clawed legs with gold edges and blue jewels, and two long "
        "necks whose heads blaze with orange and blue fire")
BASE = {"red": (190, 30, 40), "red_dark": (90, 10, 16), "red_light": (240, 110, 110), "black": (34, 30, 36),
        "black_light": (90, 86, 96), "gold": (240, 196, 60), "jewel": (60, 140, 240), "jewel_light": (200, 230, 255),
        "fire": (255, 150, 40, 220), "fire_core": (255, 240, 170, 240), "blue": (70, 150, 255, 220),
        "blue_core": (220, 240, 255, 240), "claw": (220, 220, 226), "eye": (90, 230, 120)}
SHINY = {"red": (30, 40, 60), "red_dark": (12, 14, 24), "red_light": (90, 110, 150), "gold": (230, 230, 240)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", light="red_light", trim="gold", trim_w=0.4)
BLACK = armour(P, "black", "black_light")
JEWEL = gem(P, "jewel", "jewel_light")


def firef(key, core):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p[core] if v / max(H, 1e-6) < 0.35 else p[key]
        return c, c[:3]
    return s


def build():
    m = Model("bryweludramon")
    mats = {"skin": RED, "belly": BLACK, "neck": RED, "head": RED, "snout": RED, "jaw": BLACK,
            "mouth": solid(P, "black"), "tooth": solid(P, "claw"), "leg_upper": RED, "leg_lower": BLACK,
            "paw": BLACK, "claw": solid(P, "claw"), "tail": RED}
    a = quadruped(m, mats, "bryweludramon", length=26.0, body_y=18.0, body_rx=5.6, body_ry=5.6, chest_bulk=1.2,
                  neck=((4, 26, -16), (8, 34, -20), (10, 40, -24)), head_len=9.0, head_w=2.8, head_h=3.0,
                  snout=0.6, mouth_open=14, teeth=3, leg_bulk=1.2, toes=3,
                  tail=((0, 22, 18), (0, 22, 26), (2, 20, 34), (4, 16, 40)), tail_r=(2.6, 2.0, 1.4, 0.8))
    bd = a["body"]
    # the second neck: blue fire
    nk2 = m.bone("neck_2", bd, (-2, 24, -12))
    pts = [(-2, 24, -12), (-6, 30, -16), (-10, 36, -18), (-12, 42, -20)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, nk2, p0, p1, 4, RED, extend=0.8)
    h2 = m.bone("head_2", nk2, pts[-1])
    hx, hy, hz = pts[-1]
    m.round_box(h2, hx, hz - 2.0, 2.8, 4.0, hy - 1.6, hy + 2.4, RED, cut=1)
    m.box(h2, hx - 1.8, hy - 1.4, hz - 8.0, hx + 1.8, hy + 0.8, hz - 5.0, RED)
    for (hd, c, key, core) in ((a["head"], (10, 40, -24), "fire", "fire_core"), (h2, pts[-1], "blue", "blue_core")):
        spike(m, hd, (c[0], c[1] + 2.0, c[2] - 1.0), (0, 0.6, 1), 1.4, 5.0, solid(P, "gold"))
        for j, ang in enumerate((-30, 30, 90)):                                    # the fire round each head
            m.box(hd, c[0] - 5.0, c[1] - 2.0, c[2] + 1.0, c[0] + 5.0, c[1] + 12.0, c[2] + 1.0,
                  cutout(flame_inside(4, 0.25, j + (key == "blue") * 7), firef(key, core)),
                  rotation=(-35, ang, 0), pivot=(c[0], c[1], c[2] + 1.0))
        m.box(hd, c[0] - 2.9, c[1] + 0.6, c[2] - 3.0, c[0] + 2.9, c[1] + 1.4, c[2] - 2.0, solid(P, "eye"))
    # gold-edged back plates with blue jewels, spikes along the spine
    for i in range(6):
        z = -12.0 + i * 4.6
        m.box(bd, -1.6, 22.0, z - 1.4, 1.6, 23.4, z + 1.4, JEWEL)
        spike(m, bd, (0, 23.4, z + 1.4), (0, 0.6, 1), 1.8, 3.4, RED)
        for sx in (-1, 1):
            spike(m, bd, (sx * 5.0, 20.0, z), (sx, 0.5, 0.6), 1.4, 2.6, BLACK)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        lg = a[nm]
        e = lg["elbow"]
        m.box(lg["bone"], e[0] - 1.0, e[1] - 1.0, e[2] - 2.6, e[0] + 1.0, e[1] + 1.0, e[2] - 1.6, JEWEL)
    return m
