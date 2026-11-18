"""Shared builder for Kekomon and Kekkomon (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
a round green spiky slime with a yellow belly lip, big round eyes, a happy open mouth with a pink tongue, a tall
pink-tipped spike on top and spiky green frills round its sides. Kekkomon (Baby II) adds a crescent-moon mark on its
brow, more spikes and a red tuft. Shiny: sky blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

BASE = {"green": (120, 230, 60), "green_dark": (60, 160, 20), "green_light": (200, 255, 150), "yellow": (240, 230, 90),
        "pink": (240, 120, 150), "eye": (60, 50, 70), "white": (250, 250, 250), "red": (220, 50, 70)}
SHINY = {"green": (110, 190, 250), "green_dark": (40, 120, 200), "green_light": (200, 240, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, crest=False):
    def bodyf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                d = math.hypot(x - sx * 2.0, y - 5.8)
                if d < 0.5:
                    return tone(p["eye"], face), None
                if d < 1.2:
                    return tone(p["white"], face), None
            if 2.4 < y < 3.8 and abs(x) < 1.6 - (3.8 - y) * 0.6:
                return tone(p["pink"], face), None
            if crest and abs(math.hypot(x, y - 8.6) - 0.7) < 0.2 and y > 8.6:
                return tone(p["yellow"], face), None
        if y < 2.4:
            return tone(p["yellow"], face), None
        return skin(P, "green", dark="green_dark", light="green_light")(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 4, 0))
        ball(m, bd, (0, 5.0, 0), 5.0, bodyf, layers=4, squash=0.85)
        hd = m.bone("head", bd, (0, 9, 0))
        spike(m, hd, (0.6, 8.6, 0.6), (0.2, 1, -0.1), 2.6, 6.0 if crest else 5.0, skin(P, "green", dark="green_dark"),
              tip=0.8)
        spike(m, hd, (0.8, 13.4 if crest else 12.4, 0.5), (0.2, 1, -0.1), 1.0, 1.2, solid(P, "pink"), tip=0.8)
        n = 6 if crest else 4
        for i in range(n):                                                         # spiky frills
            ang = math.radians(-60 + i * 120 / max(1, n - 1))
            for sx in (-1, 1):
                spike(m, bd, (sx * 4.4 * math.cos(ang), 5.0 + 3.0 * math.sin(ang), 1.0), (sx * math.cos(ang), math.sin(ang), 0.3),
                      1.4, 2.4, skin(P, "green", dark="green_dark"), tip=0.8)
        if crest:
            for j in range(4):                                                     # red tuft
                spike(m, hd, (-1.6 + j * 0.5, 8.4, 2.0), (-0.5 + j * 0.3, 1, 0.6), 0.9, 3.0, solid(P, "red"), tip=0.8)
        return m

    return build
