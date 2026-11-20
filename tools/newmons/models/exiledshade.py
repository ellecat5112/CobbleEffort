"""Exiled Shade (Ghost/Rock), the ancient paradox Giratina, built from boxes after @ArtWithAlfred's art (no name given;
our name).

A long, low beast of grey stone on six stubby legs, its feet and ankles marked with gold, a dark red band along its
belly. Over its back heaves a vast mound of living shadow, black and ragged at its edges, pierced by red spikes. Curved
gold plates claw down over its shoulders like Giratina's ribs, its low head wears Giratina's golden mask round a red
eye, and its grey tail stretches far behind.

Shiny: pale stone, a deep violet shadow and silver plates.

Front is -z, y is up. 37 units tall (to the spikes); about 4.2 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import slab_z
from _pgen1 import smooth_path
from _regi import _hash, ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 37
SCALE = round(4.2 * 16 / HEIGHT, 3)
HITBOX = [3.2, 30 / 16]
KIND = "quadruped"
K = 3
LOOK = ("a long low six-legged beast of grey stone under a vast ragged mound of living shadow pierced by red spikes, "
        "with curved gold rib plates, gold-marked feet and Giratina's golden mask on its low head")

BASE = {"stone": (176, 178, 186), "stone_dark": (122, 124, 136), "stone_light": (214, 216, 222),
        "crack": (70, 70, 80), "shadow": (34, 32, 38), "shadow_light": (62, 58, 70), "shadow_rim": (110, 40, 50),
        "red": (150, 36, 44), "red_dark": (100, 24, 32), "spike": (196, 72, 70), "gold": (234, 196, 70),
        "gold_dark": (180, 136, 40), "eye": (230, 40, 40)}
SHINY = {"stone": (222, 220, 214), "stone_dark": (170, 168, 160), "stone_light": (244, 242, 236),
         "shadow": (52, 30, 70), "shadow_light": (86, 56, 110), "shadow_rim": (140, 70, 170), "gold": (210, 216, 230),
         "gold_dark": (150, 156, 176)}
BY = 11.0      # body centre height


def P(v):
    return pal(BASE, SHINY, v)


def stonef(x, y, z, face, variant, **k):
    """Grey stone with a few dark cracks; a dark red band low along its belly."""
    p = P(variant)
    if face in ("east", "west", "down") and y < BY - 3.0 and abs(z) < 17.0:
        return tone(p["red"] if face != "down" else p["red_dark"], face), None
    if abs(math.sin(x * 0.7 + z * 0.35) + math.sin(z * 0.5 - y * 0.6)) < 0.06:
        return p["crack"], None
    if face == "up":
        return p["stone_light"], None
    return lit(p["stone"], face, y, BY, 7), None


def legf(x, y, z, face, variant, **k):
    """A stubby leg: grey, with gold diamonds on its ankle."""
    p = P(variant)
    if 3.0 < y < 5.4 and face in ("north", "east", "west"):
        u = (x if face == "north" else z) % 2.4 - 1.2
        if abs(u) + abs(y - 4.2) * 0.9 < 0.9:
            return p["gold"], None
    return tone(p["stone"], face), None


def goldf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        return mix(p["gold"], (255, 255, 255), 0.2), None
    return tone(p["gold"] if face != "down" else p["gold_dark"], face), None


def shadowf(x, y, z, face, variant, **k):
    """Living shadow: near-black, a little lighter in wisps, reddish at its lower rim."""
    p = P(variant)
    if y < BY + 4.5:
        return p["shadow_rim"], None
    if math.sin(x * 0.5 + y * 0.3) * math.sin(z * 0.45 - y * 0.25) > 0.55:
        return p["shadow_light"], None
    return p["shadow"], None


def spikef(x, y, z, face, variant, **k):
    return tone(P(variant)["spike"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 28.0, y - 8.6) < 1.0:
        return p["eye"], p["eye"]
    return stonef(x, y, z, face, variant)


def build() -> Model:
    m = Model("exiledshade")
    top = m.bone("exiledshade", None, (0, 0, 0))
    bd = m.bone("body", top, (0, BY, 0))
    for z0, z1, rx, ry in ((-18, -13, 5.0, 4.4), (-13, -7, 6.0, 5.0), (-7, 0, 6.4, 5.2), (0, 7, 6.4, 5.2),
                           (7, 13, 6.0, 4.8), (13, 18, 5.0, 4.2)):
        slab_z(m, bd, 0, BY, z0, z1, rx, ry, stonef)                               # the long low body
    # the mound of living shadow: overlapping lumps, ragged at the edges
    for i, (cx, cy, cz, rx, ry, rz) in enumerate(((0, 21, -2, 8.6, 9.0, 10.0), (0, 27, 0, 6.6, 6.4, 7.4),
                                                  (-3, 16, 8, 8.0, 5.6, 7.0), (3, 17, -10, 7.8, 5.6, 6.0),
                                                  (0, 31, 2, 4.0, 3.6, 4.4), (5, 23, 5, 5.0, 5.0, 5.0),
                                                  (-5, 24, -5, 5.0, 5.0, 5.0))):
        ellipsoid(m, bd, cx, cy, cz, rx, ry, rz, shadowf, step=1)
    for i in range(9):                                                           # ragged wisps at its edges
        a = math.radians(i * 40 + 10)
        base = (math.cos(a) * 8.0, 15.0 + 6.0 * _hash(i, 2), math.sin(a) * 9.0)
        d = (math.cos(a), 0.3 + 0.6 * _hash(i, 3), math.sin(a))
        spike(m, bd, base, d, 3.0, 4.0 + 3.0 * _hash(i, 4), shadowf, tip=1.6)
    for base, d, h in (((0, 33.0, 2.0), (0.1, 1, 0.1), 6.0), ((-4.0, 28.0, -6.0), (-0.4, 1, -0.3), 5.0),
                       ((5.0, 27.0, 6.0), (0.5, 1, 0.2), 5.0), ((-6.0, 22.0, 9.0), (-0.8, 0.7, 0.4), 4.4)):
        spike(m, bd, base, d, 2.4, h, spikef, tip=1.0)                             # red spikes through the shadow
    for sx in (-1, 1):                                                           # curved gold rib plates
        for i, z in enumerate((-12.0, -7.0, -2.0)):
            a0 = (sx * 5.6, BY + 5.0, z)
            a1 = (sx * 8.0, BY + 1.0, z - 2.4)
            rod(m, bd, a0, a1, 2.6, goldf, extend=0.6, t2=1.2)
            spike(m, bd, a1, (sx * 0.4, -1, -0.6), 2.2, 3.4 - i * 0.4, goldf, tip=0.8)
    hd = m.bone("head", bd, (0, 8.0, -18.0))                                        # low head in a golden mask
    m.round_box(hd, 0, -23.0, 4.6, 5.4, 3.6, 11.4, headf, cut=1)
    m.round_box(hd, 0, -29.0, 3.2, 2.8, 3.6, 8.6, headf, cut=0.6)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 1.2, sx * 5.6))
        m.box(hd, x0, 4.4, -30.4, x1, 12.8, -21.6, goldf, rotation=(0, sx * 12, 0), pivot=(sx * 2.4, 8.0, -25.0))
        spike(m, hd, (sx * 4.6, 11.8, -22.6), (sx * 0.6, 0.8, 0.6), 2.2, 5.6, goldf, tip=1.0)
        spike(m, hd, (sx * 3.6, 4.4, -29.0), (sx * 0.4, -0.6, -1), 2.0, 4.4, goldf, tip=0.8)
    m.box(hd, -1.4, 9.0, -31.6, 1.4, 14.0, -25.0, goldf)                             # the mask's centre crest
    for nm, sx, z in (("leg_front_left", 1, -11.0), ("leg_front_right", -1, -11.0), ("leg_mid_left", 1, 0.0),
                      ("leg_mid_right", -1, 0.0), ("leg_back_left", 1, 10.0), ("leg_back_right", -1, 10.0)):
        hip = (sx * 5.6, BY - 2.0, z)
        lg = m.bone(nm, top, hip)
        rod(m, lg, hip, (sx * 7.4, 5.0, z - 0.6), 4.0, legf, extend=0.8)
        rod(m, lg, (sx * 7.4, 5.6, z - 0.6), (sx * 7.8, 1.4, z - 1.2), 3.6, legf, extend=0.6)
        m.box(lg, sx * 7.8 - 2.2, 0, z - 3.6, sx * 7.8 + 2.2, 2.2, z + 1.0, legf)
        for c in (-1, 0, 1):
            spike(m, lg, (sx * 7.8 + c * 1.4, 0.8, z - 3.4), (c * 0.3, -0.2, -1), 1.2, 2.2, goldf, tip=0.5)
    tl = m.bone("tail", bd, (0, BY, 17.0))
    pts = smooth_path([(0, BY, 16.0), (2.0, BY - 1.0, 23.0), (5.0, BY - 3.0, 30.0), (9.0, BY - 5.0, 36.0),
                       (14.0, BY - 6.0, 40.0)], 10)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, a, b, max(1.0, round((6.0 - 5.0 * i / (len(pts) - 2)) * 2) / 2), stonef, extend=0.8)
    return m
