"""Tanhyll, the Anteater Pokémon (Normal/Fighting), built from boxes after the user's idea and the concept art they
shared ("Tanhyll, Monster form").

A hunched, shaggy anteater standing on two legs: dark grey fur dappled with lighter grey clouds, a pale cream bib on
its chest, tufts of fur bristling along its back and shoulders, a small head with a long tube of a snout curving down
and a long pink tongue hanging from it, hooked at the end like a cane; heavy forearms with big curved white claws,
sturdy legs with white claws on its feet, and a big bushy tail sweeping down behind it.

Front is -z, y is up. 25 units tall; baseScale 1.0 (1.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, mix, rod, spike
from _route import pal, tone

SCALE = 1.0
HITBOX = [1.0, 1.6]
KIND = "biped"
K = 4
HEIGHT = 25
LOOK = ("a hunched, shaggy dark-grey anteater on two legs, dappled with lighter grey, a cream bib, a long curved "
        "snout with a hooked pink tongue, big curved white claws and a bushy tail")

BASE = {"fur": (62, 62, 68), "blotch": (104, 104, 112), "bib": (226, 222, 210), "claw": (236, 236, 240),
        "tongue": (232, 120, 120), "eye": (20, 20, 24), "snout": (54, 54, 60)}
SHINY = {"fur": (116, 72, 46), "blotch": (176, 132, 86), "bib": (250, 244, 230), "tongue": (200, 80, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def blotchy(bib_below=None):
    """Dark fur with soft lighter-grey cloud blotches (and a cream bib on the chest below `bib_below`)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if bib_below is not None and face == "north" and y < bib_below and abs(x) < 3.2 - 0.25 * (bib_below - y):
            return tone(p["bib"], face), None
        n = math.sin(x * 0.55 + z * 0.35) * math.cos(y * 0.5 - x * 0.2) + 0.5 * math.sin(z * 0.8 + y * 0.3)
        return tone(p["blotch"] if n > 0.55 else p["fur"], face), None
    return s


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and ((z + 5.8) / 0.5) ** 2 + ((y - 18.3) / 0.45) ** 2 < 1:
        return p["eye"], None
    return blotchy()(x, y, z, face, variant)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def build() -> Model:
    m = Model("tanhyll")
    top = m.bone("tanhyll", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 11, 0))
    m.round_box(bd, 0, 0.5, 5, 4.5, 10, 18, blotchy(bib_below=17.5), cut=2)      # belly and chest
    m.round_box(bd, 0, 1.5, 5.5, 5, 15, 22.5, blotchy(), cut=2)                   # the shaggy hump
    for i, (sx, y, z) in enumerate(((0, 22.5, 1), (0, 22, 4), (2.5, 21.5, 2.5), (-2.5, 21.5, 2.5), (4.5, 20, 0),
                                     (-4.5, 20, 0), (0, 21, 6))):                 # bristling fur tufts
        spike(m, bd, (sx, y, z), (sx * 0.25, 1, 0.6), 2.5, 3.5, blotchy(), tip=1)
    hd = m.bone("head", bd, (0, 18, -4))
    m.round_box(hd, 0, -5.5, 1.8, 1.8, 16.5, 20, headf, cut=0.6)
    chain(m, hd, [(0, 17.5, -7), (0, 15.5, -10), (0, 12.5, -12.5)], [1.6, 1.2], solid("snout"))   # long curved snout
    chain(m, hd, [(0, 12.2, -12.8), (0, 8, -13.2), (0, 4.5, -12.8), (0, 3.6, -11.6), (0, 4.4, -10.6)],
          [0.6, 0.6, 0.6, 0.6], solid("tongue"))                                    # the hooked tongue
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                           # heavy forearms, big claws
        a = m.bone(nm, bd, (sx * 5, 19, -1))
        rod(m, a, (sx * 5, 19, -1), (sx * 6.5, 14, -3.5), 3, blotchy())
        m.round_box(a, sx * 6.8, -4, 2, 2, 9.5, 14.5, blotchy(), cut=0.6)
        for dx in (-0.8, 0.8):
            chain(m, a, [(sx * 6.8 + dx, 10, -5.5), (sx * 6.8 + dx, 8.4, -7.2), (sx * 6.6 + dx, 7.6, -6.4)],
                  [1.1, 0.9], solid("claw"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3, 11, 1.5))
        m.round_box(lg, sx * 3.2, 1.5, 2.2, 2.4, 5, 11.5, blotchy(), cut=0.8)
        m.box(lg, sx * 3.2 - 1.6, 0, -0.5, sx * 3.2 + 1.6, 5.5, 3, blotchy())
        for dx in (-0.8, 0.8):
            rod(m, lg, (sx * 3.2 + dx, 0.5, -0.4), (sx * 3.2 + dx, 0.2, -2), 0.8, solid("claw"))
    tail = m.bone("tail", bd, (0, 12, 5.5))                                       # the big bushy tail
    chain(m, tail, [(0, 12.5, 5.5), (0, 10, 10), (-1, 6.5, 14), (-2, 3.5, 17)], [4.5, 4, 3], blotchy())
    for (x, y, z) in ((0, 13.5, 8), (-0.5, 11, 12), (-1.5, 8, 15.5)):
        spike(m, tail, (x, y, z), (0, 0.8, 1), 2.5, 3, blotchy(), tip=1)
        spike(m, tail, (x, y - 2.5, z), (0, -0.6, 1), 2.5, 3, blotchy(), tip=1)
    return m
