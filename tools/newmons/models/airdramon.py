"""Airdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a mythical winged serpent. A white skull-like head masked in black with a red-ringed eye, a gaping red
mouth lined with fangs, white horn-quills and a blazing mane of red, orange and yellow feathers round its face; a long
blue serpent body of overlapping scales with a pale banded belly, coiling down to a flame-tipped tail; two great ragged
wings, crimson-orange veined with darker red and fading to black at their tattered edges. 15 blocks tall.

Front is -z, y is up. 48 units tall (the wings); Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import cutout, eye, flame_inside, local, mix, mul, scales, skin, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = ("a winged serpent: a black-masked white skull head with a red-ringed eye, a gaping fanged red mouth, white "
        "horn-quills, a blazing red-orange-yellow feather mane, a long blue scaled body with a pale banded belly, a "
        "flame-tipped tail and two great ragged crimson-orange wings fading to black")

BASE = {"blue": (54, 104, 196), "blue_dark": (28, 56, 128), "blue_light": (120, 170, 236), "belly": (196, 210, 230),
        "skull": (246, 244, 238), "skull_dark": (190, 188, 184), "mask": (30, 28, 34), "mouth": (196, 36, 50),
        "tongue": (230, 90, 110), "teeth": (250, 248, 240), "eye": (220, 40, 40), "pupil": (20, 16, 18),
        "white": (255, 255, 255), "red": (214, 44, 30), "orange": (246, 136, 30), "yellow": (252, 214, 60),
        "wing": (236, 104, 40), "wing_dark": (170, 40, 26), "wing_edge": (34, 26, 30), "flame": (255, 150, 40, 220),
        "flame_core": (255, 230, 120, 235)}
SHINY = {"blue": (40, 150, 90), "blue_dark": (20, 90, 54), "blue_light": (110, 210, 150), "belly": (226, 236, 200),
         "wing": (120, 90, 220), "wing_dark": (70, 40, 160), "orange": (160, 120, 255), "red": (120, 60, 220),
         "yellow": (200, 180, 255), "flame": (160, 120, 255, 220), "flame_core": (230, 210, 255, 235)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = scales(P, "blue", "blue_dark", size=1.5, light="blue_light", belly_key="belly",
              belly=lambda x, y, z, face: face == "down")
SKULL = skin(P, "skull", dark="skull_dark", var=0.04)
MANE = [strands(P, k, "red", tip="yellow") for k in ("red", "orange", "yellow")]


def headf(x, y, z, face, variant, box=None, **k):
    """The skull head: white, with a black mask band over the eyes and black stripes down the snout."""
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 4.6, y - 41.6, 1.25, "eye", ring="mouth")
        if c is not None:
            return c, None
        if abs(y - 41.6) < 1.9 and -8.5 < z < -1.5:
            return tone(p["mask"], face), None                       # the black mask band
    if face == "up" and abs(abs(x) - 1.2) < 0.35 and z < -3:
        return tone(p["mask"], face), None                           # stripes down the snout
    return SKULL(x, y, z, face, variant, box=box, **k)


def mouthf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("up", "down"):
        return tone(p["tongue"] if abs(x) < 0.8 else p["mouth"], face), None
    return SKULL(x, y, z, face, variant, box=box, **k)


def wing_inside(x, y, z, face, box):
    """A ragged wing on a yz plane: a deeply notched trailing edge between the finger bones, torn holes."""
    u, v, W, H = local(x, y, z, face, box)
    tu, tv = u / W, v / H                                            # 0..1 back, 0..1 up
    if tv > 1 - tu * 0.55:
        return False
    notch = 0.12 + 0.3 * tu * abs(math.sin(tu * 11.0)) ** 0.6 + 0.08 * abs(math.sin(tu * 37))
    if tv < notch:
        return False
    for i in range(7):                                               # torn holes
        cu, cv, r = 0.3 + 0.1 * i, 0.3 + 0.45 * ((i * 0.37) % 1), 0.025 + 0.02 * (i % 3)
        if math.hypot(tu - cu, (tv - cv) * 0.7) < r:
            return False
    return True


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    tu, tv = u / W, v / H
    col = mix(p["wing"], p["wing_dark"], tv * 0.6)
    for vein in (0.25, 0.48, 0.7, 0.9):                              # finger veins fanning back
        if abs(tv - (1 - tu * (1.2 - vein))) < 0.025:
            col = p["wing_dark"]
    edge = 1 - tu * 0.55 - tv
    if tu > 0.7 or edge < 0.08:
        col = mix(col, p["wing_edge"], min(1, (tu - 0.7) / 0.3 if tu > 0.7 else 1 - edge / 0.08))
    return tone(col, face), None


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if abs(u / max(W, 1e-6) - 0.5) < 0.2 else p["flame"]
    return c, c[:3]


def spine():
    """The serpent's spine: rearing neck, a body looping down and round, the tail curling back up."""
    pts = []
    for i in range(15):
        t = i / 14
        y = 36 - 30 * t + 6 * math.sin(t * math.pi * 1.6)
        z = -2 + 10 * math.sin(t * math.pi * 1.2)
        x = 5 * math.sin(t * math.pi * 2.2)
        pts.append(((x, y, z), 6.2 - 4.4 * t))
    return pts


