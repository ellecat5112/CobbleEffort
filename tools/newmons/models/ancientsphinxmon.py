"""Ancient Sphinxmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the ancient warrior of darkness, a black lion sphinx. Black armour edged in gold over a
crouching lion's body, a pharaoh's headdress with a red jewel, glowing red eyes, gold bands and great gold claws,
a mechanical tail and two huge wings of long gold blade-feathers. 35 blocks tall.

Front is -z, y is up. 58 units tall (the wings); Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 58
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a black lion sphinx in gold-edged armour: a pharaoh headdress with a red jewel, glowing red eyes, gold claws, "
        "a mechanical tail and two huge wings of gold blade-feathers")
BASE = {"black": (36, 36, 44), "black_dark": (12, 12, 16), "black_light": (100, 102, 120), "gold": (226, 176, 60),
        "gold_dark": (150, 104, 26), "gold_light": (255, 236, 160), "red": (220, 30, 30), "red_light": (255, 140, 130),
        "eye": (255, 50, 40), "mouth": (80, 10, 10), "tooth": (240, 236, 220), "tongue": (180, 50, 60)}
SHINY = {"black": (230, 226, 210), "black_dark": (160, 150, 130), "black_light": (255, 255, 250),
         "red": (40, 120, 230), "red_light": (160, 210, 255), "eye": (60, 170, 255)}


def P(v):
    return pal(BASE, SHINY, v)


BLACK = armour(P, "black", "black_dark", light="black_light", trim="gold")
BLACK_PLAIN = armour(P, "black", "black_dark", light="black_light")
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(y - 33.6) < 0.5 and 0.7 < abs(x) < 2.2:
        return p["eye"], p["eye"]
    return BLACK(x, y, z, face, variant, box=box, **k)


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(v / max(H, 1e-6) - 0.5) < 0.12:
        return tone(p["gold_dark"], face), None
    return GOLD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ancientsphinxmon")
    mats = {"skin": BLACK_PLAIN, "belly": BLACK, "neck": BLACK, "head": headf, "snout": BLACK_PLAIN,
            "jaw": BLACK_PLAIN, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "tongue": solid(P, "tongue"),
            "leg_upper": BLACK, "leg_lower": BLACK_PLAIN, "paw": BLACK, "claw": GOLD, "tail": GOLD}
    a = quadruped(m, mats, "ancientsphinxmon", length=30.0, body_y=18.0, body_rx=7.0, body_ry=7.0, chest_bulk=1.25,
                  neck=((0, 26, -15), (0, 31, -18)), head_len=10.0, head_w=4.6, head_h=5.2, snout=0.35,
                  mouth_open=10, teeth=4, leg_bulk=1.5, toes=3,
                  tail=((0, 22, 18), (0, 26, 24), (2, 30, 28)), tail_r=(1.4, 1.2, 1.0))
    hd = a["head"]
    hx, hy, hz = 0, 31, -18
    for sx in (-1, 1):                                           # the pharaoh's headdress: flaps down to the chest
        m.box(hd, min(sx * 4.4, sx * 6.0), 23.0, -20.0, max(sx * 4.4, sx * 6.0), 36.5, -15.0, BLACK,
              rotation=(0, 0, sx * 8), pivot=(sx * 4.4, 36.0, -17.5))
        spike(m, hd, (sx * 4.0, 37.0, -16.0), (sx * 0.8, 0.8, 0.3), 1.6, 4.6, GOLD, tip=0.8)
    m.box(hd, -4.6, 35.0, -21.0, 4.6, 37.5, -14.0, GOLD)                                 # gold band
    m.box(hd, 0 - 1.0, 35.4, -21.6 - 0.6, 0 + 1.0, 37.2, -21.6 + 0.6, gem(P, "red", "red_light"))
    rod(m, hd, (0, 22.0, -21.0), (0, 18.0, -21.0), 2, GOLD, extend=0.2)                  # pharaoh beard
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # wings of long gold blade-feathers
        wb = m.bone(nm, a["body"], (sx * 5.0, 24.0, -6.0))
        rod(m, wb, (sx * 5.0, 24.0, -6.0), (sx * 12.0, 36.0, -4.0), 3, GOLD, extend=0.3)
        for i in range(6):
            t = i / 5
            base = (sx * (6.0 + 6.0 * t), 26.0 + 10.0 * t, -5.0 + 1.0 * t)
            ln = 14.0 + 10.0 * (1 - abs(t - 0.6))
            x0, x1 = sorted((base[0], base[0] + sx * ln))
            m.box(wb, x0, base[1] - 1.2, base[2], x1, base[1] + 1.2, base[2] + 1, bladef,
                  rotation=(0, 0, sx * (10 + 18 * t)), pivot=base)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        lg = a[nm]
        wr = lg["wrist"]
        m.round_box(lg["bone"], wr[0], wr[2], 2.2, 2.2, 4.0, 6.0, GOLD, cut=1)            # gold anklets
    return m
