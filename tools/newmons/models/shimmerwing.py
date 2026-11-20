"""Shimmer Wing (Fire/Fairy), the ancient paradox Ho-Oh, built from boxes after @goldmills_'s art (the art's own name).

A shaggy crouching dinosaur of a Ho-Oh in scarlet plumage streaked with crimson. A great curling crest of gold
sweeps up from its head over a lime green tuft, its yellow beak gapes, and its short feathered arms end in dark blue
claws. Beneath it spreads a skirt of long tail feathers fading from lime green to white; its thick blue legs end in
white talons; and from its back rises a long tail that ends in a great brush of golden plumes.

Shiny: golden plumage with a silver skirt.

Front is -z, y is up. 50 units tall; about 3.2 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import plane, scales, solid as dsolid
from _pgen1 import CLEAR, ribbon, smooth_path, tri
from _regi import ellipsoid
from _route import mix, pal, tone

HEIGHT = 50
SCALE = round(3.2 * 16 / HEIGHT, 3)
HITBOX = [1.8, HEIGHT / 16]
KIND = "biped"
K = 3
LOOK = ("a shaggy crouching scarlet dinosaur-bird with a curling gold crest, a lime tuft, dark blue claws, a skirt of "
        "lime-to-white tail feathers and a long tail ending in a golden brush")

BASE = {"red": (232, 64, 40), "red_dark": (178, 34, 30), "red_light": (250, 120, 80), "gold": (240, 182, 60),
        "gold_dark": (196, 132, 40), "gold_light": (255, 222, 130), "lime": (176, 214, 86), "lime_dark": (120, 168, 60),
        "white": (242, 244, 236), "navy": (52, 60, 112), "navy_dark": (34, 40, 80), "talon": (240, 240, 244),
        "beak": (246, 206, 70), "mouth": (150, 40, 50), "eye": (40, 20, 20), "brush": (200, 150, 80),
        "brush_dark": (150, 104, 54)}
SHINY = {"red": (240, 200, 70), "red_dark": (200, 150, 40), "red_light": (255, 230, 140), "lime": (210, 214, 226),
         "lime_dark": (160, 166, 186), "navy": (110, 60, 40), "navy_dark": (80, 40, 26)}


def P(v):
    return pal(BASE, SHINY, v)


def plumage(key, dark, light):
    """Shaggy scarlet plumage: long overlapping feathers with darker streaks."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        a, b = plane(x, y, z, face)
        row = math.floor(b / 1.8)
        aa = a + (0.7 if row % 2 else 0)
        lu = ((aa / 1.4) % 1.0) * 2 - 1
        lv = (b / 1.8) % 1.0
        if lv < 0.2 + 0.25 * lu * lu:
            c = mix(p[key], p[dark], 0.38)
        elif abs(lu) < 0.12:
            c = p[light]
        else:
            c = p[key]
        return tone(c, face), None
    return s


RED = plumage("red", "red_dark", "red_light")
LEG = scales(P, "navy", "navy_dark", size=1.1, rim_mix=0.5)


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 5.0, y - 40.8) < 0.55:
        return p["eye"], None
    return RED(x, y, z, face, variant, **k)


