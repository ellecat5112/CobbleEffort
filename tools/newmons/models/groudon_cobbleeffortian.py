"""The CobbleEffort Groudon (Steel/Fire), after Hoops and Hiphop's regional Groudon art: a hunched titan in white steel
armour joined by glowing red seams, as if the magma inside shows through the cracks between its plates. A ridged steel
visor with four slats runs forward to a point over its red face, with a heavy black guard on each cheek; its chest and
throat are slate blue, its belly bronze banded with red; white gauntlets end in three black claws, and armoured legs
in black toe claws. Its bronze tail is built of thick segments bolted together and curls up over its back to a great
crescent blade.

Shiny: gunmetal plates with blue-hot seams and a gold tail.

Front is -z, y is up. 62 units tall (the tail blade); baseScale 0.9 (3.5 m).
"""
from __future__ import annotations

import math

from _afake import solid_of
from _boxmodel import Model, rod, spike
from _route import pal, tone

SCALE = 0.9
HITBOX = [3.2, 3.2]
KIND = "biped"
K = 2
HEIGHT = 62
ANIM = {"leg_amp": 14}
LOOK = ("a hunched titan in white steel armour joined by glowing red seams: a slatted steel visor over a red face, "
        "black cheek guards, a slate-blue chest, bronze belly bands, white gauntlets with black claws and a bolted "
        "bronze tail curling up to a crescent blade")
LOCATORS = {"seat_1": ("body", (0, 34, 4))}       # Mega Showdown's riding data seats the rider here

BASE = {"plate": (232, 228, 222), "plate_dark": (190, 184, 178), "seam": (186, 48, 40), "glow": (255, 104, 40),
        "bronze": (140, 108, 94), "bronze_dark": (104, 78, 68), "belly": (136, 168, 200), "claw": (50, 50, 56),
        "face": (172, 50, 42), "eye": (240, 224, 150), "pupil": (40, 34, 30), "teeth": (242, 238, 230),
        "bolt": (64, 64, 72)}
SHINY = {"plate": (78, 82, 92), "plate_dark": (58, 60, 68), "seam": (50, 100, 200), "glow": (90, 190, 255),
         "bronze": (200, 162, 82), "bronze_dark": (152, 118, 56), "belly": (222, 204, 152), "face": (52, 96, 190)}


def P(variant):
    return pal(BASE, SHINY, variant)


solid = solid_of(P)


def seam(p):
    return p["seam"], p["glow"]


