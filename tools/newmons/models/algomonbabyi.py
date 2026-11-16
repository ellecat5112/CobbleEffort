"""Algomon (Baby I) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): a glossy lime-green droplet that floats on its own. Violet lines run up its body to a thin stalk
carrying a magenta bulb, a violet band rings its middle, and one great yellow eye with a magenta iris stares out of
its front; a pink drip hangs from its tip. Tiny.

Front is -z, y is up. 22 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _algo import BASE, GREEN, P, SHINY, VIOLET, ringed_eye
from _digidetail import plane, solid
from _route import tone

HEIGHT = 22
SCALE, HITBOX = sized(0.35, HEIGHT, 0.3)
KIND = "floater"
K = 4
LOOK = "a glossy lime-green droplet with violet lines, a stalk with a magenta bulb and one big yellow ringed eye"
EYE = ringed_eye(0, 8.0, 3.4)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = EYE(x, y, z, face, p)
    if c is not None:
        return tone(c, face), None
    a, b = plane(x, y, z, face)
    if abs(b - 8.0) < 0.5 and face in ("east", "west", "south"):
        return tone(p["violet"], face), None                    # the band round its middle
    if b > 11.5 and min(abs(a), abs(abs(a) - 2.4)) < 0.35:
        return tone(p["violet"], face), None                    # lines running up to the stalk
    return GREEN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("algomonbabyi")
    top = m.bone("algomonbabyi", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 8.0, 0), 6.2, bodyf, layers=6)
    for i in range(5):                                          # the droplet's tapering upper half
        r = 4.6 * (1 - i / 5) + 0.6
        m.round_box(bd, 0, 0, r, r, 12.6 + i * 1.4, 14.2 + i * 1.4, bodyf, cut=max(1, round(r * 0.35)))
    for sx in (-1, 1):                                          # violet rim plates beside the eye
        m.box(bd, sx * 5.4 - 0.6, 6.6, -4.6, sx * 5.4 + 0.6, 9.4, -3.0, VIOLET)
    st = m.bone("cap", bd, (0, 19, 0))
    rod(m, st, (0, 19.0, 0), (0, 22.0, 0.4), 1, VIOLET, extend=0.2)
    ball(m, st, (0, 23.0, 0.5), 1.6, solid(P, "pink"), layers=3)
    m.box(bd, -0.6, 0.0, -0.6, 0.6, 2.2, 0.6, solid(P, "pink"))  # the drip
    return m
