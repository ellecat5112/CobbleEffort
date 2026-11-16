"""Alraumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little mandrake. A round pale-green head with two huge glossy black eyes and a fanged grin, a
lilac lily blooming on its crown with a curled stem, a cloak of veined green leaves for a body, long leaf-claw hands
tipped violet and root feet. 1 block tall.

Front is -z, y is up. 30 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import local, mix, plane, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 0.7)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 18}
LOOK = ("a little mandrake: a round pale-green head with huge glossy black eyes, a lilac lily on its crown, a cloak "
        "of veined green leaves, violet-tipped leaf claws and root feet")
BASE = {"head": (200, 230, 120), "head_dark": (130, 170, 60), "leaf": (90, 170, 50), "leaf_dark": (40, 100, 30),
        "vein": (170, 220, 110), "lily": (190, 160, 230), "lily_dark": (120, 90, 180), "violet": (110, 70, 170),
        "root": (200, 200, 90), "eye": (16, 16, 22), "white": (250, 250, 250), "mouth": (60, 40, 30)}
SHINY = {"head": (240, 200, 120), "head_dark": (190, 140, 60), "leaf": (180, 70, 90), "leaf_dark": (110, 30, 50),
         "vein": (240, 150, 160), "lily": (250, 240, 140), "lily_dark": (210, 180, 60)}


def P(v):
    return pal(BASE, SHINY, v)


HEAD = skin(P, "head", dark="head_dark", var=0.04)


def leaff(x, y, z, face, variant, box=None, **k):
    """A leaf: a pale midrib and branching veins on green."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    cu = u - W / 2
    if abs(cu) < 0.22 or abs(abs(cu) - ((v * 0.8) % 2.0) * 0.6) < 0.16:
        return tone(p["vein"], face), None
    return tone(mix(p["leaf_dark"], p["leaf"], 0.4 + 0.6 * v / max(H, 1e-6)), face), None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            du, dv = a - sx * 2.6, b - 22.0
            if (du / 1.9) ** 2 + (dv / 2.4) ** 2 < 1:
                return (p["white"] if math.hypot(du + 0.6, dv - 0.9) < 0.5 else p["eye"]), None
        if abs(b - 18.4 - 0.15 * abs(a)) < 0.25 and abs(a) < 2.4:
            return p["mouth"], None
        if abs(a - 1.4) < 0.3 and 17.4 < b < 18.4:
            return p["white"], None                                     # its one fang
    return HEAD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("alraumon")
    top = m.bone("alraumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    hd = m.bone("head", bd, (0, 17, 0))
    ball(m, hd, (0, 21.0, 0), 5.6, headf, layers=6)
    rod(m, hd, (0, 26.0, 0), (0, 27.5, 0.4), 2, solid(P, "leaf_dark"), extend=0.2)
    fl = m.bone("cap", hd, (0, 27, 0))
    for i in range(6):                                           # lily petals curling outward
        ang = math.radians(i * 60)
        tip = (4.4 * math.sin(ang), 29.5, 4.4 * math.cos(ang))
        rod(m, fl, (0, 27.4, 0), tip, 2, solid(P, "lily"), extend=0.3, t2=1)
        spike(m, fl, tip, (math.sin(ang), -0.6, math.cos(ang)), 1.0, 1.4, solid(P, "lily_dark"))
    for j, (p0, p1) in enumerate((((0, 28, 0), (0, 31, 0.6)), ((0, 31, 0.6), (1.6, 32.6, 0.4)),
                                  ((1.6, 32.6, 0.4), (2.2, 31.2, 0.2)), ((2.2, 31.2, 0.2), (1.2, 30.4, 0.2)))):
        rod(m, fl, p0, p1, 1, solid(P, "violet"), extend=0.3)          # the curled stem
    for i in range(10):                                          # a cloak of leaves hanging from under the head
        ang = math.radians(-150 + i * 33)
        base = (3.6 * math.sin(ang), 17.0, -3.6 * math.cos(ang))
        m.box(bd, base[0] - 1.6, 6.0, base[2], base[0] + 1.6, 17.0, base[2], leaff,
              rotation=(-12 * math.cos(ang), -math.degrees(ang), 0), pivot=base)
    m.round_box(bd, 0, 0, 3.0, 3.0, 8.0, 17.0, leaff, cut=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):         # long leaf-claw arms
        ab = m.bone(nm, bd, (sx * 3.0, 15.0, 0))
        el = (sx * 6.5, 12.0, -1.0)
        rod(m, ab, (sx * 3.0, 15.0, 0), el, 2, leaff, extend=0.3)
        for f in range(3):
            tip = (sx * (8.0 + f * 0.6), 5.5 + f * 0.8, -2.5 + f * 1.4)
            rod(m, ab, el, tip, 1, leaff, extend=0.3)
            spike(m, ab, tip, (sx * 0.2, -1, 0), 0.9, 1.6, solid(P, "violet"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):         # root feet
        lg = m.bone(nm, top, (sx * 1.6, 8.0, 0))
        rod(m, lg, (sx * 1.6, 8.0, 0), (sx * 2.2, 2.0, 0), 2, solid(P, "root"), extend=0.3)
        for f in range(3):
            rod(m, lg, (sx * 2.2, 2.0, 0), (sx * 2.2 + (f - 1) * 1.6, 0.4, -2.0 + abs(f - 1)), 1, solid(P, "root"),
                extend=0.3)
    return m
