"""Valdurmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the holy bird of light: a slender pale-blue phoenix with a golden-crested head and a red-lined beak,
golden talons, layers of translucent feathered wings spread all round it, and a great halo of rainbow light blazing
behind. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import eye, feathers, metal, solid
from _route import pal, tone

HEIGHT = 54
SCALE, HITBOX = sized(35, HEIGHT, 10.0)
KIND = "floater"
K = 3
LOOK = "a slender pale-blue phoenix of light with a golden crest, layers of translucent feather wings and a blazing rainbow halo"
BASE = {"blue": (150, 190, 220), "blue_dark": (70, 110, 160), "gold": (250, 210, 80), "gold_dark": (190, 140, 30),
        "red": (220, 60, 50), "wing": (255, 236, 200, 160), "wing_dark": (240, 190, 140, 160), "eye": (250, 80, 50),
        "pupil": (30, 10, 10), "white": (255, 255, 255)}
SHINY = {"blue": (230, 170, 220), "blue_dark": (170, 100, 160)}
HALO = [(255, 90, 90), (255, 170, 70), (255, 240, 90), (110, 230, 110), (90, 170, 255), (180, 110, 255)]


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 9.6, y - 36.6, 0.8, "eye", slit=True)
        if c is not None:
            return c, None
    return feathers(P, "blue", "blue_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("valdurmon")
    top = m.bone("valdurmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    ball(m, bd, (0, 28.0, 0), 4.4, feathers(P, "blue", "blue_dark"), layers=4, ry=6.0)
    nk = m.bone("neck", bd, (0, 32, -2))
    rod(m, nk, (0, 32.0, -2.0), (0, 36.0, -6.0), 2, feathers(P, "blue", "blue_dark"), extend=0.6)
    hd = m.bone("head", nk, (0, 36, -7))
    ball(m, hd, (0, 36.6, -8.0), 2.4, headf, layers=3)
    spike(m, hd, (0, 36.0, -10.0), (0, -0.2, -1), 1.6, 4.0, metal(P, "gold"), tip=0.8)
    for j in range(5):
        spike(m, hd, ((j - 2) * 0.6, 38.6, -7.0), ((j - 2) * 0.3, 1, 0.8), 0.9, 5.0, metal(P, "gold"), tip=0.8)
    for sx in (-1, 1):
        for layer, (dy, span, sweep) in enumerate(((4.0, 30.0, 10), (0.0, 26.0, 35), (-4.0, 22.0, 60))):
            wb = m.bone("wing_%s_%d" % ("left" if sx > 0 else "right", layer), bd, (sx * 3.0, 30.0 + dy, 1.0))
            feather_wing(m, wb, (sx * 3.0, 30.0 + dy, 1.0), span, 10.0, 2, solid(P, "wing", glow=True), side=sx,
                         sweep=sweep, droop=-dy)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 1.6, 24.0, 0))
        rod(m, lg, (sx * 1.6, 24.0, 0), (sx * 2.0, 18.0, -1.0), 1, metal(P, "gold"), extend=0.3)
        for t in range(3):
            spike(m, lg, (sx * 2.0, 18.0, -1.0), ((t - 1) * 0.5, -0.6, -1), 0.8, 2.4, metal(P, "gold"), tip=0.8)
    for j in range(5):                                                                 # tail plumes
        spike(m, bd, ((j - 2) * 1.0, 25.0, 4.0), ((j - 2) * 0.3, -1, 0.6), 1.0, 14.0, solid(P, "wing", glow=True),
              tip=0.8)
    hb = m.bone("halo", bd, (0, 30, 6))                                                # rainbow halo
    for ring in range(len(HALO)):
        r = 16.0 + ring * 1.4
        for i in range(24):
            ang = i * 2 * math.pi / 24
            cx, cy = r * math.cos(ang), 30.0 + r * math.sin(ang)
            if cy < 1.0:
                continue
            m.box(hb, cx - 1.0, cy - 1.0, 7.0, cx + 1.0, cy + 1.0, 7.6, _halo(ring))
    return m


def _halo(ring):
    col = HALO[ring] + (190,)

    def f(x, y, z, face, variant, box=None, **k):
        return col, col[:3]
    return f
