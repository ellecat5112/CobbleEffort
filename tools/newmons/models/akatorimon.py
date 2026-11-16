"""Akatorimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a fierce giant rooster. A round body of white feathers, a great fan of tail and wing feathers
whose tips burn red and orange in zigzag flames, a red zigzag comb and a hanging red wattle, a gaping yellow beak, a
scarred red eye, shaggy feathered thighs and scaly pink legs ending in long red talons. 15 blocks tall.

Front is -z, y is up. 44 units tall (the tail fan); Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import cutout, eye, feathers, local, mix, scales, skin, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 1.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = ("a fierce giant rooster: round white feathered body, a great fan of fire-tipped tail and wing feathers, a red "
        "zigzag comb and wattle, a gaping yellow beak, a scarred red eye, shaggy feathered thighs and scaly legs with "
        "long red talons")

BASE = {"white": (250, 248, 244), "white_dark": (200, 196, 196), "shaft": (226, 220, 214), "red": (220, 44, 36),
        "red_dark": (150, 20, 20), "orange": (250, 150, 40), "yellow": (250, 210, 60), "beak": (246, 200, 50),
        "beak_dark": (190, 130, 30), "mouth": (200, 50, 60), "leg": (232, 180, 170), "leg_dark": (170, 110, 104),
        "talon": (200, 40, 40), "eye": (230, 40, 40), "pupil": (24, 18, 18), "scar": (150, 30, 40)}
SHINY = {"white": (60, 60, 70), "white_dark": (30, 30, 36), "shaft": (90, 90, 100), "red": (60, 120, 240),
         "red_dark": (30, 70, 170), "orange": (90, 200, 250), "yellow": (190, 240, 255), "talon": (60, 120, 240)}


def P(v):
    return pal(BASE, SHINY, v)


PLUME = feathers(P, "white", "white_dark", shaft="shaft", size=(2.6, 3.8), flow=(0, -1))
LEG = scales(P, "leg", "leg_dark", size=1.0)


def firetip(x, y, z, face, variant, box=None, **k):
    """A long feather: white, its outer end burning red and orange in a zigzag edge."""
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)            # 0 at the root
    u, v, W, H = local(x, y, z, face, box)
    zig = 0.62 + 0.08 * abs(((u + v) * 1.4) % 2 - 1)
    if t > zig:
        col = mix(p["orange"], p["red"], (t - zig) / (1 - zig))
    elif t > zig - 0.06:
        col = p["yellow"]
    else:
        col = p["white"] if (u * 3) % 1 > 0.12 else p["white_dark"]
    return tone(col, face), None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 3.0, y - 33.0, 1.1, "eye", lid="red_dark")
        if c is not None:
            return c, None
        if abs((z + 3.0) - (y - 33.0) * 0.6) < 0.25 and abs(y - 33.0) < 2.0:
            return p["scar"], None                                    # the scar across its eye
    return PLUME(x, y, z, face, variant, box=box, **k)


def comb(x, y, z, face, box):
    """A zigzag comb on an yz plane."""
    u, v, W, H = local(x, y, z, face, box)
    return v < H * (0.45 + 0.55 * abs(((u / W) * 4) % 2 - 1))


def build():
    m = Model("akatorimon")
    top = m.bone("akatorimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for y0, y1, r, rz in ((11, 13, 4.0, 4.6), (13, 16, 5.6, 6.0), (16, 21, 6.4, 6.8), (21, 24, 5.6, 6.0),
                          (24, 26, 4.2, 4.6)):
        m.round_box(bd, 0, 0.6, r, rz, y0, y1, PLUME, cut=max(1, round(r * 0.35)))       # the round body
    m.round_box(bd, 0, -2.0, 3.2, 3.0, 24.0, 30.0, PLUME, cut=1)                         # neck ruff
    hd = m.bone("head", bd, (0, 30, -2))
    m.round_box(hd, 0, -2.6, 2.6, 2.8, 29.5, 35.5, headf, cut=1)
    m.box(hd, -1.3, 31.4, -9.0, 1.3, 33.4, -5.0, solid(P, "beak"), rotation=(-8, 0, 0), pivot=(0, 32, -5))  # beak
    jw = m.bone("jaw", hd, (0, 31.2, -5.2))
    m.box(jw, -1.1, 29.8, -8.2, 1.1, 31.2, -5.2, solid(P, "beak_dark"), rotation=(22, 0, 0), pivot=(0, 31.2, -5.2))
    m.box(hd, -0.9, 30.6, -7.6, 0.9, 31.4, -5.4, solid(P, "mouth"))
    m.box(hd, 0, 35.0, -6.0, 0, 39.5, 1.0, cutout(comb, solid(P, "red")))                 # the comb
    m.box(hd, -0.6, 35.0, -5.0, 0.6, 36.2, 0.4, solid(P, "red"))
    m.box(hd, -0.6, 27.0, -5.6, 0.6, 30.0, -4.2, skin(P, "red", dark="red_dark"))        # wattle
    # the tail fan: rings of long fire-tipped feathers
    tf = m.bone("tail", bd, (0, 20, 5))
    for ring, (n, L, spread) in enumerate(((11, 15.0, 150), (9, 11.0, 120))):
        for i in range(n):
            ang = math.radians(-spread / 2 + spread * i / (n - 1))
            d = (math.sin(ang), math.cos(ang) * 0.95 + 0.25, 0.55 - ring * 0.2)
            nrm = math.sqrt(sum(c * c for c in d))
            tip = tuple(c + dd / nrm * L for c, dd in zip((0, 19.0, 5.5), d))
            rod(m, tf, (0, 19.0, 5.5 + ring), tip, 1, firetip, extend=0.2, t2=3)
    # wings: fans of fire-tipped feathers swept back and out
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 6.0, 21.0, 0.0))
        m.round_box(w, sx * 6.6, 0.6, 1.4, 4.0, 16.0, 23.0, PLUME, cut=1)
        for i in range(7):
            ang = math.radians(-30 + i * 14)
            tip = (sx * (8.0 + 7.0 * math.cos(ang)), 20.0 + 7.0 * math.sin(ang), 6.0 + i * 0.6)
            rod(m, w, (sx * 7.0, 19.0, 0.5 + i * 0.4), tip, 1, firetip, extend=0.2, t2=2)
    # legs: shaggy feathered thighs, scaly legs, long red talons and a spur
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 13.0, 1.0))
        m.round_box(lg, sx * 2.8, 1.0, 2.4, 2.6, 8.0, 14.0, PLUME, cut=1)
        for i in range(5):                                                                # shaggy fringe
            spike(m, lg, (sx * 2.8 + (i - 2) * 0.9, 8.4, -0.6 + (i % 2) * 2.4), (0, -1, 0.1), 1.0, 2.0, PLUME, tip=0.3)
        rod(m, lg, (sx * 2.8, 8.4, 1.0), (sx * 2.9, 1.2, 0.0), 2, LEG, extend=0.3)
        for t, d in ((0, (0, -0.2, -1)), (1, (0.5, -0.2, -0.8)), (-1, (-0.5, -0.2, -0.8))):
            rod(m, lg, (sx * 2.9, 1.0, 0.0), (sx * 2.9 + d[0] * 3, 0.5, -3.0 + abs(t)), 1, LEG, extend=0.2)
            spike(m, lg, (sx * 2.9 + d[0] * 3, 0.5, -3.0 + abs(t)), d, 0.9, 2.2, solid(P, "talon"), tip=0.2)
        spike(m, lg, (sx * 2.9, 3.0, 0.9), (0, -0.3, 1), 0.8, 1.8, solid(P, "talon"), tip=0.2)    # spur
    return m
