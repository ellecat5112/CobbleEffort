"""Flymon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
giant wasp. A big yellow wasp with a black-and-yellow striped abdomen ending in a long stinger, magenta-pink wings,
a round yellow head with large red compound eyes and fanged mandibles, a black thorax and six black legs with
claws. 15 blocks tall.

Front is -z, y is up. 32 units tall; Adult stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, local, metal, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = ("a big yellow wasp with a striped abdomen and long stinger, magenta-pink wings, red compound eyes, fanged "
        "mandibles, a black thorax and six clawed black legs")
BASE = {"yellow": (250, 210, 40), "yellow_dark": (190, 140, 10), "black": (34, 32, 38), "black_dark": (14, 14, 18),
        "eye": (200, 30, 40), "eye_light": (255, 120, 110), "steel": (220, 220, 230), "steel_dark": (120, 120, 130),
        "wing": (240, 80, 180, 150), "vein": (170, 30, 120, 220)}
SHINY = {"yellow": (120, 220, 120), "yellow_dark": (50, 150, 50), "wing": (80, 180, 250, 150)}


def P(v):
    return pal(BASE, SHINY, v)


YELLOW = armour(P, "yellow", "yellow_dark", trim="black", trim_w=0.2)
BLACK = metal(P, "black", dark="black_dark")


def stripef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (z * 0.45) % 2.0 < 0.9:
        return tone(p["black"], face), None
    return YELLOW(x, y, z, face, variant, box=box, **k)


def eyef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    on = (int(x * 1.6) + int(y * 1.6) + int(z * 1.6)) % 2
    return tone(p["eye_light"] if on else p["eye"], face), None


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (u % 3.0) < 0.3 or abs(v - H * 0.5) < 0.25:
        return p["vein"], None
    return p["wing"], None


def build():
    m = Model("flymon")
    top = m.bone("flymon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, -2.0, 4.4, 4.0, 14.0, 22.0, BLACK, cut=1)                         # thorax
    ab_ = m.bone("abdomen", bd, (0, 16, 2))
    for j in range(6):                                                                   # striped abdomen
        r = 5.4 - abs(j - 2) * 0.7
        m.round_box(ab_, 0, 4.0 + j * 2.8, r, r, 16.0 - j * 1.4 - r, 16.0 - j * 1.4 + r, stripef, cut=2)
    spike(m, ab_, (0, 7.0, 20.0), (0, -0.6, 1), 1.4, 8.0, metal(P, "steel", dark="steel_dark"), tip=0.2)
    hd = m.bone("head", bd, (0, 20, -6))
    m.round_box(hd, 0, -8.0, 4.0, 3.4, 15.0, 23.0, YELLOW, cut=2)
    for sx in (-1, 1):
        m.round_box(hd, sx * 3.0, -9.6, 1.8, 2.0, 17.6, 22.0, eyef, cut=1)               # red compound eyes
        spike(m, hd, (sx * 1.4, 15.6, -11.0), (-sx * 0.5, -0.5, -1), 1.0, 3.0, BLACK, tip=0.2)  # fanged mandibles
        rod(m, hd, (sx * 1.2, 22.6, -9.0), (sx * 4.0, 28.0, -12.0), 1, BLACK, extend=0.2, t2=1) # antennae
    for side in (1, -1):                                                                 # magenta wings
        for j, (ang, ln) in enumerate(((22, 20.0), (-8, 15.0))):
            x0, x1 = sorted((side * 3.0, side * (3.0 + ln)))
            m.box(bd, x0, 21.0 - j * 2.5, 1.0 + j * 1.0, x1, 26.0 - j * 2.5, 1.0 + j * 1.0, wingf,
                  rotation=(0, side * 25, side * ang), pivot=(side * 3.0, 23.0, 1.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                  # six clawed legs
        lg = m.bone(nm, bd, (sx * 3.0, 15.0, -2.0))
        for j, dz in enumerate((-5.0, -2.0, 1.0)):
            rod(m, lg, (sx * 3.0, 15.0, dz), (sx * 7.0, 9.0, dz - 1.0), 1, BLACK, extend=0.3, t2=1)
            rod(m, lg, (sx * 7.0, 9.0, dz - 1.0), (sx * 6.0, 2.0, dz - 2.0), 1, BLACK, extend=0.3, t2=1)
            spike(m, lg, (sx * 6.0, 2.0, dz - 2.0), (0, -0.4, -1), 0.6, 1.6, BLACK, tip=0.2)
    return m
