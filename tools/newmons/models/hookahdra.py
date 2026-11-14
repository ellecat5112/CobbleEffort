"""Hookahdra, the Hookah Hydra Pokémon (Water/Poison), Bongwater evolved, the Nicodex's Water type (the user's design):
a multi-headed glass-and-brass sea serpent. Its body is a great bulbous glass vase of bubbling water with a brass
collar, a tall ornate brass stem and a crowning bowl of glowing coals; three braided teal hoses coil out of it as
necks, each ending in a serpent head with a brass mouthpiece snout and glowing eyes, puffing sweet mist.

Shiny: violet glass, silver fittings and rose hoses.

Front is -z, y is up. 40 units tall; baseScale 0.92 (2.3 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _nico import palette, puff, translucent
from _route import along, tone

SHINY = {"glass": (222, 196, 246, 110), "water": (170, 110, 220, 150), "brass": (206, 208, 220),
         "gold_dark": (150, 150, 168), "teal": (200, 100, 140), "teal_dark": (150, 60, 100)}
P, solid, ramp = palette(SHINY)
SCALE = 0.92
HITBOX = [2.0, 2.5]
KIND = "quadruped"
K = 3
HEIGHT = 40
LOOK = ("a glass-and-brass hookah sea serpent: a bubbling glass vase body, a brass stem and coal bowl, and three braided "
        "teal hose necks ending in serpent heads with brass mouthpiece snouts")


def hosef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = along(z, box) * box.size[2]
    return tone(p["teal_dark"] if (t % 1.6) < 0.5 else p["teal"], face), None   # braided bands


def headf(sx):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("east", "west", "north") and abs(y - k["box"].lo[1] - 2.4) < 0.5 and abs(z - k["box"].lo[2] - 1.0) < 0.6:
            return p["amber"], p["amber"]                                     # glowing eyes
        return tone(p["teal"], face), None
    return s


def coalf(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["ember_hot"] if (int(x * 2) + int(z * 2)) % 3 == 0 else p["ember"]
    return c, c


def serpent(m, bone, base, mid, tip, sx):
    rod(m, bone, base, mid, 2.6, hosef, extend=0.6)
    rod(m, bone, mid, tip, 2.4, hosef, extend=0.6)
    hx, hy, hz = tip
    m.box(bone, hx - 1.8, hy - 1.4, hz - 2.6, hx + 1.8, hy + 2.0, hz + 1.4, headf(sx))      # serpent head
    rod(m, bone, (hx, hy + 0.2, hz - 2.4), (hx, hy - 0.2, hz - 5.6), 1.4, solid("brass"), extend=0.2)   # mouthpiece
    puff(m, bone, (hx + 0.4, hy + 0.6, hz - 7.0), 1.1, translucent(P, "mist"))
    for d in ((-0.4, 1, 0.5), (0.4, 1, 0.5)):
        spike(m, bone, (hx + d[0] * 2, hy + 1.8, hz + 0.6), d, 1.0, 1.8, solid("brass"))     # brass horns


def build() -> Model:
    m = Model("hookahdra")
    top = m.bone("hookahdra", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    for y0, r in ((0.0, 5.0), (2.0, 6.6), (4.0, 7.2), (6.0, 7.0), (8.0, 6.0), (10.0, 4.2)):   # the glass vase
        m.round_box(bd, 0, 0, r, r, y0, y0 + 2.0, translucent(P, "glass"), cut=max(1, round(r * 0.35)))
    for y0, r in ((0.6, 4.2), (2.4, 5.8), (4.2, 6.2), (6.0, 5.6)):
        m.round_box(bd, 0, 0, r, r, y0, y0 + 1.8, translucent(P, "water"), cut=max(1, round(r * 0.35)))
    for c in ((1.6, 5.0, 1.0), (-2.2, 7.0, -1.0), (0.4, 8.6, 2.0)):
        puff(m, bd, c, 0.7, translucent(P, "mist"))                              # bubbles rising
    m.round_box(bd, 0, 0, 3.4, 3.4, 12.0, 13.6, solid("brass"), cut=1.0)         # brass collar
    rod(m, bd, (0, 13.4, 0), (0, 27.0, 0), 2.6, solid("brass"), extend=0.4)      # the ornate stem
    for y in (17.0, 21.0, 24.0):
        m.round_box(bd, 0, 0, 2.2, 2.2, y, y + 0.9, solid("gold_dark"), cut=0.6)
    m.round_box(bd, 0, 0, 3.6, 3.6, 27.0, 29.0, solid("brass"), cut=1.0)         # the bowl
    m.round_box(bd, 0, 0, 2.8, 2.8, 28.8, 30.0, coalf, cut=0.8)                  # glowing coals
    m.box(bd, -3.4, 13.0, -1.0, 3.4, 14.4, 1.0, solid("brass"))                  # hose ports
    hd = m.bone("head", bd, (0, 14, -3))                                         # the front head
    serpent(m, hd, (0, 13.8, -3.0), (0, 20.0, -9.0), (0, 30.0, -10.0), 0)
    for sx, side in ((-1, "left"), (1, "right")):
        nk = m.bone(f"neck_{side}", bd, (sx * 3.4, 14, 0))
        serpent(m, nk, (sx * 3.4, 13.8, 0.0), (sx * 10.0, 18.0, -2.0), (sx * 12.0, 27.0, -5.0), sx)
    return m
