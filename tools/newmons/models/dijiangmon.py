"""Dijiangmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the faceless chaos god. A dark, headless, sack-like body wrapped and strapped in black belts with
gold buckles and red spikes, two great tattered brown-grey feathered wings, long coiling limbs bound in black wraps
that end in enormous grey grasping hands with red claws and a spiked bracelet, and a long whip tail. 35 blocks tall.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digidetail import feathers, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = ("a dark headless sack-like body bound in black straps with gold buckles and red spikes, tattered feather wings, "
        "long coiling bound limbs ending in huge grey grasping hands and a whip tail")
BASE = {"black": (40, 40, 52), "black_dark": (12, 12, 18), "strap": (60, 60, 70), "strap_dark": (20, 20, 26),
        "gold": (240, 190, 60), "red": (190, 30, 40), "grey": (120, 120, 134), "grey_dark": (60, 60, 70),
        "grey_light": (180, 180, 196), "feather": (140, 120, 110), "feather_dark": (60, 46, 40), "tip": (190, 40, 40),
        "steel": (200, 204, 214), "steel_dark": (100, 104, 114)}
SHINY = {"black": (110, 40, 40), "black_dark": (50, 10, 10), "feather": (220, 210, 200), "feather_dark": (140, 130, 120)}


def P(v):
    return pal(BASE, SHINY, v)


WRAP = leather(P, "black", "black_dark", stitch="strap")
HAND = skin(P, "grey", dark="grey_dark", light="grey_light")


def strapf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "up" and (y % 5.0) < 1.0:
        if abs(x) < 0.8 and face == "north":
            return tone(p["gold"], face), None
        return tone(p["strap"], face), None
    return WRAP(x, y, z, face, variant, box=box, **k)


def coil(m, bone, pts, t):
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bone, p0, p1, t, strapf, extend=0.6)


def hand(m, bone, c, sx, up):
    m.round_box(bone, c[0], c[2], 2.6, 2.6, c[1] - 2.0, c[1] + 2.0, HAND, cut=1)
    for j in range(4):
        base = (c[0] + (j - 1.5) * 1.3, c[1] + 2.0 * up, c[2])
        pts = [base, (base[0] + sx * 0.6, base[1] + 3.6 * up, base[2] - 1.0),
               (base[0] + sx * 0.4, base[1] + 6.0 * up, base[2] - 3.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bone, p0, p1, 1, HAND, extend=0.4)
        spike(m, bone, pts[-1], (0, up * 0.6, -1), 0.8, 2.0, solid(P, "red"))


def build():
    m = Model("dijiangmon")
    top = m.bone("dijiangmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 34, 0))
    for i, (r, y) in enumerate(((5.0, 30.0), (6.6, 34.0), (7.0, 38.0), (6.4, 42.0), (5.0, 46.0))):
        m.round_box(bd, 0, 0, r, r * 0.8, y, y + 4.4, strapf, cut=max(1, round(r * 0.3)))    # sack-like body
    hd = m.bone("head", bd, (0, 48, 0))
    m.round_box(hd, 0, 0, 3.4, 3.0, 48.0, 51.0, strapf, cut=1)
    for i in range(12):                                                                     # red spikes
        ang = i * 2.1
        y = 32.0 + (i * 5) % 16
        d = (math.sin(ang), 0.4, math.cos(ang))
        spike(m, bd, (6.0 * d[0], y, 4.6 * d[2]), d, 1.0, 4.0, solid(P, "red"), tip=0.25)
    for side in (1, -1):                                                                    # tattered wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 44.0, 3.0))
        feather_wing(m, wb, (side * 4.0, 44.0, 3.0), 22.0, 12.0, 2,
                     feathers(P, "feather", "feather_dark", size=(1.4, 3.0), tip="tip"), side=side, sweep=30,
                     droop=-6.0)
    al = m.bone("arm_left", bd, (6, 42, 0))                                                 # raised coiling arm
    pts = [(6.0, 42.0, 0), (12.0, 46.0, -2.0), (16.0, 52.0, -4.0), (18.0, 56.0, -4.0)]
    coil(m, al, pts, 3)
    hand(m, al, (18.0, 56.0, -4.0), 1, 1)
    ar = m.bone("arm_right", bd, (-6, 38, 0))                                               # hanging coiling arm
    pts = [(-6.0, 38.0, 0), (-12.0, 30.0, -2.0), (-12.0, 18.0, 0.0), (-14.0, 10.0, -2.0)]
    coil(m, ar, pts, 3)
    for j in range(5):
        a_ = math.radians(j * 72)
        spike(m, ar, (-14.0 + 2.4 * math.cos(a_), 12.0, -2.0 + 2.4 * math.sin(a_)), (math.cos(a_), 0, math.sin(a_)),
              0.8, 2.0, solid(P, "gold"))                                                    # spiked bracelet
    hand(m, ar, (-14.0, 8.0, -2.0), -1, -1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                     # bound legs
        lg = m.bone(nm, top, (sx * 3.0, 30.0, 0))
        coil(m, lg, [(sx * 3.0, 31.0, 0), (sx * 6.0, 20.0, 2.0), (sx * 8.0, 10.0, -2.0), (sx * 7.0, 2.0, -4.0)], 3)
        for j in range(3):
            spike(m, lg, (sx * 7.0 + (j - 1) * 1.0, 1.4, -4.6), (0, -0.4, -1), 0.8, 3.0, solid(P, "red"), tip=0.2)
    tl = m.bone("tail", bd, (0, 30, 4))
    coil(m, tl, [(0, 30.0, 4.0), (3.0, 22.0, 10.0), (9.0, 14.0, 12.0), (15.0, 10.0, 8.0), (19.0, 12.0, 2.0)], 2)
    return m
