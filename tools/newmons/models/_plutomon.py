"""Shared builder for Plutomon and Plutomon (Fusion) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the lord of the underworld of the Olympos XII: a gaunt knight in spiked black armour lined with gold,
a horned helm with a single red eye, hound-skull pauldrons, long bladed greaves, a chain whip, and a vast tattered
cape of dark crimson flaring up behind it like wings. Fusion: Plutomon riding atop a great beast of blue-green
scales whose front is a silver orb of a face with four black eyes and a red mark, its crimson cape spread over the
beast's back. Shiny: silver armour and a violet cape.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, cutout, local, metal, noise2, scales, solid
from _dorbickmon import mount
from _route import pal, tone

BASE = {"black": (40, 38, 46), "black_dark": (12, 12, 16), "gold": (220, 180, 70), "gold_dark": (130, 90, 20),
        "cape": (130, 20, 30), "cape_dark": (60, 8, 14), "eye": (240, 40, 40), "bone": (220, 214, 196),
        "scale": (40, 110, 160), "scale_dark": (14, 50, 90), "silver": (210, 214, 226), "silver_dark": (110, 114, 130),
        "pupil": (16, 16, 20), "steel": (180, 184, 196)}
SHINY = {"black": (200, 204, 216), "black_dark": (110, 114, 130), "cape": (100, 40, 150), "cape_dark": (50, 16, 80)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", trim="gold", trim_w=0.25)
GOLD = metal(P, "gold", dark="gold_dark")


def capef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["cape_dark"] if face == "north" else p["cape"], face), None


def torn(seed):
    def inside(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        f = (box.lo[0] + u) * 0.8
        return v / max(H, 1e-6) < 0.85 - 0.25 * noise2(f, seed) - 0.1 * abs(math.sin(f * 2.1 + seed))
    return cutout(inside, capef)


def knight(m, name, scale_bulk=0.9):
    mats = {"skin": ARM, "neck": metal(P, "black", dark="black_dark"), "knee": GOLD, "talon": metal(P, "steel"),
            "foot": ARM, "hand": ARM, "finger": metal(P, "steel")}
    a = humanoid(m, mats, bulk=scale_bulk, arm_bulk=0.85, leg_bulk=0.85, talons=True, digitigrade=True, name=name)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.0, 60.0, ARM, cut=1)                          # horned helm
    m.box(hd, -0.6, 57.0, -3.3, 0.6, 58.2, -3.1, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 59.0, 0), (sx * 0.8, 1, 0.3), 1.2, 6.0, GOLD, tip=0.8)
        spike(m, hd, (sx * 1.0, 60.0, -1.0), (sx * 0.2, 1, -0.2), 1.0, 4.0, ARM, tip=0.8)
        m.round_box(bd, sx * 8.0, 0.0, 3.2, 3.4, 46.0, 52.0, ARM, cut=1)                # hound-skull pauldrons
        m.round_box(bd, sx * 8.6, -3.4, 1.6, 1.8, 46.0, 49.0, solid(P, "bone"), cut=0)
        m.box(bd, min(sx * 8.0, sx * 9.2), 48.0, -5.3, max(sx * 8.0, sx * 9.2), 48.8, -5.1, solid(P, "eye", glow=True))
        for j in range(3):
            spike(m, bd, (sx * 9.0, 52.0, -2.0 + j * 2.0), (sx * 0.5, 1, 0), 1.0, 4.0 + j, ARM, tip=0.8)
    for sx in (-1, 1):                                                                   # bladed greaves
        lg = a["leg_left" if sx > 0 else "leg_right"]
        spike(m, lg["bone"], (lg["knee"][0], lg["knee"][1] + 2.0, lg["knee"][2] - 1.0), (0, 1, -0.3), 1.2, 6.0,
              metal(P, "steel"), tip=0.8)
    w = a["arm_right"]["wrist"]                                                          # chain whip
    pts = [w, (w[0] - 2.0, w[1] - 8.0, w[2] - 2.0), (w[0] - 1.0, w[1] - 16.0, w[2] + 2.0), (w[0] + 2.0, 6.0, w[2] + 4.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, a["arm_right"]["bone"], p0, p1, 1, metal(P, "steel"), extend=0.2)
    cb = m.bone("cape", bd, (0, 52, 4))                                                  # wing-like cape
    for side in (-1, 1):
        for i in range(5):
            t = i / 4
            ang = math.radians(25 + 55 * t)
            L = 30.0 - 6.0 * t
            x0, x1 = sorted((side * 2.0, side * (2.0 + 9.0)))
            m.box(cb, x0, 50.0 - L * 0.3, 4.0 + i * 0.3, x1, 50.0 + L * 0.7, 4.0 + i * 0.3, torn(i + (3 if side > 0 else 0)),
                  rotation=(10, side * 15, -side * (90 - math.degrees(ang))), pivot=(side * 2.0, 50.0, 4.0))
    return a


def make(name, fusion=False):
    def build():
        m = Model(name)
        if not fusion:
            knight(m, name)
            return m
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 20, 0))
        ball(m, bd, (0, 26.0, 10.0), 26.0, scales(P, "scale", "scale_dark", size=2.2), layers=10, ry=22.0)
        hd = m.bone("head", bd, (0, 22, -16))
        ball(m, hd, (0, 22.0, -18.0), 16.0, metal(P, "silver", dark="silver_dark"), layers=8)
        for ex, ey in ((-5.6, 27.0), (5.6, 27.0), (-9.0, 19.0), (9.0, 19.0)):            # four black eyes
            ball(m, hd, (ex, ey, -31.4), 2.6, solid(P, "pupil"), layers=2, squash=0.4)
        m.box(hd, -1.6, 15.0, -34.4, 1.6, 18.0, -33.6, solid(P, "eye", glow=True))
        for j in range(7):
            spike(m, bd, (-21.0 + j * 7.0, 34.0, 30.0), ((j - 3) * 0.3, 0.2, 1), 2.4, 9.0, solid(P, "scale_dark"),
                  tip=0.8)
        for side in (-1, 1):                                                              # stubby clawed legs
            for zz in (-4.0, 22.0):
                nm = f"leg_{'front' if zz < 0 else 'back'}_{'left' if side > 0 else 'right'}"
                lg = m.bone(nm, top, (side * 16.0, 12.0, zz))
                m.round_box(lg, side * 16.0, zz, 4.0, 4.0, 0.0, 14.0, scales(P, "scale", "scale_dark", size=1.6), cut=1)
                for f in range(3):
                    spike(m, lg, (side * 16.0 + (f - 1) * 2.4, 1.0, zz - 4.0), (0, -0.2, -1), 1.2, 3.0,
                          solid(P, "bone"), tip=0.8)
        i_box, i_bone = len(m.boxes), len(m.bones)
        knight(m, "rider", scale_bulk=0.85)
        mount(m, i_box, i_bone, 46.0, 8.0, bd)
        return m

    return build
