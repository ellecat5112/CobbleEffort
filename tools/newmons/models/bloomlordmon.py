"""Bloom Lordmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the flower knight. A slender knight in white-and-teal plate edged in gold, a helm crowned by a
huge crimson-pink lily with a golden heart, a long cape of violet petals, pointed teal sabatons, a curling green vine
whip in its left hand and a long glowing crimson lance in its right. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, cutout, local, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a slender flower knight in white-and-teal plate edged in gold, crowned by a huge crimson lily, with a cape "
        "of violet petals, a green vine whip and a long glowing crimson lance")
BASE = {"white": (240, 244, 250), "white_dark": (170, 180, 200), "teal": (40, 180, 200), "teal_dark": (10, 100, 120),
        "gold": (240, 200, 60), "gold_dark": (170, 120, 20), "lily": (226, 40, 110), "lily_light": (255, 160, 200),
        "lily_dark": (140, 10, 60), "violet": (150, 90, 210), "violet_light": (220, 190, 250),
        "violet_dark": (70, 30, 120), "lance": (220, 30, 60), "lance_light": (255, 180, 190), "vine": (90, 180, 60),
        "vine_dark": (40, 100, 30), "under": (40, 40, 60), "visor": (30, 160, 200)}
SHINY = {"lily": (250, 220, 70), "lily_light": (255, 250, 200), "lily_dark": (180, 130, 10), "violet": (60, 170, 120),
         "violet_light": (180, 240, 210), "violet_dark": (20, 90, 60), "lance": (60, 120, 240)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", trim="gold", trim_w=0.4)
TEAL = armour(P, "teal", "teal_dark", trim="gold", trim_w=0.4)
GOLD = metal(P, "gold", dark="gold_dark")
UNDER = solid(P, "under")


def petal(key, light, dark):
    """A pointed petal with a pale midrib, darker toward its root."""
    def inside(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        du, t = abs(u / max(W, 1e-6) - 0.5) * 2, v / max(H, 1e-6)
        return du < math.sin(math.pi * min(1.0, t * 1.1)) ** 0.7

    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        du, t = abs(u / max(W, 1e-6) - 0.5) * 2, v / max(H, 1e-6)
        col = p[light] if du < 0.08 else p[dark] if t < 0.2 else p[key]
        return tone(col, face), None
    return cutout(inside, s)


LILY = petal("lily", "lily_light", "lily_dark")
PETAL = petal("violet", "violet_light", "violet_dark")


def capef(x, y, z, face, variant, box=None, **k):
    """The petal cape: violet, paling toward the shoulders and darkening to the hem, with pale petal veins."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = v / max(H, 1e-6)
    if abs(((x * 0.5) % 1) - 0.5) < 0.05:
        return tone(p["violet_light"], face), None
    col = p["violet_dark"] if t < 0.18 else p["violet"] if t < 0.8 else p["violet_light"]
    return tone(col, face), None


def lancef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["lance_light"] if abs(u / max(W, 1e-6) - 0.5) < 0.15 else p["lance"]
    return c, c[:3]


def build():
    m = Model("bloomlordmon")
    mats = {"skin": UNDER, "chest": WHITE, "abs": TEAL, "pelvis": WHITE, "neck": UNDER, "deltoid": WHITE,
            "upper_arm": UNDER, "forearm": WHITE, "hand": TEAL, "finger": TEAL, "thigh": UNDER, "knee": GOLD,
            "shin": WHITE, "calf": WHITE, "foot": TEAL, "toe": TEAL}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=0.95, name="bloomlordmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0.0, 2.6, 2.8, 54.4, 61.0, WHITE, cut=1)
    m.box(hd, -2.0, 56.8, -3.0, 2.0, 57.8, -2.6, solid(P, "visor", glow=True))
    for sx in (-1, 1):                                                                     # winged helm fins
        spike(m, hd, (sx * 2.6, 58.6, 0.6), (sx, 0.6, 0.6), 1.6, 4.0, TEAL)
    # the great lily crown: two rings of petals round a golden heart
    cr = m.bone("crown", hd, (0, 61, 1))
    m.box(cr, -1.2, 61.0, -0.2, 1.2, 64.0, 2.2, GOLD)
    for ring, (n, L, tilt) in enumerate(((6, 13.0, 30), (5, 10.0, 55))):
        for i in range(n):
            ang = i * 360 / n + ring * 30
            m.box(cr, -3.0, 61.0, 1.0, 3.0, 61.0 + L, 1.0, LILY,
                  rotation=(tilt * math.cos(math.radians(ang)) - 10, 0, tilt * math.sin(math.radians(ang))),
                  pivot=(0, 61.0, 1.0))
    for sx in (-1, 1):                                                                     # gold pauldron edges
        m.box(bd, min(sx * 5.0, sx * 9.6), 51.0, -2.8, max(sx * 5.0, sx * 9.6), 52.2, 3.0, GOLD,
              rotation=(0, 0, -sx * 12), pivot=(sx * 5.0, 51.6, 0))
    # the cape of violet petals hanging from the shoulders
    cb = m.bone("cap", bd, (0, 52, 3))
    cape(m, cb, 52.0, 22.0, 48.0, capef, z=4.4, flare=1.1, panels=9, sweep=(0, 5), seed=3)
    # the crimson lance in its right hand
    ar = a["arm_right"]
    h = ar["hand"]
    lb = m.bone("lance", ar["bone"], h)
    m.box(lb, h[0] - 1.6, h[1] - 0.4, h[2] - 1.6, h[0] + 1.6, h[1] + 0.6, h[2] + 1.6, GOLD)       # guard
    rod(m, lb, (h[0], h[1] + 4.0, h[2] + 2.0), (h[0], h[1] - 2.0, h[2] - 1.0), 1, GOLD, extend=0)
    rod(m, lb, (h[0], h[1] - 0.6, h[2]), (h[0] + 2.0, h[1] - 30.0, h[2] - 10.0), 3, lancef, extend=0, t2=1)
    spike(m, lb, (h[0] + 2.0, h[1] - 30.0, h[2] - 10.0), (0.07, -1, -0.33), 1.4, 5.0, lancef)
    # the vine whip curling from its left hand
    al = a["arm_left"]
    h = al["hand"]
    pts = [h]
    for i in range(1, 9):
        th = i * 0.6
        pts.append((h[0] + 2.0 * i * 0.6 + 2.0 * math.sin(th), h[1] - 2.4 * i + 3.0 * math.cos(th),
                    h[2] - 1.4 * i))
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, al["bone"], p0, p1, 1, solid(P, "vine"), extend=0.4)
    for i in (2, 4, 6):
        spike(m, al["bone"], pts[i], (1, 0.4, 0), 0.8, 1.4, solid(P, "vine_dark"))
    return m
