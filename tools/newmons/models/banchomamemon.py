"""Bancho Mamemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the delinquent boss of the Mamemon. A small round armoured body of dark steel under a tattered
black long coat, a blue delinquent's cap pulled low, little blue gloved hands holding a wooden bat and a huge brass
shell-club, and chains hanging all round it, with tiny Mamemon faces bobbing beside it. 35 blocks tall (it is tiny
for a boss, but its pride is not).

Front is -z, y is up. 48 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape
from _digidetail import armour, cutout, fabric, local, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("the delinquent boss Mamemon: a small round dark steel body under a tattered black coat, a blue cap pulled low, "
        "a wooden bat and a huge brass shell-club, and chains hanging all round it")
BASE = {"steel": (90, 92, 104), "steel_dark": (40, 40, 48), "steel_light": (170, 172, 186), "coat": (36, 34, 42),
        "coat_dark": (14, 12, 18), "cap": (40, 60, 150), "cap_dark": (16, 24, 80), "glove": (100, 130, 200),
        "wood": (200, 160, 100), "wood_dark": (130, 90, 50), "brass": (220, 180, 80), "brass_dark": (150, 110, 30),
        "chain": (130, 132, 144), "face": (210, 210, 220), "eye": (30, 30, 40), "red": (200, 40, 50)}
SHINY = {"steel": (170, 120, 70), "steel_dark": (100, 60, 30), "steel_light": (230, 190, 140), "cap": (170, 40, 60),
         "cap_dark": (90, 16, 24), "coat": (220, 216, 230), "coat_dark": (160, 156, 170)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = armour(P, "steel", "steel_dark", light="steel_light", panel=(2.4, 2.4))
COAT = fabric(P, "coat", "coat_dark", axis="y", period=3.0)
CHAIN = metal(P, "chain", dark="steel_dark")


def torn(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.14 * abs(math.sin((box.lo[0] + u) * 2.0)) + 0.03


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if abs(a - sx * 2.6) < 1.0 and abs(b - 24.0) < 0.5:
                return p["eye"], None                            # scowling eyes under the cap
    return STEEL(x, y, z, face, variant, box=box, **k)


def chain(m, bone, a, b):
    n = max(1, round(math.dist(a, b) / 1.6))
    for j in range(n):
        c = tuple(aa + (bb - aa) * (j + 0.5) / n for aa, bb in zip(a, b))
        m.box(bone, c[0] - 0.5, c[1] - 0.5, c[2] - 0.5, c[0] + 0.5, c[1] + 0.5, c[2] + 0.5, CHAIN,
              rotation=(45 * (j % 2), 45, 0), pivot=c)


def build():
    m = Model("banchomamemon")
    top = m.bone("banchomamemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    ball(m, bd, (0, 22.0, 0), 9.0, facef, layers=7)
    hd = m.bone("head", bd, (0, 28, 0))
    m.round_box(hd, 0, 0.4, 7.6, 7.6, 27.0, 31.0, armour(P, "cap", "cap_dark"), cut=2)   # cap
    m.box(hd, -6.0, 26.6, -11.0, 6.0, 27.6, -6.0, armour(P, "cap", "cap_dark"))         # cap brim
    cb = m.bone("cap", bd, (0, 30, 6))                           # tattered black coat
    cape(m, cb, 31.0, 22.0, 30.0, cutout(torn, COAT), z=7.0, flare=1.2, panels=9, sweep=(0, 10))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 8.4, 22.0, -1.0))
        h = (sx * 11.0, 20.0, -4.0)
        rod(m, ab, (sx * 8.4, 22.0, -1.0), h, 2, STEEL, extend=0.3)
        ball(m, ab, h, 1.8, solid(P, "glove"), layers=2)
    ar = m.bone("bat", "arm_right", (-11.0, 20.0, -4.0))         # wooden bat
    rod(m, ar, (-11.0, 18.0, -4.0), (-12.0, 40.0, -2.0), 2, metal(P, "wood", dark="wood_dark"), extend=0, t2=2)
    al = m.bone("club", "arm_left", (11.0, 20.0, -4.0))          # brass shell-club
    rod(m, al, (11.0, 18.0, -4.0), (13.0, 26.0, -3.0), 1, solid(P, "red"), extend=0)
    m.round_box(al, 13.6, -2.8, 2.6, 2.6, 26.0, 44.0, metal(P, "brass", dark="brass_dark"), cut=1)
    spike(m, al, (13.6, 44.0, -2.8), (0, 1, 0), 3.0, 3.0, metal(P, "brass", dark="brass_dark"))
    for i in range(6):                                           # chains hanging round it
        ang = math.radians(-150 + i * 60)
        s = (8.0 * math.sin(ang), 16.0, -8.0 * math.cos(ang))
        chain(m, bd, s, (s[0] * 1.6, 2.0 + (i % 2) * 2, s[2] * 1.6))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.6, 13.0, 0))
        rod(m, lg, (sx * 3.6, 13.0, 0), (sx * 4.0, 2.0, 0), 2, STEEL, extend=0.3)
        m.box(lg, sx * 4.0 - 2.0, 0.0, -3.0, sx * 4.0 + 2.0, 2.0, 1.6, STEEL)
    for i, c in enumerate(((-16.0, 34.0, -2.0), (16.0, 40.0, 0.0), (-14.0, 16.0, 2.0))):   # little Mamemon faces
        ball(m, bd, c, 2.4, solid(P, "face"), layers=3)
    return m
