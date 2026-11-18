"""Morphomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little white fluffy fairy-moth with a round body, big black eyes, a tiny smile, two long
striped antennae, short stubby legs, and four great translucent blue butterfly wings veined dark, the morpho's
shimmering blue. 1 block tall.

Front is -z, y is up. 30 units tall (the wings); Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, local, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 1.4)
KIND = "floater"
K = 3
LOOK = "a little white fluffy fairy-moth with big black eyes, long striped antennae and four great translucent blue wings"
BASE = {"white": (246, 246, 252), "white_dark": (190, 194, 214), "black": (24, 24, 30), "blue": (60, 100, 230, 190),
        "blue_light": (160, 200, 255, 160), "vein": (20, 40, 120), "pink": (240, 170, 200)}
SHINY = {"blue": (240, 120, 200, 190), "blue_light": (255, 200, 240, 160), "vein": (120, 20, 80)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "white", "white_dark", length=1.0)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs((u * 0.9) % 2.4 - 1.2) < 0.12:
        return tone(p["vein"], face), None
    return (p["blue_light"] if v / max(H, 1e-6) > 0.7 else p["blue"]), None


def build():
    m = Model("morphomon")
    top = m.bone("morphomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 9.0, 0), 4.2, FUR, layers=4, ry=5.0)
    hd = m.bone("head", bd, (0, 14, 0))
    ball(m, hd, (0, 15.6, -0.4), 3.6, FUR, layers=4, ry=3.2)
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.6, 15.6, -3.95, sx * 1.4 + 0.6, 17.0, -3.8, solid(P, "black"))
        for j in range(5):                                                               # striped antennae
            p0 = (sx * (0.8 + j * 0.9), 18.0 + j * 2.0, -0.4 + j * 0.3)
            p1 = (sx * (0.8 + (j + 1) * 0.9), 18.0 + (j + 1) * 2.0, -0.4 + (j + 1) * 0.3)
            rod(m, hd, p0, p1, 1, solid(P, "black" if j % 2 else "white"), extend=0.1)
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 1.6, 4.0, 0))
        rod(m, lg, (sx * 1.6, 5.0, 0), (sx * 1.8, 1.0, -0.4), 2, FUR, extend=0.3)
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 2.0, 11.0, 2.0))
        x0, x1 = sorted((sx * 2.0, sx * 15.0))
        m.box(wb, x0, 10.0, 2.6, x1, 24.0, 2.6, wingf, rotation=(0, sx * 15, sx * 20), pivot=(sx * 2.0, 11.0, 2.6))
        x0, x1 = sorted((sx * 2.0, sx * 11.0))
        m.box(wb, x0, 2.0, 3.0, x1, 11.0, 3.0, wingf, rotation=(0, sx * 15, -sx * 15), pivot=(sx * 2.0, 11.0, 3.0))
    m.box(hd, -0.5, 14.4, -4.0, 0.5, 14.8, -3.85, solid(P, "pink"))
    return m