def skirtf(cx, cy):
    """A fan of long tail feathers hanging below the body (an xy plane): lime at the root fading to white."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        dx, dy = x - cx, cy - y
        if dy < 0:
            return CLEAR
        a = math.degrees(math.atan2(dx, dy))
        if abs(a) > 62:
            return CLEAR
        f = (a + 62) / 124 * 9
        R = 12.0 + 3.0 * (1 - abs(a) / 62) - 2.6 * abs((f % 1.0) - 0.5) * 2
        r = math.hypot(dx, dy)
        if r > R:
            return CLEAR
        if abs((f % 1.0) - 0.5) < 0.06:
            return p["lime_dark"], None
        t = r / R
        return (p["lime"] if t < 0.55 else mix(p["lime"], p["white"], (t - 0.55) / 0.45)), None
    return s


def brushf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    return tone(p["gold_light"] if d > 0.7 else (p["brush"] if d > 0.3 else p["brush_dark"]), face), None


def build() -> Model:
    m = Model("shimmerwing")
    top = m.bone("shimmerwing", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 24, 1))
    ellipsoid(m, bd, 0, 25.0, 1.0, 5.6, 6.6, 7.0, RED, step=1)                       # shaggy scarlet body
    nk = m.bone("neck", bd, (0, 29, -4.6))
    neck = smooth_path([(0, 28.5, -4.0), (0, 32.5, -6.4), (0, 36.5, -6.6), (0, 39.4, -5.6)], 6)
    ribbon(m, nk, neck, [4.6, 4.4, 4.2, 3.9, 3.7, 3.5, 3.4], RED, extend=1.0)
    for q in neck[1:6]:                                                            # shaggy ruff of neck feathers
        for sx in (-1, 1):
            spike(m, nk, (sx * 1.6, q[1], q[2] + 0.4), (sx * 0.9, -0.6, 0.6), 1.4, 3.2, RED, tip=0.6)
    hd = m.bone("head", nk, (0, 40, -5.6))
    m.round_box(hd, 0, -5.4, 2.6, 3.0, 39.0, 43.2, headf, cut=1)                   # head
    rod(m, hd, (0, 41.4, -8.0), (0, 39.8, -11.6), 2.0, dsolid(P, "beak"), extend=0.4, t2=1.8)   # gaping beak
    spike(m, hd, (0, 40.0, -11.4), (0, -1, -0.3), 1.4, 1.6, dsolid(P, "beak"))
    rod(m, hd, (0, 39.4, -7.6), (0, 37.8, -10.4), 1.6, dsolid(P, "beak"), extend=0.3, t2=1.0)
    m.box(hd, -0.7, 38.4, -10.0, 0.7, 40.6, -7.6, dsolid(P, "mouth"))
    for sx in (-0.8, 0.0, 0.8):                                                     # lime tuft on the brow
        spike(m, hd, (sx, 42.6, -6.6), (sx * 0.4, 0.8, -1), 1.2, 3.0, dsolid(P, "lime"), tip=0.5)
    crest = smooth_path([(0, 43.0, -4.6), (0, 47.0, -4.0), (0, 49.6, -1.6), (0, 49.0, 1.6), (0, 46.6, 2.4)], 10)
    for i, (a, b) in enumerate(zip(crest, crest[1:])):                             # the curling gold crest
        w = 4.4 - 2.4 * i / len(crest)
        rod(m, hd, a, b, w, dsolid(P, "gold" if i % 3 else "gold_light"), extend=0.8, t2=max(1.4, w * 0.8))
    for sx in (-1, 1):
        rod(m, hd, (sx * 1.6, 43.0, -3.6), (sx * 3.0, 46.4, -1.0), 1.8, dsolid(P, "gold_dark"), extend=0.4)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                           # feathered arms, navy claws
        ar = m.bone(nm, bd, (sx * 4.2, 28.0, -4.0))
        el, hand = (sx * 6.0, 24.6, -6.0), (sx * 5.4, 22.6, -8.6)
        rod(m, ar, (sx * 4.2, 28.0, -4.0), el, 3.0, RED, extend=0.6)
        rod(m, ar, el, hand, 2.2, RED, extend=0.5)
        for f in (0, 1, 2):
            spike(m, ar, (sx * 5.4 + (f - 1) * 0.7, 22.6, -8.6), ((f - 1) * 0.3, -0.7, -1), 0.9, 2.6,
                  dsolid(P, "navy"), tip=0.4)
        spike(m, ar, (sx * 6.2, 24.6, -5.6), (sx * 0.4, -0.8, 0.6), 1.6, 4.0, RED, tip=0.6)
    m.box(bd, -15.0, 4.0, -5.8, 15.0, 21.0, -5.8, skirtf(0.0, 20.6))               # lime-to-white feather skirt
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):                           # thick navy legs, white talons
        lg = m.bone(nm, bd, (sx * 3.2, 21, 2.0))
        m.round_box(lg, sx * 3.2, 2.0, 2.6, 3.0, 14.6, 22.0, RED, cut=1)
        knee, ank = (sx * 3.4, 14.4, 0.4), (sx * 3.6, 6.4, 3.0)
        rod(m, lg, (sx * 3.3, 15.4, 1.6), knee, 2.6, LEG, extend=0.5)
        rod(m, lg, knee, ank, 2.4, LEG, extend=0.5)
        rod(m, lg, ank, (sx * 3.6, 1.4, 0.4), 2.2, LEG, extend=0.5)
        m.box(lg, sx * 3.6 - 1.8, 0, -1.2, sx * 3.6 + 1.8, 2.0, 2.0, LEG)
        for d in (-0.5, 0.0, 0.5):
            rod(m, lg, (sx * 3.6 + d, 1.0, -1.0), (sx * 3.6 + d * 3.0, 1.0, -3.8), 1.2, LEG, extend=0.3)
            spike(m, lg, (sx * 3.6 + d * 3.2, 1.0, -3.8), (d * 0.3, -0.5, -1), 1.2, 2.4, dsolid(P, "talon"), tip=0.5)
        spike(m, lg, (sx * 3.6, 1.2, 2.0), (0, -0.3, 1), 1.0, 2.0, dsolid(P, "talon"))
    tl = m.bone("tail", bd, (0, 26.0, 7.6))                                        # long tail with a golden brush
    path = smooth_path([(0, 26.0, 7.6), (0, 28.0, 14.0), (0, 31.5, 19.5), (0, 35.5, 22.5), (0, 39.0, 23.0)], 12)
    ribbon(m, tl, path, [4.0 - 1.8 * i / len(path) for i in range(len(path))], RED, extend=0.8)
    end = path[-1]
    for i in range(14):
        ang = math.radians(-80 + i * (160 / 13))
        d = (math.sin(ang) * 0.9, 0.7 + 0.3 * math.cos(ang), 0.6 - 0.2 * math.cos(ang))
        spike(m, tl, end, d, 2.2, 9.5 + 2.0 * tri(i / 3.0), brushf, tip=0.7)
    return m