def plated(seams=(), vseams=(), w=0.32):
    """White steel plate; red glowing seams at heights `seams` and at x positions `vseams` (front and top faces)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face not in ("up", "down") and any(abs(y - h) < w for h in seams):
            return seam(p)
        if face in ("north", "up") and any(abs(x - v) < w for v in vseams):
            return seam(p)
        return tone(p["plate"], face), None
    return s


def torso(x, y, z, face, variant, **k):
    """Slate-blue chest and throat in front, bronze belly banded with red below and round the sides."""
    p = P(variant)
    if face == "north" and abs(x) < 5.6 - max(0, 22 - y) * 0.25 and y > 16:
        return tone(p["belly"], face), None
    if y < 22 and face != "up" and int((y + 0.5) // 1.6) % 2 == 0:
        return tone(p["seam"] if face == "north" else p["bronze_dark"], face), None     # red bands on the belly
    return tone(p["bronze"], face), None


def tailf(x, y, z, face, variant, box=None, **k):
    """A bolted bronze tail segment: a red seam where it meets the next, a dark bolt on each side."""
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)
    if t < 0.12:
        return seam(p)
    if face in ("east", "west"):
        cy = box.lo[1] + box.size[1] / 2
        if math.hypot(y - cy, (t - 0.55) * box.size[2]) < 1.3:
            return tone(p["bolt"], face), None
    return tone(p["bronze"] if t > 0.2 else p["bronze_dark"], face), None


def bladef(x, y, z, face, variant, **k):
    """The crescent tail blade (a cut-out in the yz plane), bronze with a glowing red V."""
    p = P(variant)
    d_out = math.hypot(y - 40, z - 12)
    d_in = math.hypot(y - 36.5, z - 13.5)
    if not (d_out < 21 and d_in > 17.5 and y > 41 and z > 3):
        return (0, 0, 0, 0), None
    if abs(d_in - 18.3) < 0.45:                                        # a seam along its inner edge
        return seam(p)
    if face in ("east", "west") and 22 < z < 32 and abs(abs(z - 27) * 1.4 - (y - 44)) < 0.5 and y < 52:
        return seam(p)                                                 # the V near its root
    return tone(p["bronze"] if d_out < 20 else p["bronze_dark"], face), None


def facef(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(y - 32.4, z + 18.4) < 1.0:
        return (p["pupil"] if math.hypot(y - 32.4, z + 18.2) < 0.45 else p["eye"]), None
    if face == "north" and 28.2 < y < 29.6 and (abs(x) + (y - 28.2) * 2) % 1.6 < 1.1:
        return p["teeth"], None                                       # a row of teeth
    if face in ("east", "west") and 28.4 < y < 29.4 and z < -12:
        return p["teeth"], None
    if y < 28.2:
        return tone(p["belly"], face), None                           # the jaw underneath
    return tone(p["face"], face), None


def build() -> Model:
    m = Model("groudon_cobbleeffortian")
    top = m.bone("groudon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 2))
    # the torso: bronze belly, blue chest, white back armour and shoulder plates
    m.round_box(bd, 0, 3, 8, 8, 13, 25, torso, cut=2)
    m.round_box(bd, 0, 0, 7, 7, 24, 31, torso, cut=2)
    m.box(bd, -8.5, 25, -3, 8.5, 33, 11, plated(vseams=(0,)))
    m.box(bd, -7, 32.5, 0, 7, 35, 9, plated(vseams=(-3.5, 3.5)))
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 7.5, sx * 12))
        m.box(bd, x0, 26, -8, x1, 33, 1, plated(seams=(26.4,)))                # shoulder plates
        x0, x1 = sorted((sx * 5.5, sx * 11))
        m.box(bd, x0, 13, -3, x1, 20, 9, plated(seams=(16.5,)))                # hip plates

    hd = m.bone("head", bd, (0, 31, -7))
    m.box(hd, -4, 27, -12, 4, 33, -4, torso)                                   # the neck
    m.box(hd, -4.5, 27, -21, 4.5, 34, -10, facef)                              # red face over the jaw
    m.box(hd, -5, 33.5, -20, 5, 37.5, -8, plated(seams=(35.5,)))               # the visor's base
    for x in (-3.8, -1.3, 1.3, 3.8):                                           # four slats running forward to a point
        m.box(hd, x - 0.8, 35.5, -22, x + 0.8, 38.5, -7, plated(), rotation=(10, 0, 0), pivot=(x, 37, -8))
    spike(m, hd, (0, 33, -20), (0, -0.35, -1), 3, 4, plated(), tip=1.5)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 4.5, sx * 8))
        m.box(hd, x0, 31.5, -16.5, x1, 37.5, -10, solid("claw"))               # heavy black cheek guards
        rod(m, hd, (sx * 6, 37, -11), (sx * 7, 40, -4), 2, solid("claw"))     # and the bar sweeping back

    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 9, 27, -5))
        rod(m, a, (sx * 9.5, 27, -4), (sx * 12, 22, -9), 4, solid("bronze"))
        x0, x1 = sorted((sx * 9.5, sx * 14.5))
        m.box(a, x0, 18, -15, x1, 24, -7, plated(seams=(21,), vseams=(sx * 11, sx * 13)))   # gauntlet
        for cx in (10.5, 12, 13.5):
            spike(m, a, (sx * cx, 19.5, -14.5), (0, -0.8, -0.6), 1.4, 6, solid("claw"), tip=0.8)

    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 7.5, 15, 3))
        x0, x1 = sorted((sx * 4, sx * 11))
        m.box(lg, x0, 7, -2, x1, 16, 8, plated())                              # armoured thighs
        x0, x1 = sorted((sx * 5, sx * 10))
        m.box(lg, x0, 2, -1, x1, 8, 6, plated(seams=(3.5,)))                   # shins
        m.box(lg, x0, 0, -3, x1, 2, 7, solid("plate_dark"))                    # feet
        for cx in (5.8, 7.5, 9.2):
            spike(m, lg, (sx * cx, 1, -2.5), (0, -0.25, -1), 1.4, 4, solid("claw"), tip=0.8)

    # the bolted bronze tail, curling up over its back to the blade
    pts = [(0, 20, 9), (0, 21.5, 16), (0, 24, 22), (0, 29, 27.5), (0, 35, 30.5), (0, 41, 31.5), (0, 46, 30.5)]
    th = (12, 11, 10, 9, 8, 7)
    t1 = m.bone("tail", bd, pts[0])
    t2 = m.bone("tail_2", t1, pts[3])
    t3 = m.bone("tail_3", t2, pts[5])
    for i, (a, b, t) in enumerate(zip(pts, pts[1:], th)):
        rod(m, t1 if i < 3 else t2 if i < 5 else t3, a, b, t, tailf, extend=1.5)
    m.box(t3, -1.5, 40, 3, 1.5, 62, 34, bladef)
    return m