def build():
    m = Model("airdramon")
    top = m.bone("airdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    pts = spine()
    cuts = [0, 4, 8, 11]
    bones = {}
    parent = bd
    for n, c in zip(("neck", "coil_1", "coil_2", "tail"), cuts):
        parent = m.bone(n, parent, pts[c][0])
        bones[c] = parent
    cur = bones[0]
    for i, ((a, ta), (b, tb)) in enumerate(zip(pts, pts[1:])):
        cur = bones.get(i, cur)
        rod(m, cur, a, b, round((ta + tb) / 2), BODY, extend=1.0)
        if i % 2 == 0 and i < 12:                                  # back fin spines
            spike(m, cur, (a[0], a[1] + ta / 2, a[2]), (0, 1, 0.5), 1.2, 1.6 + ta * 0.3, MANE[1], tip=0.3)
    # tail flame
    tl = bones[11]
    tp = pts[-1][0]
    for ang in (0, 60, 120):
        m.box(tl, tp[0] - 2.5, tp[1] - 1.0, tp[2], tp[0] + 2.5, tp[1] + 7.0, tp[2],
              cutout(flame_inside(3, 0.15, 4), flamef), rotation=(0, ang, -60), pivot=tp)
    # head on the neck: skull, snout, open jaw, teeth, horn-quills, feather mane
    hd = m.bone("head", bones[0], (0, 40, -3))
    m.round_box(hd, 0, -3.5, 3.0, 3.4, 38.5, 44.5, headf, cut=1)
    m.box(hd, -2.4, 40.0, -11.0, 2.4, 43.4, -6.0, headf)                         # snout
    m.box(hd, -2.0, 43.2, -10.4, 2.0, 44.2, -6.2, headf)
    jw = m.bone("jaw", hd, (0, 39.5, -3.5))
    m.box(jw, -2.2, 37.4, -10.4, 2.2, 39.5, -4.0, mouthf, rotation=(26, 0, 0), pivot=(0, 39.5, -4.0))
    for sx in (-1, 1):
        for zz in (-10.4, -9.0, -7.6, -6.2):
            spike(m, hd, (sx * 2.1, 40.0, zz), (0, -1, 0), 0.8, 1.4, solid(P, "teeth"), tip=0.25)
        spike(m, hd, (sx * 2.2, 44.0, -4.5), (sx * 0.5, 1, 0.6), 1.0, 5.0, solid(P, "skull"), tip=0.25)   # quills
        spike(m, hd, (sx * 1.6, 44.4, -2.5), (sx * 0.3, 1, 0.9), 0.9, 4.0, solid(P, "skull"), tip=0.25)
    mane = m.bone("mane", hd, (0, 41, -1))
    for i in range(22):                                                         # the feather mane round its face
        ang = math.radians(i * (360 / 22))
        d = (math.cos(ang) * 0.8, math.sin(ang) * 0.8, 1.0)                     # swept back, like flames
        base = (2.8 * math.cos(ang), 41.0 + 3.0 * math.sin(ang), -1.5)
        spike(m, mane, base, d, 1.4, 5.0 + 2.5 * (i % 3), MANE[i % 3], tip=0.3)
    for i in range(6):                                                          # long flame-feathers down its neck
        rod(m, mane, (0, 39.0 - i * 1.4, 1.0), (math.sin(i) * 3, 34.0 - i * 2.0, 8.0 + i), 1, MANE[i % 3], extend=0.2, t2=2)
    # wings
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bones[0], (sx * 2.0, 33.0, 1.0))
        m.box(w, sx * 2.0, 26.0, 1.0, sx * 2.0, 48.0, 25.0, cutout(wing_inside, wingf),
              rotation=(0, sx * 55, sx * 12), pivot=(sx * 2.0, 33.0, 1.0))
        rod(m, w, (sx * 2.0, 33.0, 1.0), (sx * 2.0 + sx * 6, 46.0, 6.0), 1, solid(P, "wing_dark"), extend=0.2)
    return m
