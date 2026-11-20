"""Proto Lugia (Water/Dragon), the ancient paradox Lugia, built from boxes after @indigo_region's art (the art's own
name).

A gaunt, spiny Lugia of dark slate violet streaked with pale blue, its belly a long plated band of lilac. Pale bone
spikes, brown at their roots, jut from its back, its flanks and its tail; its wings are great hands of four long
feathered fingers, each ending in a bone-white claw, and its long tail trails three fin spikes. Its head is narrow and
fierce, with a pale beak, red eyes and swept-back horns.

Shiny: dusk-orange with pale gold spikes.

Front is -z, y is up. 58 units tall; about 4.4 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR, inside, ribbon, smooth_path
from _regi import ellipsoid, lit
from _route import pal, tone

HEIGHT = 58
SCALE = round(4.4 * 16 / HEIGHT, 3)
HITBOX = [2.4, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a gaunt dark violet Lugia with a lilac plated belly, bone spikes along its back, flanks and tail, and great "
        "wings of four feathered fingers tipped with bone-white claws")

BASE = {"slate": (106, 104, 158), "slate_dark": (70, 68, 110), "slate_light": (156, 158, 210), "belly": (192, 146, 206),
        "belly_dark": (150, 104, 168), "bone": (226, 224, 230), "bone_root": (136, 116, 114), "beak": (214, 206, 214),
        "eye": (230, 50, 60), "claw": (232, 230, 234)}
SHINY = {"slate": (190, 112, 70), "slate_dark": (140, 74, 44), "slate_light": (232, 168, 112), "belly": (246, 210, 150),
         "belly_dark": (210, 166, 110), "bone": (250, 236, 170), "bone_root": (170, 120, 70)}
CY = 34.0


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def hidef(x, y, z, face, variant, **k):
    """Dark slate with long pale streaks; a lilac plated band down the belly."""
    p = P(variant)
    if face == "north" and abs(x) < 2.6 and 24 < y < 46:
        return lit(p["belly_dark"] if (y % 2.2) < 0.4 else p["belly"], face, y, CY, 9), None
    if face in ("east", "west", "south") and ((y * 0.6 + z * 0.3) % 3.4) < 0.35:
        return lit(p["slate_light"], face, y, CY, 9), None
    return lit(p["slate"], face, y, CY, 9), None


def fingerf(x, y, z, face, variant, **k):
    """A wing finger: dark slate with a pale streak along it (rods: z runs along the finger)."""
    p = P(variant)
    if face in ("up", "north") and abs(x - 0.0) < 10 and (abs(y) < 0.35):
        return tone(p["slate_light"], face), None
    return tone(p["slate"] if face != "down" else p["slate_dark"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 4.6, y - 54.8) < 0.6:
        return p["eye"], p["eye"]
    return lit(p["slate"], face, y, 54, 2), None


def bone(m, bone_, base, d, w, h):
    """A bone spike: a brown root and a long pale point."""
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    mid = tuple(b + uu * h * 0.3 for b, uu in zip(base, u))
    rod(m, bone_, base, mid, w, solid("bone_root"), extend=0.2)
    spike(m, bone_, mid, u, w * 0.9, h * 0.7, solid("bone"), tip=max(0.6, w * 0.35))


def membranef(poly, sx):
    """The wing's broad web between its fingers (an xy plane; poly in (u, y), u = sx * x)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u = sx * x
        if not inside(poly, u, y):
            return CLEAR
        if ((u * 0.5 + y * 0.8) % 4.0) < 0.5:
            return p["slate_light"], None
        return p["slate"], None
    return s


def wing(m, wg, sx):
    sh, el, wr = (sx * 5.0, 43.0, 0.5), (sx * 12.0, 47.0, 1.0), (sx * 19.0, 45.0, 1.0)
    tips = []
    rod(m, wg, sh, el, 3.6, fingerf, extend=0.8)
    rod(m, wg, el, wr, 3.2, fingerf, extend=0.8)
    bone(m, wg, (el[0], el[1] + 1.2, el[2]), (sx * 0.2, 1, 0.2), 1.6, 4.6)
    for i, (ang, L) in enumerate(((58, 15.0), (25, 17.0), (-8, 16.0), (-40, 13.0))):
        a = math.radians(ang)
        d = (sx * math.cos(a), math.sin(a), 0.15 * i)
        mid = tuple(w_ + v * L * 0.55 for w_, v in zip(wr, d))
        end = tuple(w_ + v * L for w_, v in zip(wr, d))
        rod(m, wg, wr, mid, 3.8, fingerf, extend=0.8)
        rod(m, wg, mid, end, 3.2, fingerf, extend=0.8)
        spike(m, wg, end, d, 2.6, 4.8, solid("claw"), tip=0.9)                 # bone-white claw tips
        tips.append((sx * end[0], end[1]))
    poly = [(5.0, 41.0), (12.0, 48.5), tips[0], tips[1], tips[2], tips[3], (14.0, 34.0), (6.0, 36.0)]
    x0, x1 = sorted((sx * 4.0, sx * 40.0))
    m.box(wg, x0, 28.0, 2.0, x1, 62.0, 2.0, membranef(poly, sx))


