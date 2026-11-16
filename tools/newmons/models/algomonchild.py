"""Algomon (Child) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): a glossy violet ball of a head with one huge ringed eye (green rim, yellow almond, red iris) and three
horns tipped yellow and red, floating on a bundle of curling lime-green tentacles. 1 block tall.

Front is -z, y is up. 34 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _algo import GREEN, P, VIOLET, hornf, ringed_eye, tentaclef
from _route import tone

HEIGHT = 34
SCALE, HITBOX = sized(1.0, HEIGHT, 0.7)
KIND = "floater"
K = 4
LOOK = ("a glossy violet ball head with one huge green-rimmed yellow eye and red iris, three yellow-and-red tipped "
        "horns, floating on curling lime-green tentacles")
EYE = ringed_eye(0, 22.0, 5.0, ring="green", iris="eye_r")
TENT = tentaclef()


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = EYE(x, y, z, face, p)
    if c is not None:
        return tone(c, face), None
    return VIOLET(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("algomonchild")
    top = m.bone("algomonchild", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    hd = m.bone("head", bd, (0, 22, 0))
    ball(m, hd, (0, 22.0, 0), 7.6, headf, layers=7)
    for ang in (-28, 0, 28):                                     # three horns
        r = math.radians(ang)
        base = (5.6 * math.sin(r), 28.0, 1.0)
        rod(m, hd, base, (base[0] + 3.0 * math.sin(r), 34.0, 2.0), 3, hornf, extend=0.3)
    sk = m.bone("skirt", bd, (0, 15, 0))
    for i in range(9):                                           # tentacles curling down and back
        ang = math.radians(i * 40)
        r0 = 3.0
        pts = [(r0 * math.sin(ang), 16.0, r0 * math.cos(ang)),
               (4.6 * math.sin(ang), 10.0, 4.6 * math.cos(ang) + 1),
               (6.0 * math.sin(ang + 0.4), 5.0, 6.0 * math.cos(ang + 0.4) + 2),
               (7.6 * math.sin(ang + 0.9), 2.0, 7.6 * math.cos(ang + 0.9) + 2)]
        for j, (a, b) in enumerate(zip(pts, pts[1:])):
            rod(m, sk, a, b, 3 - j, TENT, extend=0.4)
    m.round_box(bd, 0, 0, 3.4, 3.4, 13.0, 16.5, GREEN, cut=1)
    return m
