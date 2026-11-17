"""Exo Grimmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the armoured dragon of ruin. A hulking crouched dragon in violet-and-black plate with silver
horn-blades, a jutting armoured head with a red-veined fanged maw, curved silver spikes along its shoulders and
back, huge clawed legs with silver talons, a red streak glowing down its flank and two great wings of orange-gold
membrane edged in black. 35 blocks tall.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, quadruped
from _digidetail import armour, cutout, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hulking crouched dragon in violet-and-black plate with silver horn-blades, a fanged armoured head, silver back "
        "spikes, huge silver talons and great orange-gold membrane wings")
BASE = {"violet": (110, 50, 120), "violet_dark": (40, 14, 50), "violet_light": (190, 120, 200), "black": (34, 32, 40),
        "silver": (210, 214, 226), "silver_dark": (100, 104, 116), "red": (220, 40, 50), "wing": (250, 180, 60),
        "wing_dark": (220, 110, 30), "wing_edge": (40, 30, 30), "mouth": (130, 20, 40), "tooth": (250, 248, 240),
        "eye": (250, 60, 60)}
SHINY = {"violet": (60, 110, 60), "violet_dark": (20, 50, 20), "violet_light": (140, 200, 140), "wing": (120, 200, 250),
         "wing_dark": (40, 110, 200)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "violet", "violet_dark", light="violet_light", trim="black", trim_w=0.4)
SILVER = metal(P, "silver", dark="silver_dark")


def flankf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 18.0 - z * 0.15) < 0.6:
        return p["red"], p["red"]
    return PLATE(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = v / max(H, 1e-6)
    return tone(p["wing_edge"] if t < 0.1 else p["wing_dark"] if t < 0.4 else p["wing"], face), None


def build():
    m = Model("exogrimmon")
    mats = {"skin": flankf, "belly": PLATE, "neck": PLATE, "head": PLATE, "snout": PLATE, "jaw": PLATE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": PLATE, "leg_lower": PLATE,
            "paw": PLATE, "claw": SILVER, "tail": PLATE}
    a = quadruped(m, mats, "exogrimmon", length=32.0, body_y=16.0, body_rx=8.0, body_ry=7.6, chest_bulk=1.4,
                  neck=((0, 22, -15), (0, 26, -20)), head_len=11.0, head_w=4.0, head_h=4.4, snout=0.6, mouth_open=22,
                  teeth=5, leg_bulk=2.0, toes=4, tail=((0, 18, 17), (0, 14, 24), (2, 10, 30)), tail_r=(3.0, 2.2, 1.4))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.7, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.7,
              solid(P, "eye", glow=True))
        pts = [(sx * 2.4, ey + 1.6, ez + 1.0), (sx * 5.0, ey + 6.0, ez + 4.0), (sx * 6.0, ey + 8.0, ez + 9.0)]
        for p0, p1 in zip(pts, pts[1:]):                                            # silver horn-blades
            rod(m, hd, p0, p1, 1, SILVER, extend=0.4, t2=2)
        for j in range(3):                                                          # shoulder spikes
            pts = [(sx * 7.0, 22.0, -10.0 + j * 4.0), (sx * 10.0, 28.0, -12.0 + j * 4.0),
                   (sx * 9.0, 32.0, -16.0 + j * 4.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, bd, p0, p1, 1, SILVER, extend=0.3, t2=2)
    for j in range(5):                                                              # back spikes
        spike(m, bd, (0, 24.0, -6.0 + j * 5.0), (0, 1, 0.6), 1.4, 5.0, SILVER, tip=0.3)
    for side in (1, -1):                                                            # great orange-gold wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 5.0, 24.0, -2.0))
        bat_wing(m, wb, (side * 5.0, 24.0, -2.0), 26.0, 22.0, 4, solid(P, "black"), cutout(lambda *a_: True, wingf),
                 side=side, sweep=20)
    return m
