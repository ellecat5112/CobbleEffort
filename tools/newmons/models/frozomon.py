"""Frozomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
snowplough beast. A hulking red armoured machine-beast streaked with frost, riding on black caterpillar treads, with a
broad plough-blade jaw, a small grey face with a yellow eye peering from under a heavy brow plate, steel tusks, two
exhaust stacks bristling with ice-blue spikes, a glowing orange furnace vent on its flank and a back blowing snow.
25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fbm, local, metal, riveted, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = ("a hulking frost-streaked red armoured machine-beast on caterpillar treads with a plough-blade jaw, a grey face "
        "with a yellow eye, steel tusks, ice-spiked exhaust stacks and a glowing orange furnace vent")
BASE = {"red": (200, 40, 40), "red_dark": (110, 14, 18), "red_light": (240, 120, 110), "frost": (230, 236, 246),
        "black": (40, 40, 46), "black_dark": (16, 16, 20), "grey": (130, 134, 146), "grey_dark": (70, 74, 86),
        "steel": (210, 214, 224), "steel_dark": (100, 104, 116), "ice": (130, 200, 250), "ice_dark": (60, 130, 200),
        "eye": (250, 220, 60), "glow": (255, 170, 40), "glow_core": (255, 240, 170), "tusk": (240, 236, 220)}
SHINY = {"red": (60, 120, 200), "red_dark": (20, 50, 110), "red_light": (150, 200, 250), "glow": (120, 250, 220)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "red", "red_dark", light="red_light", trim="black", trim_w=0.3, rivets=True)
BLACK = riveted(P, "black", "black_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def frostf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if fbm(x * 0.4, y * 0.4, z * 0.4, seed=7) > 0.62:
        return tone(p["frost"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def treadf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot((z % 4.0) - 2.0, y - 3.0) < 1.4:
        return tone(p["grey"], face), None
    if (z * 1.0) % 2.0 < 0.5 or (y * 1.0) % 2.0 < 0.4 and face in ("up", "down"):
        return tone(p["black_dark"], face), None
    return tone(p["black"], face), None


def ventf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["glow_core"] if abs(v - H / 2) < H * 0.2 else p["glow"]
    return c, c


def build():
    m = Model("frozomon")
    top = m.bone("frozomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                # caterpillar treads
        lg = m.bone(nm, top, (sx * 9.0, 4.0, 0))
        x0, x1 = sorted((sx * 6.0, sx * 12.0))
        m.round_box(lg, sx * 9.0, 2.0, 3.0, 13.0, 0.0, 8.0, treadf, cut=2)
    m.round_box(bd, 0, 2.0, 10.0, 12.0, 8.0, 24.0, frostf, cut=3)                      # hulking body
    m.round_box(bd, 0, 4.0, 8.0, 8.0, 22.0, 30.0, frostf, cut=2)
    for sx in (-1, 1):
        m.box(bd, sx * 10.0 - 0.3 if sx > 0 else -10.3, 12.0, -2.0, sx * 10.0 + 0.3 if sx > 0 else -9.7, 18.0, 6.0,
              ventf)                                                                   # furnace vents
    hd = m.bone("head", bd, (0, 18, -10))
    m.round_box(hd, 0, -12.0, 7.0, 3.0, 12.0, 24.0, frostf, cut=2)                     # face block
    m.round_box(hd, 0, -14.0, 9.0, 2.0, 8.0, 16.0, STEEL, cut=1)                       # plough-blade jaw
    m.round_box(hd, 0, -15.2, 4.0, 1.0, 17.0, 21.0, solid(P, "grey"), cut=0)           # grey face
    m.box(hd, 1.0, 19.0, -16.3, 2.6, 20.0, -16.1, solid(P, "eye", glow=True))
    m.box(hd, -2.6, 19.0, -16.3, -1.0, 20.0, -16.1, solid(P, "eye", glow=True))
    m.round_box(hd, 0, -14.4, 6.0, 2.4, 21.0, 24.0, ARM, cut=1)                        # heavy brow plate
    for sx in (-1, 1):
        spike(m, hd, (sx * 6.0, 10.0, -15.0), (sx * 0.3, -0.4, -1), 1.6, 5.0, solid(P, "tusk"), tip=0.3)
    for sx in (-1, 1):                                                                  # exhaust stacks + ice spikes
        rod(m, bd, (sx * 5.0, 26.0, 4.0), (sx * 5.0, 38.0, 6.0), 3, BLACK, extend=0.3)
        for j in range(5):
            ang = math.radians(j * 72)
            spike(m, bd, (sx * 5.0 + 2.6 * math.cos(ang), 33.0, 5.0 + 2.6 * math.sin(ang)),
                  (math.cos(ang), 0.2, math.sin(ang)), 1.2, 3.4, metal(P, "ice", dark="ice_dark"), tip=0.2)
    for j in range(6):                                                                  # spiked back
        spike(m, bd, ((j - 2.5) * 2.4, 22.0, 12.0), (0, 0.3, 1), 1.4, 5.0, metal(P, "ice", dark="ice_dark"), tip=0.2)
    return m
