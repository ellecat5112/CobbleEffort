"""Shared builder for JESmon, JESmon (X-Antibody) and JESmon GX (CobbleEffort: Digital; hand-built at the detail
standard after the official art on wikimon.net): the newest Royal Knight. JESmon: a white-armoured knight with a ribbed
breastplate, a horned crested helm, a tattered red cape, a long red sword etched with script, and four blazing golden
flame-blades (its Sistermon guardians' fire) fanned behind. X: red-and-gold spiked armour, thorny limbs, a great red
blade and wings of jagged gold crystal shards. GX: a slender red-and-gold knight with a long lance and wide wings of
cyan-and-gold light shards.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, humanoid
from _digidetail import armour, cutout, fabric, flame_inside, gem, local, metal, noise2, solid
from _route import pal, tone


def make(name, look="base"):
    base = {"white": (240, 240, 246), "white_dark": (160, 164, 184), "white_light": (255, 255, 255),
            "red": (210, 30, 40), "red_dark": (120, 10, 20), "red_light": (250, 120, 110), "gold": (250, 200, 70),
            "gold_dark": (170, 120, 20), "gold_light": (255, 240, 170), "cyan": (90, 230, 250), "cyan_light": (220, 255, 255),
            "eye": (250, 220, 60), "black": (30, 30, 36), "fire": (255, 190, 60, 210), "fire_core": (255, 250, 210, 240),
            "shard": (255, 220, 110, 200), "shard_light": (255, 250, 220, 230)}
    shiny = {"white": (60, 60, 76), "white_dark": (20, 20, 30), "red": (40, 90, 220), "red_dark": (14, 30, 120),
             "fire": (120, 200, 255, 210), "shard": (140, 220, 255, 200)}

    def P(v):
        return pal(base, shiny, v)

    WHITE = armour(P, "white", "white_dark", light="white_light", trim="gold", trim_w=0.25)
    RED = armour(P, "red", "red_dark", light="red_light", trim="gold", trim_w=0.25)
    GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
    BODY = WHITE if look == "base" else RED

    def ribf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and abs(x) < 4.0 and (y % 1.8) < 0.6 and 42.0 < y < 50.0:
            return tone(p["gold"] if look != "base" else p["white_dark"], face), None
        return BODY(x, y, z, face, variant, box=box, **k)

    def firef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
        return c, c[:3]

    def shardf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        c = p["shard_light"] if (u + v) % 3.0 < 0.8 else (p["cyan"] + (200,) if look == "gx" and (u - v) % 4.0 < 1.0
                                                           else p["shard"])
        return c, c[:3]

    def shard_in(xx, y, z, face, box):
        u, v, W, H = local(xx, y, z, face, box)
        a, b = u / max(W, 1e-6), v / max(H, 1e-6)
        if W > H:
            a, b = b, a
        return abs(a - 0.5) < 0.5 * (1 - b) + 0.1 * abs(math.sin(b * 9.0))

    def build():
        m = Model(name)
        mats = {"skin": BODY, "chest": ribf, "abs": BODY, "pelvis": BODY, "neck": GOLD, "deltoid": BODY,
                "upper_arm": BODY, "forearm": BODY, "hand": BODY, "finger": BODY, "claw": GOLD, "thigh": BODY,
                "knee": GOLD, "shin": BODY, "calf": BODY, "foot": BODY, "talon": GOLD, "toe": GOLD}
        lean = look == "gx"
        a = humanoid(m, mats, bulk=0.85 if lean else 1.0, arm_bulk=0.9, leg_bulk=0.9 if lean else 1.0,
                     digitigrade=look != "base", talons=look != "base", name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 60.4, BODY, cut=1)
        m.round_box(hd, 0, -3.2, 2.0, 0.4, 56.4, 58.0, solid(P, "black"), cut=0)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.8), 56.8, -3.7, max(sx * 0.6, sx * 1.8), 57.6, -3.6, solid(P, "eye", glow=True))
            pts = [(sx * 2.4, 59.0, 0), (sx * 5.0, 63.0, 1.0), (sx * 6.0, 67.0, 3.0)]               # swept horns
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 1, GOLD, extend=0.3, t2=2)
        spike(m, hd, (0, 60.0, -1.6), (0, 1, 0.2), 1.6, 5.0, GOLD, tip=0.8)
        for sx in (-1, 1):                                                       # pauldrons
            m.round_box(bd, sx * 7.6, 0.0, 3.4, 3.6, 47.0, 53.0, BODY, cut=2)
            for j in range(3 if look != "base" else 1):
                spike(m, bd, (sx * 9.0, 52.0 - j * 2.0, 0), (sx * 0.8, 0.6, 0.2), 1.2, 5.0, GOLD, tip=0.8)
        if look != "base":                                                       # thorny limbs
            for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):
                anc = a[nm]
                j = anc.get("elbow") or anc.get("knee")
                sx = 1 if j[0] > 0 else -1
                for t in range(2):
                    spike(m, anc["bone"], (j[0], j[1] - t * 3.0, j[2]), (sx, 0.2, 0.6), 1.0, 4.0, GOLD, tip=0.8)
        hr = a["arm_right"]
        hx, hy, hz = hr["hand"]
        if look == "gx":                                                         # long lance
            rod(m, hr["bone"], (hx + 6.0, hy + 4.0, hz + 6.0), (hx - 22.0, hy - 10.0, hz - 14.0), 1,
                metal(P, "red", dark="red_dark"), extend=0, t2=1)
            spike(m, hr["bone"], (hx - 22.0, hy - 10.0, hz - 14.0), (-1.0, -0.5, -0.7), 1.6, 8.0, GOLD, tip=0.8)
        else:                                                                     # long red sword
            m.round_box(hr["bone"], hx, hz, 0.8, 0.8, hy - 2.0, hy + 2.0, GOLD, cut=0)
            m.round_box(hr["bone"], hx, hz, 3.0, 0.8, hy - 2.6, hy - 1.8, GOLD, cut=0)
            m.round_box(hr["bone"], hx, hz - 0.4, 1.2 if look == "base" else 1.8, 0.4, hy - 30.0, hy - 2.6,
                        metal(P, "red", dark="red_dark", light="red_light"), cut=0)
            spike(m, hr["bone"], (hx, hy - 30.0, hz - 0.4), (0, -1, 0), 2.4, 3.0, metal(P, "red", dark="red_dark"), tip=0.8)
        if look == "base":
            cape(m, bd, 53.0, 14.0, 40.0, fabric(P, "red", "red_dark"), z=4.0, flare=0.8, panels=8)
            for i in range(4):                                                    # four flame blades
                ang = math.radians(-60 + i * 40)
                c = (18.0 * math.sin(ang), 48.0 + 12.0 * math.cos(ang), 8.0)
                for rot in (0, 90):
                    m.box(bd, c[0] - 4.5, c[1], c[2], c[0] + 4.5, c[1] + 24.0, c[2],
                          cutout(flame_inside(4, 0.1, i), firef), rotation=(0, rot, -math.degrees(ang) * 0.6),
                          pivot=(c[0], c[1], c[2]))
                rod(m, bd, (c[0] * 0.8, c[1] - 6.0, c[2]), c, 1, GOLD, extend=0, t2=1)
        else:                                                                     # crystal shard wings
            S = cutout(shard_in, shardf)
            for side in (1, -1):
                wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 50.0, 4.0))
                for j in range(5):
                    th = -25 + j * 24
                    ln = (26.0 if look == "gx" else 22.0) - abs(j - 2) * 2.0
                    x0, x1 = sorted((side * 3.0, side * (3.0 + ln)))
                    m.box(wb, x0, 48.0, 4.0, x1, 54.0, 4.0, S,
                          rotation=(0, side * -15, side * th), pivot=(side * 3.0, 50.0, 4.0))
        return m

    return build
