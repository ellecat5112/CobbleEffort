"""Master (a Digimon of the CobbleEffort: Digital crossover; hand-built after the game render on wikimon.net): the
mastermind of a ruined world: a huge pulsing brain of teal-green cells flecked with red, cradled over a smooth pale
violet shell-head with four black eye-holes and a red mouth etched with lines, and thin glowing cyan cables trailing
below. 35 blocks tall.

Front is -z, y is up. 30 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a huge pulsing brain of teal-green cells over a smooth pale violet shell-head with four black eye-holes and glowing cables"
BASE = {"teal": (40, 160, 160), "teal_dark": (14, 70, 80), "red": (220, 30, 40), "shell": (200, 190, 220),
        "shell_dark": (120, 110, 150), "black": (16, 14, 20), "cyan": (90, 230, 250)}
SHINY = {"teal": (180, 70, 160), "teal_dark": (90, 20, 80)}


def P(v):
    return pal(BASE, SHINY, v)


def brainf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = math.sin(x * 2.0) * math.sin(y * 2.1) * math.sin(z * 1.9)
    if c > 0.6:
        return tone(p["red"], face), p["red"]
    return tone(p["teal"] if c > -0.3 else p["teal_dark"], face), None


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for (ex, ey) in ((-2.4, 11.0), (2.4, 11.0), (-1.2, 8.6), (1.2, 8.6)):
            if math.hypot(x - ex, y - ey) < 0.9:
                return tone(p["black"], face), None
        if abs(y - 6.4) < 0.4 and abs(x) < 1.0:
            return tone(p["red"], face), None
    return metal(P, "shell", dark="shell_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("master")
    top = m.bone("master", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 20.0, 3.0), 9.0, brainf, layers=6, squash=0.85)
    hd = m.bone("head", bd, (0, 10, -4))
    ball(m, hd, (0, 10.0, -4.0), 5.0, shellf, layers=4)
    for i in range(5):                                                               # trailing cables
        ang = math.radians(-60 + i * 30)
        pts = [(4.0 * math.sin(ang), 12.0, 4.0), (7.0 * math.sin(ang), 4.0, 6.0), (6.0 * math.sin(ang), 0.6, 9.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, solid(P, "cyan", glow=True), extend=0.2, t2=1)
    return m
