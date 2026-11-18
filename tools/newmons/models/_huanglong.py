"""Shared builder for Huanglongmon and Huanglongmon: Ruin Mode (CobbleEffort: Digital; hand-built after the official
art on wikimon.net): the yellow dragon, lord of the Four Holy Beasts: a great four-legged golden dragon armoured in
gleaming gold scale plates, a long horned head with flowing whiskers, a mane of jade spines down its back, twelve
glowing orbs round its body and a long armoured tail. Ruin Mode: dark violet armour, three heads on long necks and
cold blue flames pouring from its mouths and back. Shiny: silver-white (base) / crimson (Ruin).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import armour, cutout, flame_inside, gem, local, metal, scales, skin, solid, strands
from _route import pal, tone


def make(name, ruin=False):
    if not ruin:
        base = {"gold": (250, 200, 60), "gold_dark": (170, 110, 14), "gold_light": (255, 240, 160), "jade": (60, 190, 130),
                "jade_dark": (20, 110, 70), "orb": (120, 230, 200), "orb_light": (230, 255, 245), "eye": (220, 40, 40),
                "mouth": (180, 40, 40), "tooth": (250, 248, 236), "whisker": (250, 240, 200), "fire": (255, 210, 80, 210),
                "fire_core": (255, 250, 210, 240)}
        shiny = {"gold": (230, 232, 240), "gold_dark": (140, 144, 160), "gold_light": (255, 255, 255)}
    else:
        base = {"gold": (90, 50, 130), "gold_dark": (34, 14, 60), "gold_light": (170, 120, 210), "jade": (60, 90, 200),
                "jade_dark": (20, 30, 110), "orb": (90, 160, 255), "orb_light": (220, 240, 255), "eye": (250, 220, 60),
                "mouth": (40, 60, 160), "tooth": (230, 230, 240), "whisker": (180, 170, 220), "fire": (80, 160, 255, 210),
                "fire_core": (220, 245, 255, 240)}
        shiny = {"gold": (150, 30, 40), "gold_dark": (60, 8, 14), "gold_light": (230, 110, 110),
                 "fire": (255, 120, 60, 210), "orb": (255, 140, 80)}

    def P(v):
        return pal(base, shiny, v)

    SC = scales(P, "gold", "gold_dark", size=1.8, light="gold_light", rim_mix=0.5)
    PLATE = armour(P, "gold", "gold_dark", light="gold_light", trim="jade", trim_w=0.3)
    SPINE = strands(P, "jade", "jade_dark")

    def firef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
        return c, c[:3]

    FIRE = cutout(flame_inside(4, 0.1, 3), firef)

    def head(m, bone, c, s):
        """A horned dragon head with whiskers centred at c (looking -z), scale s."""
        x, y, z = c
        m.round_box(bone, x, z, 3.4 * s, 4.4 * s, y - 2.6 * s, y + 3.0 * s, SC, cut=max(1, round(s)))
        m.round_box(bone, x, z - 6.0 * s, 2.4 * s, 3.0 * s, y - 1.6 * s, y + 1.4 * s, SC, cut=max(1, round(s)))
        m.round_box(bone, x, z - 5.0 * s, 2.2 * s, 3.2 * s, y - 3.6 * s, y - 2.0 * s, solid(P, "mouth"), cut=0)
        for sx in (-1, 1):
            m.box(bone, min(x + sx * 3.0 * s, x + sx * 3.5 * s), y + 0.8 * s, z - 3.4 * s,
                  max(x + sx * 3.0 * s, x + sx * 3.5 * s), y + 1.8 * s, z - 1.6 * s, solid(P, "eye", glow=True))
            pts = [(x + sx * 2.0 * s, y + 2.6 * s, z + 1.0 * s), (x + sx * 3.4 * s, y + 6.6 * s, z + 4.0 * s),
                   (x + sx * 3.0 * s, y + 9.0 * s, z + 8.0 * s)]
            for p0, p1 in zip(pts, pts[1:]):                                       # antlered horns
                rod(m, bone, p0, p1, max(1, round(1.2 * s)), metal(P, "gold_light", dark="gold"), extend=0.3)
            wp = [(x + sx * 2.2 * s, y - 0.6 * s, z - 7.6 * s), (x + sx * 5.0 * s, y - 2.4 * s, z - 6.0 * s),
                  (x + sx * 8.0 * s, y - 5.0 * s, z - 2.0 * s)]
            for p0, p1 in zip(wp, wp[1:]):                                         # whiskers
                rod(m, bone, p0, p1, 1, solid(P, "whisker"), extend=0.2, t2=1)
            for j in range(3):
                spike(m, bone, (x + sx * (1.0 + j * 0.6) * s, y - 2.0 * s, z - 7.6 * s), (0, -1, 0), 0.8, 1.4 * s,
                      solid(P, "tooth"), tip=0.8)

    def build():
        m = Model(name)
        mats = {"skin": SC, "belly": PLATE, "neck": SC, "head": SC, "snout": SC, "jaw": SC,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": PLATE, "leg_lower": SC,
                "paw": SC, "claw": solid(P, "gold_light"), "tail": SC}
        a = quadruped(m, mats, name, length=34.0, body_y=18.0, body_rx=6.4, body_ry=6.4, chest_bulk=1.25,
                      neck=((0, 24, -15), (0, 30, -19)), head_len=10.0, head_w=3.6, head_h=4.0, snout=0.8,
                      mouth_open=14, teeth=5, leg_bulk=1.3, toes=4,
                      tail=((0, 20, 17), (0, 18, 24), (2, 14, 30), (5, 12, 35)), tail_r=(3.0, 2.4, 1.6, 1.0))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
                  ez + 0.8, solid(P, "eye", glow=True))
            pts = [(sx * 1.6, ey + 1.4, ez + 1.0), (sx * 3.0, ey + 5.0, ez + 4.0), (sx * 2.6, ey + 7.0, ez + 8.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 1, metal(P, "gold_light", dark="gold"), extend=0.3, t2=2)
        for i in range(12):                                                         # jade spine mane
            spike(m, bd if i < 10 else a["neck"], (0, 24.4 if i < 10 else 31.0, -12.0 + i * 3.0 if i < 10 else
                  -18.0 + (i - 10) * 2.0), (0, 1, 0.6), 1.6, 5.0 - (i % 3), SPINE, tip=0.8)
        for i in range(12):                                                         # twelve orbs
            ang = 2 * math.pi * i / 12
            m.round_box(bd, 9.0 * math.cos(ang), 2.0 + 15.0 * math.sin(ang), 1.2, 1.2, 25.0 + (i % 2) * 2.0,
                        27.4 + (i % 2) * 2.0, gem(P, "orb", "orb_light"), cut=0)
        for p in a["tail_pts"][1:]:
            spike(m, a["tail"], p, (0, 1, 0.4), 1.2, 2.6, SPINE, tip=0.8)
        if ruin:
            for sx in (-1, 1):                                                       # two more heads on long necks
                nb = m.bone("neck_left" if sx > 0 else "neck_right", bd, (sx * 4.0, 24.0, -12.0))
                pts = [(sx * 4.0, 24.0, -12.0), (sx * 9.0, 30.0, -16.0), (sx * 12.0, 33.0, -20.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, nb, p0, p1, 3, SC, extend=0.8)
                head(m, nb, (sx * 12.0, 33.0, -23.0), 0.8)
                for ang in (0, 90):
                    m.box(nb, sx * 12.0 - 1.6, 26.0, -29.0, sx * 12.0 + 1.6, 31.0, -29.0, FIRE, rotation=(0, ang, 0),
                          pivot=(sx * 12.0, 26.0, -29.0))
            for j in range(4):                                                      # back flames
                for ang in (0, 90):
                    m.box(bd, -2.0, 25.0, -8.0 + j * 6.0, 2.0, 31.0, -8.0 + j * 6.0, FIRE, rotation=(0, ang, 0),
                          pivot=(0, 25.0, -8.0 + j * 6.0))
        return m

    return build
