"""Blimpmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a living airship. A long brown riveted hull whose sides are cream gores between curved ribs, a steel
ram spike on the nose, round porthole eyes, twin gun barrels along its back, a box-kite tail of brown fins, a row of
steel spikes along its keel, two propellers and two little gloved arms hanging under its bow. 15 blocks long.

Front is -z, y is up. 24 units tall, 62 long; Adult stage (floats).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import eye, local, metal, riveted, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(15 * 24 / 62, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a living brown airship: cream hull gores between riveted ribs, a steel ram spike, porthole eyes, twin guns "
        "on its back, a finned tail, keel spikes, propellers and two little gloved arms")
BASE = {"brown": (170, 96, 50), "brown_dark": (96, 50, 24), "brown_light": (220, 150, 96), "cream": (246, 230, 190),
        "cream_dark": (206, 180, 130), "steel": (200, 204, 216), "steel_dark": (96, 100, 112), "eye": (250, 200, 60),
        "pupil": (30, 20, 10), "white": (255, 255, 255), "glove": (230, 230, 236)}
SHINY = {"brown": (70, 110, 70), "brown_dark": (30, 56, 30), "brown_light": (120, 170, 120), "cream": (220, 236, 246),
         "cream_dark": (160, 186, 206)}


def P(v):
    return pal(BASE, SHINY, v)


BROWN = riveted(P, "brown", "brown_dark", light="brown_light")
STEEL = metal(P, "steel", dark="steel_dark")
CY, L = 13.0, 30.0


def hullf(x, y, z, face, variant, box=None, **k):
    """Cream gores between brown ribs on the sides, riveted brown along the top and keel."""
    p = P(variant)
    rel = (y - CY) / 8.0
    if face in ("east", "west") and abs(rel) < 0.62:
        if z % 5.0 < 0.8:
            return tone(p["brown"], face), None
        g = (z % 5.0) / 5.0
        return tone(p["cream"] if 0.2 < g < 0.8 else p["cream_dark"], face), None
    if face == "north" and z < -L + 4:
        for sx in (-1, 1):
            c = eye(p, x - sx * 2.6, y - CY - 1.0, 1.1, "eye")
            if c is not None:
                return c, None
    return BROWN(x, y, z, face, variant, box=box, **k)


def propf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["steel"] if abs(x) + abs(y) > 0 else p["steel_dark"], face), None


def build():
    m = Model("blimpmon")
    top = m.bone("blimpmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    n = 14
    for i in range(n):                                                        # the hull: slices along z
        z0 = -L + i * 2 * L / n
        t = (z0 + L / n) / L
        r = 8.0 * math.sqrt(max(0.06, 1 - t ** 4)) if t < 0 else 8.0 * math.sqrt(max(0.06, 1 - t * t))
        slab_z(m, bd, 0, CY, z0 - 0.2, z0 + 2 * L / n + 0.2, r * 0.92, r, hullf)
    spike(m, bd, (0, CY, -L + 0.6), (0, 0, -1), 3.0, 8.0, STEEL, tip=1.0)    # ram spike
    m.round_box(bd, 0, -L + 1.6, 2.4, 1.2, CY - 2.4, CY + 2.4, STEEL, cut=1)
    for sx in (-1, 1):                                                        # twin guns on its back
        rod(m, bd, (sx * 1.6, CY + 8.4, 2.0), (sx * 1.6, CY + 8.6, -16.0), 1, STEEL, extend=0)
        m.box(bd, sx * 1.6 - 1.2, CY + 7.0, 0.0, sx * 1.6 + 1.2, CY + 9.4, 6.0, BROWN)
    m.box(bd, -2.4, CY + 6.6, 6.0, 2.4, CY + 9.0, 12.0, BROWN)               # turret housing
    for i in range(5):                                                        # keel spikes
        spike(m, bd, (0, CY - 7.4, -6.0 + i * 4.0), (0, -1, 0.5), 1.4, 3.6, STEEL, tip=0.5)
    # the box-kite tail: vertical and horizontal brown fins in a frame
    tl = m.bone("tail", bd, (0, CY, L - 2))
    for yy in (CY - 7.0, CY + 7.0):
        m.box(tl, -0.6, min(yy, CY), L - 4.0, 0.6, max(yy, CY), L + 6.0, BROWN)
    for xx in (-7.0, 7.0):
        m.box(tl, min(xx, 0), CY - 0.6, L - 4.0, max(xx, 0), CY + 0.6, L + 6.0, BROWN)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 6.0, sx * 7.2))
        m.box(tl, x0, CY - 7.0, L + 2.0, x1, CY + 7.0, L + 6.0, BROWN)
    m.box(tl, -7.2, CY + 6.0, L + 2.0, 7.2, CY + 7.2, L + 6.0, BROWN)
    m.box(tl, -7.2, CY - 7.2, L + 2.0, 7.2, CY - 6.0, L + 6.0, BROWN)
    # two propellers under the stern (spin bones turn round z)
    for sx, nm in ((1, "spin_left"), (-1, "spin_right")):
        hub = (sx * 5.0, CY - 6.4, 16.0)
        rod(m, bd, (sx * 3.0, CY - 5.0, 14.0), hub, 1, STEEL, extend=0.3)
        pb = m.bone(nm, bd, hub)
        m.box(pb, hub[0] - 0.8, hub[1] - 0.8, hub[2], hub[0] + 0.8, hub[1] + 0.8, hub[2] + 1.6, STEEL)
        for ang in (0, 120, 240):
            m.box(pb, hub[0] - 0.7, hub[1], hub[2] + 0.6, hub[0] + 0.7, hub[1] + 4.0, hub[2] + 0.8, propf,
                  rotation=(0, 0, ang), pivot=(hub[0], hub[1], hub[2] + 0.7))
    # two little arms under the bow, gloved hands
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        sh = (sx * 3.0, CY - 6.0, -18.0)
        ab = m.bone(nm, bd, sh)
        el = (sx * 4.0, CY - 10.0, -20.0)
        rod(m, ab, sh, el, 2, BROWN, extend=0.4)
        rod(m, ab, el, (sx * 3.6, CY - 12.0, -23.0), 2, STEEL, extend=0.3)
        m.box(ab, sx * 3.6 - 1.2, CY - 13.6, -25.4, sx * 3.6 + 1.2, CY - 11.2, -22.6, solid(P, "glove"))
    return m
