"""Cannonbeemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the hornet battleship. A flying fortress of gold honeycomb hexagon pods filled with glowing blue
cells, black-and-yellow striped wing blades, twin black cannons, a long striped launch deck underneath, and a small
hornet head with big eyes and mandibles at its prow. 25 blocks long.

make(carrier=True): Cannonbeemon (Aircraft Carrier), the white-grey carrier version of the manga art, with a longer
flight deck. Front is -z, y is up. 30 units tall, 60 long; Perfect stage (floats).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, eye, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25 * 30 / 60, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = ("a flying hornet fortress of gold honeycomb pods with glowing blue cells, striped wing blades, twin cannons, a "
        "striped launch deck and a small hornet head at the prow")
GOLD = {"gold": (246, 196, 40), "gold_dark": (170, 120, 10), "gold_light": (255, 240, 150), "cell": (110, 190, 250),
        "cell_light": (220, 245, 255), "stripe": (30, 30, 36), "steel": (180, 184, 196), "steel_dark": (80, 84, 96),
        "eye": (230, 80, 30), "pupil": (40, 10, 0), "white": (255, 255, 255), "teal": (60, 200, 190)}
WHITE = {"gold": (236, 236, 240), "gold_dark": (150, 152, 164), "gold_light": (255, 255, 255), "cell": (200, 204, 214),
         "cell_light": (250, 250, 255), "stripe": (40, 40, 46), "steel": (200, 204, 214), "steel_dark": (110, 114, 126),
         "eye": (90, 90, 100), "pupil": (20, 20, 24), "white": (255, 255, 255), "teal": (160, 164, 176)}
SHINY_GOLD = {"gold": (200, 60, 50), "gold_dark": (120, 20, 20), "gold_light": (250, 150, 130), "cell": (120, 250, 150),
              "cell_light": (220, 255, 230)}


def make(name, carrier=False):
    base = WHITE if carrier else GOLD
    shiny = dict(base, **({"stripe": (200, 50, 50)} if carrier else SHINY_GOLD))

    def P(v):
        return pal(base, shiny, v)

    HULL = armour(P, "gold", "gold_dark", light="gold_light", trim="stripe", trim_w=0.3)
    CELL = gem(P, "cell", "cell_light", glow=not carrier)
    STEEL = metal(P, "steel", dark="steel_dark")

    def stripedf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if (z + x * 0.3) % 4.0 < 1.6:
            return tone(p["stripe"], face), None
        return HULL(x, y, z, face, variant, box=box, **k)

    def hexpod(m, bone, c, r):
        """A honeycomb pod: a hexagonal gold rim round a glowing blue cell."""
        for i in range(6):
            ang = math.radians(i * 60)
            px, py = c[0] + r * math.cos(ang), c[1] + r * math.sin(ang)
            m.box(bone, px - 0.6, py - r * 0.6, c[2] - 2.0, px + 0.6, py + r * 0.6, c[2] + 2.0, HULL,
                  rotation=(0, 0, i * 60), pivot=(px, py, c[2]))
        m.box(bone, c[0] - r * 0.75, c[1] - r * 0.75, c[2] - 1.2, c[0] + r * 0.75, c[1] + r * 0.75, c[2] + 1.2, CELL)

    def headf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                c = eye(p, x - sx * 1.4, y - 9.6, 1.0, "eye")
                if c is not None:
                    return c, None
        return HULL(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 16, 0))
        # the honeycomb fortress: rows of hex pods on a hull block
        m.box(bd, -10.0, 12.0, -10.0, 10.0, 18.0, 20.0, HULL)
        for row, (y, n) in enumerate(((20.0, 4), (26.0, 3), (31.0, 2))):
            for j in range(n):
                x = (j - (n - 1) / 2) * 7.6
                hexpod(m, bd, (x, y, 4.0 + row * 2.0), 3.6)
        for j in range(3):
            hexpod(m, bd, (0, 22.0 - j * 1.0, 10.0 + j * 5.0), 3.2) if carrier else None
        # striped wing blades sweeping back from the sides
        for sx in (-1, 1):
            for j, (yy, ln) in enumerate(((22.0, 18.0), (17.0, 22.0))):
                x0, x1 = sorted((sx * 9.0, sx * (9.0 + ln)))
                m.box(bd, x0, yy - 0.8, -2.0, x1, yy + 0.8, 3.0, stripedf, rotation=(0, sx * 20, sx * (12 - j * 18)),
                      pivot=(sx * 9.0, yy, 0))
            rod(m, bd, (sx * 6.0, 14.0, -8.0), (sx * 6.0, 13.0, -26.0), 2, solid(P, "stripe"), extend=0)   # cannons
        # the long striped launch deck under the hull
        deck = 46.0 if carrier else 36.0
        m.box(bd, -5.0, 6.0, -12.0, 5.0, 8.0, -12.0 + deck, stripedf, rotation=(4, -8, 0), pivot=(0, 7.0, 0))
        m.box(bd, -5.4, 5.4, -12.0, -4.4, 8.6, -12.0 + deck, solid(P, "teal"), rotation=(4, -8, 0), pivot=(0, 7.0, 0))
        # the hornet head at the prow, mandibles and antennae
        hd = m.bone("head", bd, (0, 10, -12))
        m.round_box(hd, 0, -14.0, 3.0, 2.6, 7.0, 12.4, headf, cut=1)
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.2, 7.4, -16.4), (sx * 0.4, -0.3, -1), 0.8, 2.2, solid(P, "stripe"))
            rod(m, hd, (sx * 1.0, 12.0, -14.0), (sx * 3.0, 15.0, -18.0), 1, solid(P, "stripe"), extend=0)
        return m
    return build


build = make("cannonbeemon")