def build() -> Model:
    m = Model("protolugia")
    top = m.bone("protolugia", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    ellipsoid(m, bd, 0, CY, 0.4, 5.6, 9.8, 5.2, hidef, step=1)                     # the long upright body
    nk = m.bone("neck", bd, (0, 43, -0.6))
    neck = smooth_path([(0, 42.0, -0.4), (0, 46.5, -1.6), (0, 50.5, -2.6), (0, 53.0, -3.4)], 6)
    ribbon(m, nk, neck, [3.8, 3.5, 3.2, 3.0, 2.9, 2.8, 2.7], hidef, extend=1.0)
    for q in neck[1:6]:
        bone(m, nk, (0, q[1], q[2] + 1.2), (0, 0.4, 1), 1.2, 3.0)                  # spikes down the neck
    hd = m.bone("head", nk, (0, 53.5, -3.4))
    m.round_box(hd, 0, -4.4, 2.4, 3.2, 52.6, 56.6, headf, cut=1)                    # narrow head
    rod(m, hd, (0, 54.4, -7.2), (0, 53.4, -10.4), 1.8, solid("beak"), extend=0.3, t2=1.6)   # pale beak
    for sx in (-1, 1):
        rod(m, hd, (sx * 1.4, 56.2, -3.4), (sx * 2.2, 57.6, 0.6), 1.2, solid("slate_dark"), extend=0.3)
        spike(m, hd, (sx * 2.2, 57.6, 0.4), (sx * 0.2, 0.3, 1), 1.0, 3.0, solid("bone"), tip=0.4)   # swept horns
    for sx in (-1, 1):                                                             # bone spikes on the flanks
        for yy, zz in ((40.0, -1.0), (35.0, -1.6), (30.0, -1.0), (26.0, 0.0)):
            bone(m, bd, (sx * 4.2, yy, zz), (sx, -0.25, -0.3), 1.4, 3.6)
    for yy in (44.0, 39.0, 34.0, 29.0):                                            # and down its back
        bone(m, bd, (0, yy, 4.2), (0, 0.3, 1), 1.6, 4.2)
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):
        wing(m, m.bone(nm, bd, (sx * 5.0, 43.0, 0.5)), sx)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):                           # short dangling legs
        lg = m.bone(nm, bd, (sx * 3.0, 28.0, 0))
        rod(m, lg, (sx * 3.2, 28.0, -0.4), (sx * 4.0, 23.6, -3.2), 3.0, hidef, extend=0.6)
        rod(m, lg, (sx * 4.0, 23.6, -3.2), (sx * 3.8, 19.8, -1.0), 2.2, hidef, extend=0.5)
        for d in ((-0.5, -0.4, -1), (0.0, -0.5, -1), (0.5, -0.4, -1)):
            spike(m, lg, (sx * 3.8, 19.6, -1.4), (d[0] * sx, d[1], d[2]), 0.9, 2.4, solid("claw"), tip=0.4)
    tl = m.bone("tail", bd, (0, 25.0, 1.5))                                        # the long finned tail
    path = smooth_path([(0, 25.5, 1.6), (0, 19.0, 4.2), (2.0, 12.0, 6.4), (6.0, 6.0, 6.6), (12.0, 2.6, 5.0),
                        (19.0, 2.4, 3.0), (25.0, 4.0, 1.0)], 18)
    ribbon(m, tl, path, [4.0 - 3.0 * i / len(path) for i in range(len(path))], hidef, extend=0.8)
    for f in (0.3, 0.55, 0.8):
        q = path[int(f * (len(path) - 1))]
        bone(m, tl, (q[0], q[1] + 1.0, q[2]), (0.2, 1, 0.6), 1.8, 4.4)
    return m
