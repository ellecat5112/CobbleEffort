"""DORUguremon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the great beast dragon. A long, low four-legged dragon of crimson scales striped with black
zigzags, a white belly and shaggy white chest and paws, a horned crimson head with a white mane, a fan of curved
silver blade-wings rising from its back fixed with gold clamps, black claws and a long coiling tail ending in a
spinning gold drill. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, metal, scales, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a long low crimson dragon striped with black zigzags, a white chest and mane, a fan of silver blade-wings with "
        "gold clamps and a long coiling tail ending in a gold drill")
BASE = {"red": (200, 40, 40), "red_dark": (110, 14, 18), "red_light": (250, 120, 110), "black": (30, 26, 30),
        "white": (246, 246, 250), "white_dark": (190, 190, 206), "silver": (220, 224, 236), "silver_dark": (110, 114, 128),
        "gold": (240, 196, 60), "gold_dark": (160, 110, 20), "eye": (250, 200, 40), "mouth": (120, 20, 30),
        "tooth": (250, 250, 246), "claw": (40, 40, 46)}
SHINY = {"red": (60, 80, 180), "red_dark": (20, 30, 90), "red_light": (140, 160, 240)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "red", "red_dark", size=1.6, light="red_light", rim_mix=0.3)
WHITE = fur(P, "white", "white_dark", length=1.4)
SILVER = metal(P, "silver", dark="silver_dark")
GOLD = metal(P, "gold", dark="gold_dark")


def zig(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "up") and abs((y + abs((z * 0.6) % 2.0 - 1.0) * 2.0) % 4.0 - 2.0) < 0.35:
        return tone(p["black"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("doruguremon")
    mats = {"skin": zig, "belly": WHITE, "neck": WHITE, "head": zig, "snout": zig, "jaw": zig,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": zig, "leg_lower": WHITE, "paw": WHITE,
            "claw": solid(P, "claw"), "tail": zig}
    a = quadruped(m, mats, "doruguremon", length=40.0, body_y=16.0, body_rx=7.0, body_ry=6.6, chest_bulk=1.2,
                  neck=((0, 20, -20), (0, 24, -26)), head_len=10.0, head_w=3.6, head_h=4.0, snout=0.6, mouth_open=14,
                  teeth=4, leg_bulk=1.5, toes=4,
                  tail=((0, 18, 22), (6, 22, 30), (12, 28, 32), (14, 32, 26), (12, 28, 20)),
                  tail_r=(3.0, 2.4, 1.8, 1.4, 1.2))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.6,
              solid(P, "eye", glow=True))
        for j in range(3):                                                         # swept horns
            spike(m, hd, (sx * 2.0, ey + 1.6, ez + 1.0 + j * 1.6), (sx * 0.3, 0.7, 1), 1.2, 6.0 - j, zig, tip=0.3)
    for i in range(8):                                                             # white mane
        spike(m, hd, ((i - 3.5) * 0.7, ey + 1.0, ez + 3.0), ((i - 3.5) * 0.2, 0.4, 1), 1.2, 5.0, WHITE, tip=0.4)
    for side in (1, -1):                                                           # fan of silver blade-wings
        for j in range(5):
            ang = math.radians(15 + j * 16)
            base = (side * 4.0, 22.0, -6.0 + j * 3.0)
            tip = (side * (4.0 + 20.0 * math.cos(ang)), 22.0 + 18.0 * math.sin(ang), -2.0 + j * 4.0)
            rod(m, bd, base, tip, 1, SILVER, extend=0.5, t2=3)
            m.round_box(bd, base[0] + side * 1.6, base[2], 1.2, 1.2, base[1] - 0.6, base[1] + 1.4, GOLD, cut=0)
            spike(m, bd, tip, tuple(t - b for t, b in zip(tip, base)), 1.0, 2.0, GOLD, tip=0.3)
    e = a["tail_pts"][-1]                                                           # gold tail drill
    spike(m, a["tail"], e, (-0.3, -0.6, -1), 3.0, 7.0, GOLD, tip=1.0)
    return m
