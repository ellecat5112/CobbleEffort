"""Kabuterimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the giant beetle: a hulking dark-blue armoured insect with a long curved horn, a pale skull-like
face with red eyes and a fanged maw, four clawed arms, segmented legs with spiked joints, ribbed carapace plates and
two pairs of long translucent veined wings. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, cutout, local, metal, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a hulking dark-blue armoured beetle with a long curved horn, a pale skull face, four clawed arms and two pairs of veined wings"
BASE = {"blue": (50, 70, 150), "blue_dark": (16, 22, 70), "blue_light": (120, 150, 230), "grey": (150, 150, 170),
        "grey_dark": (60, 60, 80), "bone": (220, 220, 210), "eye": (230, 40, 40), "mouth": (160, 30, 40),
        "wing": (220, 230, 240, 150), "wing_vein": (150, 160, 190, 210), "claw": (200, 200, 216)}
SHINY = {"blue": (180, 60, 50), "blue_dark": (90, 14, 10), "blue_light": (240, 140, 120)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL = armour(P, "blue", "blue_dark", light="blue_light", trim="grey_dark", trim_w=0.2)


def ribf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y % 2.2) < 0.4:
        return tone(p["blue_dark"], face), None
    return SHELL(x, y, z, face, variant, box=box, **k)


def wing_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6), v / max(H, 1e-6) - 0.5
    return abs(b) < 0.5 * math.sqrt(max(0.0, 1 - a * a)) + 0.02


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return (p["wing_vein"] if (u % 3.0) < 0.3 or abs(v - H / 2) < 0.25 else p["wing"]), None


def build():
    m = Model("kabuterimon")
    top = m.bone("kabuterimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, 1.0, 6.0, 6.4, 18.0, 34.0, ribf, cut=2)                          # carapace
    m.round_box(bd, 0, 4.0, 5.0, 4.6, 12.0, 20.0, ribf, cut=2)                          # abdomen
    hd = m.bone("head", bd, (0, 34, -4))
    m.round_box(hd, 0, -5.0, 3.0, 3.6, 31.0, 37.0, solid(P, "bone"), cut=1)             # skull face
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 34.4, -8.7, max(sx * 0.8, sx * 2.2), 35.4, -8.5, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.2, 31.0, -8.0), (sx * 0.3, -1, -0.4), 0.9, 3.0, solid(P, "bone"), tip=0.8)
    m.box(hd, -1.4, 31.4, -8.7, 1.4, 32.4, -8.5, solid(P, "mouth"))
    pts = [(0, 36.0, -4.0), (0, 42.0, -8.0), (0, 47.0, -7.0), (0, 48.0, -3.0)]          # long curved horn
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 3 - j, SHELL, extend=0.6)
    for side in (1, -1):                                                              # two pairs of wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 32.0, 5.0))
        for j, (ln, h, rz) in enumerate(((26.0, 7.0, 30), (20.0, 6.0, 5))):
            x0, x1 = sorted((side * 3.0, side * (3.0 + ln)))
            m.box(wb, x0, 32.0 - h / 2, 5.4 + j, x1, 32.0 + h / 2, 5.4 + j, cutout(wing_in, wingf),
                  rotation=(0, side * -20, side * rz), pivot=(side * 3.0, 32.0, 5.4 + j))
    for k_, (y0, nm_l, nm_r) in enumerate(((30.0, "arm_left", "arm_right"), (24.0, "arm2_left", "arm2_right"))):
        for sx, nm in ((1, nm_l), (-1, nm_r)):                                       # four clawed arms
            ab = m.bone(nm, bd, (sx * 6.0, y0, -2.0))
            el = (sx * 12.0, y0 - 2.0, -6.0)
            rod(m, ab, (sx * 6.0, y0, -2.0), el, 2, SHELL, extend=0.6)
            spike(m, ab, el, (sx, 0.4, 0.4), 0.9, 3.0, solid(P, "claw"), tip=0.8)
            hand = (sx * 13.0, y0 - 9.0, -9.0)
            rod(m, ab, el, hand, 2, SHELL, extend=0.4)
            for j in range(3):
                spike(m, ab, hand, (sx * 0.3 + (j - 1) * 0.3, -1, -0.6), 0.9, 3.4, solid(P, "claw"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # segmented legs
        lg = m.bone(nm, bd, (sx * 3.6, 14.0, 2.0))
        kn = (sx * 6.0, 7.0, -3.0)
        rod(m, lg, (sx * 3.6, 14.0, 2.0), kn, 2, SHELL, extend=0.6)
        spike(m, lg, kn, (sx * 0.6, 0.2, -1), 0.9, 2.6, solid(P, "claw"), tip=0.8)
        rod(m, lg, kn, (sx * 6.0, 0.6, 1.0), 2, SHELL, extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 6.0, 0.6, 1.0), ((j - 1) * 0.5, -0.1, -1), 0.9, 3.0, solid(P, "claw"), tip=0.8)
    return m
