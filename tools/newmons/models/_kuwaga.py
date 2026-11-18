"""Shared builder for Grandis Kuwagamon, its Honey Mode and Gran Kuwagamon (CobbleEffort: Digital; hand-built after
the official art on wikimon.net). Grandis: an armoured stag-beetle titan standing upright in black-and-silver plate,
two huge glowing blade-mandibles crossed in an X behind it like wings, red eyes, a crest of orange spines, long clawed
hands and heavy clawed legs. Honey Mode: the same titan in black with yellow-gold armour and four orange blade-wings.
Gran Kuwagamon: the beast form, a long black-and-silver stag beetle with jagged mandibles, red eyes, four pink
translucent wings and six bladed legs. Shiny: crimson.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import armour, local, metal, solid
from _route import pal, tone


def make(name, look="grandis"):
    base = {"black": (40, 40, 46), "black_dark": (14, 14, 18), "black_light": (110, 110, 120), "silver": (200, 204, 216),
            "silver_dark": (100, 104, 116), "blade": (220, 224, 236, 230), "glow": (255, 220, 120),
            "eye": (230, 40, 40), "orange": (240, 120, 30), "yellow": (250, 200, 40), "yellow_dark": (180, 130, 10),
            "wing": (240, 150, 170, 130), "vein": (60, 50, 60, 220)}
    shiny = {"black": (120, 20, 30), "black_dark": (60, 8, 12), "black_light": (200, 80, 90)}

    def P(v):
        return pal(base, shiny, v)

    ARM = armour(P, "black", "black_dark", light="black_light", trim="silver", trim_w=0.3)
    SILVER = metal(P, "silver", dark="silver_dark")
    GOLD = armour(P, "yellow", "yellow_dark", trim="black", trim_w=0.3)

    def bladef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        if min(v, H - v) < 0.6 and look == "grandis":
            return p["glow"], p["glow"]
        c = p["orange"] if look == "honey" else p["blade"]
        return c, None

    def wingf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        if (u % 3.0) < 0.3 or abs(v - H * 0.5) < 0.25:
            return p["vein"], None
        return p["wing"], None

    def build():
        m = Model(name)
        if look == "gran":                                                         # the stag-beetle beast
            top = m.bone(name, None, (0, 0, 0))
            bd = m.bone("body", top, (0, 12, 0))
            for j, (r, z0) in enumerate(((6.0, -8.0), (7.0, -1.0), (6.0, 7.0), (4.0, 14.0))):
                m.round_box(bd, 0, z0, r, 3.4, 8.0, 8.0 + r * 1.4, ARM, cut=1)
            hd = m.bone("head", bd, (0, 12, -11))
            m.round_box(hd, 0, -13.0, 4.0, 3.0, 8.0, 15.0, ARM, cut=1)
            for sx in (-1, 1):
                m.box(hd, min(sx * 2.0, sx * 3.6), 12.0, -16.2, max(sx * 2.0, sx * 3.6), 13.2, -15.9, solid(P, "eye", glow=True))
                pts = [(sx * 2.4, 11.0, -15.0), (sx * 6.0, 13.0, -22.0), (sx * 4.0, 12.0, -28.0), (sx * 1.0, 10.0, -30.0)]
                for p0, p1 in zip(pts, pts[1:]):                                   # jagged mandibles
                    rod(m, hd, p0, p1, 2, SILVER, extend=0.4)
                    spike(m, hd, p1, (-sx * 1, 0, -0.2), 0.8, 2.0, SILVER, tip=0.8)
            for side in (1, -1):
                for j in range(2):
                    x0, x1 = sorted((side * 2.0, side * (26.0 - j * 4.0)))
                    m.box(bd, x0, 17.0 + j, -2.0 + j * 4.0, x1, 17.4 + j, 4.0 + j * 4.0, wingf,
                          rotation=(0, side * (10 - j * 25), side * 10), pivot=(side * 2.0, 17.0, 0))
            for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
                lg = m.bone(nm, bd, (sx * 5.0, 10.0, 0))
                for j, z in enumerate((-6.0, 0.0, 7.0)):
                    knee = (sx * 12.0, 14.0, z)
                    rod(m, lg, (sx * 5.0, 10.0, z), knee, 2, ARM, extend=0.4)
                    rod(m, lg, knee, (sx * 15.0, 0.6, z + (j - 1) * 3.0), 2, SILVER, extend=0.4)
                    spike(m, lg, knee, (sx * 0.4, 0.6, 0.4), 1.0, 3.0, SILVER, tip=0.8)
            return m
        mats = {"skin": ARM, "chest": GOLD if look == "honey" else ARM, "deltoid": GOLD if look == "honey" else ARM,
                "claw": SILVER, "talon": SILVER}
        a = humanoid(m, mats, bulk=1.1, arm_bulk=1.1, leg_bulk=1.15, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.8, 3.2, 53.4, 60.0, ARM, cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.2), 57.4, -3.9, max(sx * 0.8, sx * 2.2), 58.2, -3.7, solid(P, "eye", glow=True))
        for j in range(5):                                                         # orange spine crest
            spike(m, hd, ((j - 2) * 0.8, 59.6, 0.6), ((j - 2) * 0.2, 1, 0.5), 1.0, 4.0, solid(P, "orange"), tip=0.8)
        n = 4 if look == "honey" else 2
        for i in range(n):                                                         # crossed blades / wings
            ang = math.radians((45 + 90 * i) if n == 4 else (45 if i == 0 else 135))
            for sgn in ((1, -1) if n == 2 else (1,)):
                a0 = ang if sgn > 0 else ang + math.pi
                c = (0, 48.0, 5.0)
                L = 34.0
                m.box(bd, -1.6, 48.0, 5.0, 1.6, 48.0 + L, 5.6, bladef,
                      rotation=(0, 0, math.degrees(a0) - 90), pivot=c)
        return m

    return build
