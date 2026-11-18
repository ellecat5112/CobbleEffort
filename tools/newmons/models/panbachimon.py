"""Panbachimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a panda-bee: a round black-and-white panda cub with sleepy eyes, two long bee antennae tipped with
spiky balls, a yellow-and-black striped belt, tiny white bee wings, and a great green bamboo stalk slung on its back
with a little panda peeking from the top. 1 block tall.

Front is -z, y is up. 34 units tall (the bamboo); Child stage (no level on wikimon).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = "a round panda-bee cub with sleepy eyes, spiky-tipped antennae, a striped belt, tiny bee wings and a bamboo stalk on its back"
BASE = {"white": (246, 246, 244), "white_dark": (190, 190, 186), "black": (34, 32, 34), "black_dark": (12, 12, 14),
        "yellow": (250, 210, 50), "green": (120, 190, 80), "green_dark": (60, 120, 30), "wing": (240, 240, 250, 170),
        "pink": (240, 150, 170)}
SHINY = {"black": (140, 90, 50), "black_dark": (80, 50, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def beltf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["yellow"] if (x + 20.0) % 2.0 < 1.0 else p["black"], face), None


def bamboof(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["green_dark"] if (y % 5.0) < 0.6 else p["green"], face), None


def build():
    m = Model("panbachimon")
    top = m.bone("panbachimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 8.0, 0), 5.0, fur(P, "black", "black_dark"), layers=4, ry=5.0)
    m.round_box(bd, 0, 0, 5.2, 5.2, 7.0, 8.6, beltf, cut=2)
    hd = m.bone("head", bd, (0, 13, 0))
    ball(m, hd, (0, 16.0, -0.4), 4.6, fur(P, "white", "white_dark"), layers=5, ry=4.0)
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.8, -4.3, 1.2, 0.4, 15.0, 17.0, solid(P, "black"), cut=0)
        ball(m, hd, (sx * 3.6, 19.4, 0), 1.4, fur(P, "black", "black_dark"), layers=2)
        pts = [(sx * 1.4, 20.0, 0), (sx * 3.0, 24.0, -0.4), (sx * 5.0, 26.0, -0.8)]
        for p0, p1 in zip(pts, pts[1:]):                                                 # bee antennae
            rod(m, hd, p0, p1, 1, solid(P, "black"), extend=0.1)
        ball(m, hd, pts[-1], 0.9, solid(P, "black"), layers=1)
        x0, x1 = sorted((sx * 3.0, sx * 7.0))                                            # tiny wings
        m.box(bd, x0, 10.0, 3.0, x1, 14.0, 3.0, solid(P, "wing"), rotation=(0, 0, sx * 25), pivot=(sx * 3.0, 12.0, 3.0))
    m.box(hd, -0.5, 14.6, -4.6, 0.5, 15.0, -4.45, solid(P, "black"))
    rod(m, bd, (-4.0, 4.0, 5.0), (3.0, 32.0, 5.0), 4, bamboof, extend=0.6)                # bamboo stalk
    ball(m, bd, (3.2, 32.0, 5.0), 1.4, fur(P, "white", "white_dark"), layers=2)
    return m
