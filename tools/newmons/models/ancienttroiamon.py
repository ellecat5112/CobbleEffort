"""Ancient Troiamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the ancient warrior of wood, a war-machine horse. A body of planked golden wood bound
with riveted steel bands, a horse head whose mouth is a great steel cannon, a second cannon in its chest and two
long gun barrels on its back, bronze gears turning at its shoulders and hips, and steel-shod hooves. 35 blocks tall.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import local, metal, mix, plane, riveted, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a war-machine horse of planked golden wood bound with riveted steel: a cannon for a mouth, a chest cannon, "
        "two gun barrels on its back, bronze gears at its joints and steel-shod hooves")
BASE = {"wood": (210, 168, 90), "wood_dark": (140, 100, 44), "wood_light": (240, 210, 140), "steel": (170, 174, 186),
        "steel_dark": (80, 84, 96), "bronze": (170, 110, 60), "bronze_dark": (100, 60, 30), "eye": (255, 120, 40),
        "bore": (20, 20, 24)}
SHINY = {"wood": (120, 80, 60), "wood_dark": (70, 40, 28), "wood_light": (170, 120, 90), "bronze": (200, 200, 210),
         "bronze_dark": (120, 120, 130)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = riveted(P, "steel", "steel_dark", spacing=2.0)
GUN = metal(P, "steel", dark="steel_dark")
BRONZE = metal(P, "bronze", dark="bronze_dark")


def woodf(x, y, z, face, variant, box=None, **k):
    """Planks with grain lines and dark seams between boards."""
    p = P(variant)
    a, b = plane(x, y, z, face)
    board = (b if face not in ("up", "down") else a) % 2.4
    if board < 0.22:
        return tone(p["wood_dark"], face), None
    grain = math.sin(a * 2.3 + math.sin(b * 0.7) * 2) * 0.5 + 0.5
    return tone(mix(p["wood"], p["wood_light"] if grain > 0.8 else p["wood_dark"], 0.15 + 0.1 * grain), face), None


def boref(x, y, z, face, variant, box=None, **k):
    """A cannon: steel with a dark bore on its muzzle face."""
    p = P(variant)
    if face == "north":
        u, v, W, H = local(x, y, z, face, box)
        if math.hypot(u - W / 2, v - H / 2) < min(W, H) * 0.32:
            return p["bore"], None
    return metal(P, "steel", dark="steel_dark")(x, y, z, face, variant, box=box, **k)


def gear(m, bone, c, r, axis_x=True):
    """A bronze gear seen from the side: a disc of crossed slabs with teeth."""
    for ang in (0, 45):
        m.box(bone, c[0] - 0.6, c[1] - r, c[2] - r * 0.42, c[0] + 0.6, c[1] + r, c[2] + r * 0.42, BRONZE,
              rotation=(ang, 0, 0), pivot=c)
    for i in range(8):
        a = math.radians(i * 45 + 22.5)
        p = (c[0], c[1] + (r + 0.6) * math.sin(a), c[2] + (r + 0.6) * math.cos(a))
        m.box(bone, p[0] - 0.6, p[1] - 0.6, p[2] - 0.6, p[0] + 0.6, p[1] + 0.6, p[2] + 0.6, BRONZE,
              rotation=(i * 45 + 22.5, 0, 0), pivot=p)


def build():
    m = Model("ancienttroiamon")
    top = m.bone("ancienttroiamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    m.box(bd, -7.0, 20.0, -12.0, 7.0, 34.0, 12.0, woodf)                                 # the plank hull
    for z in (-11.0, -3.0, 5.0, 11.0):                                                   # steel bands
        m.box(bd, -7.4, 19.6, z - 0.8, 7.4, 34.4, z + 0.8, STEEL)
    m.box(bd, -7.4, 33.6, -12.4, 7.4, 34.6, 12.4, STEEL)
    m.round_box(bd, 0, -13.2, 3.4, 1.6, 23.0, 30.0, boref, cut=1)                       # chest cannon
    for sx in (-1, 1):                                                                   # back guns
        m.box(bd, sx * 3.0 - 1.6, 34.0, -2.0, sx * 3.0 + 1.6, 37.0, 4.0, STEEL)
        rod(m, bd, (sx * 3.0, 36.0, 0.0), (sx * 3.0, 42.0, -14.0), 2, GUN, extend=0.2)
        gear(m, bd, (sx * 7.4, 27.0, -8.0), 3.4)
        gear(m, bd, (sx * 7.4, 25.0, 8.0), 3.0)
    nk = m.bone("neck", bd, (0, 32, -10))
    m.box(nk, -4.0, 32.0, -14.0, 4.0, 46.0, -6.0, woodf, rotation=(-20, 0, 0), pivot=(0, 32, -10))
    hd = m.bone("head", nk, (0, 46, -12))
    m.box(hd, -4.4, 44.0, -20.0, 4.4, 52.0, -10.0, woodf)
    m.round_box(hd, 0, -22.5, 3.4, 2.6, 44.6, 51.4, boref, cut=1)                       # the mouth cannon
    m.box(hd, -4.8, 46.0, -20.4, 4.8, 47.0, -9.6, STEEL)
    for sx in (-1, 1):
        m.box(hd, sx * 4.4 - (0.4 if sx > 0 else -0.4) - 0.4, 49.0, -17.0, sx * 4.4 + 0.4, 50.0, -15.6,
              solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.6, 52.0, -11.0), (sx * 0.2, 1, 0.3), 2.0, 4.0, woodf)                 # ears
    m.box(hd, -1.0, 52.0, -18.0, 1.0, 56.0, -9.0, STEEL)                                 # steel crest
    for front, zz in ((True, -8.0), (False, 8.0)):
        for sx in (1, -1):
            nm = f"leg_{'front' if front else 'back'}_{'left' if sx > 0 else 'right'}"
            lg = m.bone(nm, top, (sx * 5.0, 21.0, zz))
            m.box(lg, sx * 5.0 - 2.4, 10.0, zz - 2.6, sx * 5.0 + 2.4, 22.0, zz + 2.6, woodf)
            m.box(lg, sx * 5.0 - 2.0, 3.0, zz - 2.2, sx * 5.0 + 2.0, 11.0, zz + 2.2, woodf,
                  rotation=(-8 if front else 8, 0, 0), pivot=(sx * 5.0, 11.0, zz))
            m.box(lg, sx * 5.0 - 2.8, 0.0, zz - 3.6, sx * 5.0 + 2.8, 3.4, zz + 2.6, STEEL)    # steel hoof
            m.box(lg, sx * 5.0 - 2.6, 13.0, zz - 2.8, sx * 5.0 + 2.6, 14.4, zz + 2.8, STEEL)
    tl = m.bone("tail", bd, (0, 30, 12))
    rod(m, tl, (0, 30, 12), (0, 22, 18), 2, STEEL, extend=0.3)
    return m
