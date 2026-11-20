"""Proto-Palkia (Water/Psychic), the ancient paradox Palkia, built from boxes after the art the user shared (the art's
own name; artist not named).

A massive Palkia of rose-pink crystal traced with glowing magenta veins and flecked with stars. A great pearl glows
on each shoulder, its arms are a darker smoky mauve, and its feet and claws are white. Behind it spread two jagged
fans of translucent magenta crystal, glowing at their edges, with more shards of crystal drifting round them.

Shiny: a violet body with cyan veins.

Front is -z, y is up. 59 units tall (to the wing tips); about 5.6 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _palkia import palkia
from _pgen1 import CLEAR, inside, stars
from _regi import lit
from _route import mix, pal, tone

HEIGHT = 59
SCALE = round(5.6 * 16 / HEIGHT, 3)
HITBOX = [3.0, HEIGHT / 16]
KIND = "biped"
K = 3
LOOK = ("a massive Palkia of rose-pink crystal veined in glowing magenta and flecked with stars, glowing shoulder pearls "
        "and two jagged fans of translucent magenta crystal spread behind it")

BASE = {"pink": (230, 150, 214), "pink_dark": (176, 90, 166), "pink_light": (250, 200, 240), "vein": (255, 110, 230),
        "star": (255, 255, 255), "mauve": (124, 100, 130), "mauve_dark": (84, 66, 92), "white": (246, 238, 246),
        "pearl": (255, 196, 248), "pearl_core": (255, 240, 255), "wing": (232, 80, 226, 170), "wing_edge": (255, 150, 245),
        "eye": (200, 40, 80)}
SHINY = {"pink": (170, 140, 236), "pink_dark": (116, 90, 190), "pink_light": (210, 196, 250), "vein": (110, 236, 255),
         "pearl": (180, 240, 255), "wing": (120, 140, 240, 170), "wing_edge": (170, 230, 255)}
WING = [(4.0, 34.0), (10.0, 46.0), (13.0, 41.0), (19.0, 55.0), (20.0, 47.0), (27.0, 50.0), (23.0, 40.0),
        (29.0, 37.0), (21.0, 33.0), (25.0, 26.0), (16.0, 30.0), (13.0, 24.0), (10.0, 30.0)]


def P(v):
    return pal(BASE, SHINY, v)


def vein(x, y, z):
    a = math.sin(y * 0.6 + math.sin(x * 0.5) * 1.6)
    b = math.sin(x * 0.35 + z * 0.4 + math.sin(y * 0.3) * 1.2)
    return abs(a + 0.7 * b) < 0.12


def crystalf(x, y, z, face, variant, **k):
    p = P(variant)
    if stars(x, y, z, face, cell=1.6, r=0.25, prob=0.3):
        return p["star"], p["star"]
    if vein(x, y, z):
        return p["vein"], p["vein"]
    if face == "up":
        return p["pink_light"], None
    return lit(p["pink"], face, y, 30, 18), None


def mauvef(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["mauve"] if face != "down" else p["mauve_dark"], face), None


def whitef(x, y, z, face, variant, **k):
    return tone(P(variant)["white"], face), None


def pearlf(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["pearl_core"] if face == "north" or (face in ("east", "west") and abs(y - 40.6) < 1.0) else p["pearl"]
    return c, c


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 10.4, y - 52.6) < 0.8:
        return p["eye"], p["eye"]
    return crystalf(x, y, z, face, variant)


def wingf(side):
    """A jagged fan of translucent magenta crystal (an xy plane), its edges and spines glowing."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u = side * x
        if not inside(WING, u, y):
            return CLEAR
        inner = [(4.0 + (q[0] - 4.0) * 0.8, 36.0 + (q[1] - 36.0) * 0.8) for q in WING]
        if not inside(inner, u, y):
            return p["wing_edge"], p["wing_edge"]
        for tip in ((19.0, 55.0), (27.0, 50.0), (29.0, 37.0), (25.0, 26.0)):
            tx, ty = tip[0] - 6.0, tip[1] - 36.0
            L = math.hypot(tx, ty)
            along = ((u - 6.0) * tx + (y - 36.0) * ty) / L
            across = abs(-(u - 6.0) * ty + (y - 36.0) * tx) / L
            if 0 < along < L and across < 0.45:
                return p["wing_edge"], p["wing_edge"]
        return p["wing"], None
    return s


def shardf(x, y, z, face, variant, box=None, **k):
    """A drifting diamond of crystal (an xy plane)."""
    p = P(variant)
    cx, cy = box.lo[0] + box.size[0] / 2, box.lo[1] + box.size[1] / 2
    u, v = abs(x - cx) / (box.size[0] / 2), abs(y - cy) / (box.size[1] / 2)
    if u + v > 1.0:
        return CLEAR
    return (p["wing_edge"], p["wing_edge"]) if u + v > 0.6 else (p["wing"], None)


def build() -> Model:
    m = Model("protopalkia")
    mats = {"skin": crystalf, "belly": crystalf, "neck": crystalf, "head": headf, "arm": mauvef, "hand": mauvef,
            "claw": whitef, "thigh": crystalf, "shin": crystalf, "foot": whitef, "talon": whitef, "tail": crystalf,
            "tail_tip": crystalf, "pearl": pearlf, "mount": crystalf, "crest": whitef}
    a = palkia(m, mats, "protopalkia", pearl_r=3.0)
    bd = a["body"]
    for nm, side in (("wing_left", 1), ("wing_right", -1)):                      # jagged crystal fans
        wg = m.bone(nm, bd, (side * 4.0, 36.0, 5.0))
        x0, x1 = sorted((side * 3.5, side * 29.5))
        m.box(wg, x0, 23.5, 5.6, x1, 55.5, 5.6, wingf(side))
        for (u, v, s) in ((31.0, 44.0, 1.6), (27.0, 22.0, 1.3), (22.0, 57.0, 1.2)):  # drifting shards
            cx = side * u
            m.box(wg, cx - s, v - s * 1.6, 6.4, cx + s, v + s * 1.6, 6.4, shardf)
    for sx in (-1, 1):                                                           # crystal spines down its back
        for i, y in enumerate((44.0, 38.0, 32.0)):
            spike(m, bd, (sx * 2.0, y, 4.0 + i * 0.8), (sx * 0.4, 0.4, 1), 1.6, 3.4 - i * 0.4, whitef, tip=0.6)
    return m
