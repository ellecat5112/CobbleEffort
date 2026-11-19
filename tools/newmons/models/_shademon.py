"""Shared builder for Shademon and Shademon (Nene Ver.) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). Shademon: a living shadow: a tall flickering mass of black smoke torn into flame-like tongues, set with
silver-ringed red spiral eyes down its length. Nene Ver.: a slender shadow figure in a long flowing black gown that
pools into smoke at its feet, pale face, long silver hair tied up in two tall bunches, and a great ragged black wing of
shadow spotted with pale spiral eyes. Shiny: deep violet.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import humanoid
from _digidetail import cutout, fabric, local, noise2, skin, solid, strands
from _route import pal, tone


def make(name, nene=False):
    base = {"black": (24, 22, 28), "black_light": (60, 56, 70), "red": (220, 30, 40), "silver": (200, 204, 216),
            "face": (240, 236, 236), "hair": (220, 220, 230), "hair_dark": (150, 150, 170), "eye": (230, 230, 240)}
    shiny = {"black": (50, 20, 70), "black_light": (100, 50, 140)}

    def P(v):
        return pal(base, shiny, v)

    def smokef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if not nene and face == "north":
            for ex, ey in ((0, 30.0), (-3.0, 24.0), (3.0, 24.0), (-2.0, 18.0), (2.0, 18.0), (0, 12.0)):
                d = math.hypot(x - ex, y - ey)
                if d < 1.6:
                    if d < 0.6 or abs(d - 1.1) < 0.2:
                        return p["red"], p["red"]
                    return tone(p["silver"], face), None
        return tone(p["black"] if noise2(x * 0.5 + z * 0.3, y * 0.4, 4) < 0.6 else p["black_light"], face), None

    def tongue(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        return abs((u / max(W, 1e-6)) - 0.5) < 0.5 - 0.5 * (v / max(H, 1e-6)) ** 1.5

    def wingf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if math.sin(x * 0.9) * math.sin(y * 0.8) > 0.88:
            return tone(p["eye"], face), None
        return tone(p["black"], face), None

    def build():
        m = Model(name)
        if not nene:
            top = m.bone(name, None, (0, 0, 0))
            bd = m.bone("body", top, (0, 8, 0))
            for i in range(7):
                r = 5.0 - abs(i - 3) * 0.6
                m.round_box(bd, 0.6 * math.sin(i), 0, r, r * 0.6, 6.0 + i * 4.6, 11.0 + i * 4.6, smokef, cut=1)
            for j in range(14):                                                          # flame-like tongues
                ang = math.radians(-160 + j * 23)
                c = (5.0 * math.cos(ang), 10.0 + j * 2.2, 0.0)
                m.box(bd, c[0] - 1.6, c[1], 0, c[0] + 1.6, c[1] + 6.0, 0, cutout(tongue, smokef),
                      rotation=(0, 0, -math.degrees(math.atan2(c[0], 6.0))), pivot=c)
            return m
        mats = {"skin": fabric(P, "black", "black_light", axis="y", period=3.0), "neck": skin(P, "face"),
                "hand": skin(P, "face"), "finger": skin(P, "face")}
        a = humanoid(m, mats, bulk=0.7, arm_bulk=0.7, leg_bulk=0.75, name=name)
        m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]
        m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
        bd = a["body"]
        for i in range(8):                                                               # long gown pooling to smoke
            r = 4.0 + i * 1.2
            m.round_box(bd, i * 0.6, i * 0.8, r, r * 0.9, 32.0 - (i + 1) * 4.0, 32.0 - i * 4.0 + 0.2, smokef,
                        cut=max(1, round(r * 0.3)))
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.2, 2.4, 54.0, 59.6, skin(P, "face"), cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.6), 57.0, -2.9, max(sx * 0.6, sx * 1.6), 57.6, -2.7, solid(P, "black"))
            m.round_box(hd, sx * 1.6, 0.6, 0.9, 0.9, 59.0, 66.0, strands(P, "hair", "hair_dark"), cut=0)   # tall bunches
        m.box(hd, -2.2, 46.0, 0.6, 2.2, 59.0, 2.6, strands(P, "hair", "hair_dark"))
        for j in range(5):                                                               # ragged shadow wing
            ang = math.radians(15 + j * 14)
            x0, x1 = sorted((-3.0, -3.0 - 30.0 + j * 3.0))
            m.box(bd, x0, 48.0, 4.0 + j * 0.3, x1, 54.0, 4.0 + j * 0.3, cutout(tongue, wingf),
                  rotation=(0, 0, -math.degrees(ang)), pivot=(-3.0, 50.0, 4.0))
        return m

    return build
