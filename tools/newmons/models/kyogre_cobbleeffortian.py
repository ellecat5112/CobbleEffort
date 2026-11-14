"""The CobbleEffort Kyogre (Ground), the user's idea: Kyogre as a giant mud fish. It wallows in swamps and drags itself
over the mud on its great pectoral fins like a mudskipper. Its broad whale body is mud brown with a khaki belly, its
back caked in dried mud that cracks into plates, and Kyogre's markings run along its flanks and fins as glowing ochre
veins, like magma seen through cracked earth. A wide flat catfish head with a long mouth, mudskipper eyes bulging on
top, two long barbels drooping from the corners of its mouth and two short ones from its chin; four tail flukes.

Shiny: grey clay with teal veins.

Front is -z, y is up. 24 units tall, 66 long; baseScale 1.1 (4.5 m long).
"""
from __future__ import annotations

import math

from _afake import solid_of
from _boxmodel import Model, rod
from _route import pal, tone

SCALE = 1.1
HITBOX = [3.6, 1.5]
KIND = "quadruped"
K = 2
HEIGHT = 24
LOOK = ("a giant mud fish: a broad mud-brown whale body with a khaki belly, a back caked in cracked dried mud, glowing "
        "ochre veins along its flanks and fins, a flat catfish head with drooping barbels, mudskipper eyes bulging on top, "
        "great pectoral fins it walks on and four tail flukes")
LOCATORS = {"seat_1": ("body", (0, 23, -4)), "seat_2": ("body", (0, 22, 6))}   # Mega Showdown's riding data

BASE = {"mud": (112, 82, 56), "mud_dark": (82, 60, 42), "dried": (170, 142, 104), "crack": (76, 56, 40),
        "belly": (186, 162, 120), "vein": (232, 156, 50), "glow": (255, 178, 60), "eye": (236, 214, 120),
        "pupil": (28, 22, 18), "white": (250, 246, 236), "mouth": (58, 36, 30), "tip": (214, 196, 160)}
SHINY = {"mud": (126, 128, 132), "mud_dark": (92, 94, 100), "dried": (176, 178, 180), "crack": (78, 80, 86),
         "belly": (206, 204, 196), "vein": (60, 200, 196), "glow": (90, 240, 230), "tip": (222, 222, 216)}


def P(variant):
    return pal(BASE, SHINY, variant)


solid = solid_of(P)


def cracked(x, y, z):
    """Dried mud: a crack network from two offset grids, bent a little so it doesn't look ruled."""
    u = x + 0.6 * math.sin(z * 0.7)
    v = z + 0.6 * math.sin(x * 0.9)
    return (u % 4.6) < 0.45 or (v % 5.3) < 0.45


def vein(x, y, z, face):
    """Kyogre's markings as glowing veins: a wave along each flank, and a ring round the head."""
    if face in ("east", "west") and -15 < z < 18 and abs(y - (11.5 + 2.6 * math.sin((z + 15) / 6.5))) < 0.45:
        return True
    if face in ("east", "west", "up") and abs(z + 13.5) < 0.45 and y > 9:
        return True
    return False


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if vein(x, y, z, face):
        return p["vein"], p["glow"]
    if y < 8 or face == "down":
        return tone(p["belly"], face), None
    if y > 17 or face == "up":
        return tone(p["crack"] if cracked(x, y, z) else p["dried"], face), None
    if y < 10 and face in ("east", "west", "north", "south") and (x * 3 + z) % 5 < 0.9:
        return tone(p["mud_dark"], face), None                         # mud running down its sides
    return tone(p["mud"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        mouth_y = 8.2 + 0.035 * x * x                                  # a wide mouth, corners turned up
        if abs(y - mouth_y) < 0.5 and abs(x) < 9:
            return p["mouth"], None
        if abs(y - mouth_y) < 1.1 and abs(x) < 9.4:
            return tone(p["belly"], face), None                        # pale lips
    if face in ("east", "west", "up") and abs(z + 13.5) < 0.45 and y > 9:
        return p["vein"], p["glow"]
    if y < 8:
        return tone(p["belly"], face), None
    if face == "up":
        return tone(p["crack"] if cracked(x, y, z) else p["dried"], face), None
    return tone(p["mud"], face), None


def eyef(x, y, z, face, variant, **k):
    """A bulging mudskipper eye, looking forward and out."""
    p = P(variant)
    cx = 6.0 if x > 0 else -6.0
    if face in ("north", "up", "east", "west"):
        if face == "north":
            d = math.hypot(x - cx, y - 19.5)
        elif face == "up":
            d = math.hypot(x - cx, z + 13.0) * 1.3
        else:
            d = math.hypot(y - 19.5, z + 13.5)
        if d < 0.7:
            return p["white"], None
        if d < 1.6:
            return p["pupil"], None
        if d < 2.5:
            return p["eye"], None
    return tone(p["mud"], face), None


def finf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)       # 0 at the body, 1 at the tip
    lx = x - (box.lo[0] + box.size[0] / 2)
    if face in ("up", "down") and abs(lx) < 0.45 and 0.15 < t < 0.8:
        return p["vein"], p["glow"]                                   # a vein down the middle of the fin
    if t > 0.78:
        return tone(p["tip"], face), None                             # mud-dipped tips
    return tone(p["mud_dark"] if face == "down" else p["mud"], face), None


def barbelf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)
    return tone(p["mud_dark"] if t < 0.7 else p["dried"], face), None


def build() -> Model:
    m = Model("kyogre_cobbleeffortian")
    top = m.bone("kyogre", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    # the broad whale body, a flattened round loaf
    m.round_box(bd, 0, -2, 9, 12, 3, 6, bodyf, cut=4)
    m.round_box(bd, 0, -2, 12, 16, 5.5, 17.5, bodyf, cut=5)
    m.round_box(bd, 0, 11, 9, 9, 7, 16.5, bodyf, cut=3)                  # tapering to the tail
    m.round_box(bd, 0, -2, 9.5, 13, 17, 21, bodyf, cut=4)
    m.round_box(bd, 0, 0, 5, 8, 20.5, 23, bodyf, cut=3)
    hd = m.bone("head", bd, (0, 12, -14))
    m.round_box(hd, 0, -18.5, 10, 5, 4.5, 15, headf, cut=2)             # the wide flat catfish head
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 3.6, sx * 8.4))
        m.box(hd, x0, 16.5, -15.5, x1, 22, -11, eyef)                    # bulging mudskipper eyes
        rod(m, hd, (sx * 9.2, 8.6, -22.5), (sx * 15, 8, -25), 1, barbelf, extend=0.3)
        rod(m, hd, (sx * 15, 8, -25), (sx * 19, 4.5, -23), 1, barbelf, extend=0.3)        # long drooping barbels

    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                  # great pectoral fins it walks on
        a = m.bone(nm, bd, (sx * 11, 9, -6))
        rod(m, a, (sx * 10.5, 9, -6), (sx * 24, 1, 1), 9, finf, extend=1, t2=2)

    tl = m.bone("tail", bd, (0, 12, 18))
    rod(m, tl, (0, 12, 18), (0, 12.5, 28), 12, bodyf, t2=9)
    rod(m, tl, (0, 12.5, 27), (0, 13, 36), 8, bodyf, t2=7)
    for sy, sx in ((1, 1), (1, -1), (-1, 1), (-1, -1)):                 # four flukes in an X, like Kyogre's
        rod(m, tl, (sx * 1.5, 13 + sy * 1.5, 35), (sx * 9, 13 + sy * 7, 44), 6, finf, extend=0.5, t2=1)
    return m
