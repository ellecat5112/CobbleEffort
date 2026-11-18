"""Mitamamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the god beast of the four souls: a great lion-bodied beast with an enormous flowing violet mane,
a golden dragon-mask head with long whiskers, pale blue-white hide, golden bands on its legs, a long dark ribbon of
spirit trailing from its back, and four soul-fires (red, blue, yellow, green) burning about its paws. 35 blocks long.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, cutout, flame_inside, fur, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a great lion-bodied beast with an enormous violet mane, a golden dragon-mask head with long whiskers, pale "
        "hide, golden leg bands, a trailing spirit ribbon and four soul-fires at its paws")
BASE = {"hide": (220, 230, 246), "hide_dark": (150, 166, 200), "mane": (130, 90, 190), "mane_dark": (60, 40, 120),
        "gold": (240, 196, 70), "gold_dark": (160, 110, 20), "ribbon": (50, 50, 90), "eye": (240, 40, 40),
        "mouth": (150, 30, 40), "tooth": (250, 250, 240), "f_red": (255, 90, 50, 210), "f_blue": (90, 150, 255, 210),
        "f_yellow": (255, 230, 80, 210), "f_green": (100, 230, 110, 210)}
SHINY = {"mane": (220, 80, 80), "mane_dark": (130, 30, 30), "hide": (250, 236, 200), "hide_dark": (200, 170, 120)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = fur(P, "hide", "hide_dark", length=1.0)
MANE = strands(P, "mane", "mane_dark")
GOLD = armour(P, "gold", "gold_dark", trim="gold_dark", trim_w=0.2)


def firef(key):
    def f(x, y, z, face, variant, box=None, **k):
        c = P(variant)[key]
        return c, c[:3]
    return cutout(flame_inside(3, 0.0, 2), f)


def build():
    m = Model("mitamamon")
    mats = {"skin": HIDE, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "claw": solid(P, "gold")}
    a = quadruped(m, mats, "mitamamon", length=32.0, body_y=18.0, body_rx=6.0, body_ry=6.0, chest_bulk=1.35,
                  neck=((0, 23, -14), (0, 27, -18)), head_len=10.0, head_w=3.8, head_h=4.0, snout=0.8,
                  mouth_open=12, teeth=6, leg_bulk=1.5, toes=4,
                  tail=((0, 21, 16), (2, 24, 22), (4, 26, 27)), tail_r=(1.6, 1.4, 1.2))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    hc = a["head_c"]
    m.round_box(hd, 0, hc[2] - 1.0, 4.2, 5.4, ey - 1.0, ey + 2.6, GOLD, cut=1)            # golden dragon mask
    for sx in (-1, 1):
        m.box(hd, min(sx * 4.2, sx * 4.5), ey, ez - 0.6, max(sx * 4.2, sx * 4.5), ey + 0.8, ez + 0.8,
              solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, ey + 2.6, hc[2] + 2.0), (sx * 0.4, 0.8, 1), 1.4, 7.0, GOLD, tip=0.8)   # horns
        pts = [(sx * 2.0, ey - 1.0, hc[2] - 5.0), (sx * 6.0, ey - 2.0, hc[2] - 6.0), (sx * 10.0, ey - 4.0, hc[2] - 3.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                 # long whiskers
            rod(m, hd, p0, p1, 1, solid(P, "gold"), extend=0.1)
    for row in range(3):                                                                 # enormous violet mane
        for i in range(12):
            ang = 2 * math.pi * i / 12
            spike(m, bd, (5.5 * math.cos(ang) * (0.9 + row * 0.1), 24.0 + 5.5 * math.sin(ang), -10.0 + row * 3.0),
                  (math.cos(ang), math.sin(ang) + 0.2, 0.9), 2.4, 9.0 - row * 1.6, MANE, tip=0.8)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):  # golden leg bands
        anc = a[nm]
        w = anc.get("wrist") or anc.get("ankle")
        if w:
            m.round_box(anc["bone"], w[0], w[2], 2.4, 2.4, w[1] + 1.0, w[1] + 2.6, GOLD, cut=1)
    rb = m.bone("ribbon", bd, (0, 26, 2))                                                # trailing spirit ribbon
    pts = [(0, 26.0, 2.0), (-4.0, 34.0, 8.0), (-10.0, 36.0, 16.0), (-14.0, 30.0, 24.0), (-16.0, 22.0, 30.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, rb, p0, p1, 1, solid(P, "ribbon"), extend=0.3, t2=3)
    for (nm, key) in zip(("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"),
                         ("f_red", "f_blue", "f_yellow", "f_green")):                     # four soul-fires
        anc = a[nm]
        w = anc.get("wrist") or anc.get("ankle") or anc["hip"]
        for ang in (0, 90):
            m.box(anc["bone"], w[0] - 2.0, 0.0, w[2], w[0] + 2.0, 5.0, w[2], firef(key), rotation=(0, ang, 0),
                  pivot=(w[0], 0.0, w[2]))
    return m
