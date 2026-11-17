"""Bushi Agumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the samurai Agumon. An Agumon with a cool half-lidded look, a black topknot crest of spiky
hair, a dark kimono and haori with a white crest on the chest, a violet sash, grey hakama trousers ragged at the
hem, and a curved katana. Child stage.

Front is -z, y is up. 25 units tall.
"""
from __future__ import annotations

import math

from _agumon import build_agumon
from _boxmodel import rod, spike
from _digi import sized
from _digidetail import cutout, fabric, local, metal, noise2, solid
from _route import pal, tone

HEIGHT = 25
SCALE, HITBOX = sized(1.0, HEIGHT, 1.3)
KIND = "biped"
K = 5
LOOK = ("an Agumon samurai with a black topknot crest, a dark kimono and haori with a white crest, a violet sash, "
        "ragged grey hakama and a curved katana")
BASE = {"kimono": (40, 40, 56), "kimono_dark": (16, 16, 24), "white": (240, 240, 246), "violet": (110, 70, 170),
        "violet_dark": (60, 30, 110), "hakama": (170, 172, 184), "hakama_dark": (110, 112, 126), "hair": (30, 24, 28),
        "hair_tip": (160, 40, 40), "steel": (210, 214, 226), "steel_dark": (110, 114, 128), "hilt": (60, 40, 30)}
SHINY = {"kimono": (140, 30, 40), "kimono_dark": (70, 10, 16), "violet": (220, 180, 50), "violet_dark": (150, 110, 10),
         "hakama": (60, 60, 74), "hakama_dark": (26, 26, 34)}


def P(v):
    return pal(BASE, SHINY, v)


KIMONO = fabric(P, "kimono", "kimono_dark", axis="y", period=1.6)
HAKAMA = fabric(P, "hakama", "hakama_dark", axis="x", period=1.2)
STEEL = metal(P, "steel", dark="steel_dark")


def kimonof(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x - 1.6, y - 14.6) < 0.9:                  # the white crest
        return tone(p["white"], face), None
    if face == "north" and abs(abs(x) - (16.8 - y) * 0.35) < 0.25 and y > 12:    # collar lines
        return tone(p["white"], face), None
    return KIMONO(x, y, z, face, variant, box=box, **k)


def ragged(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.3 * noise2((box.lo[0] + u + box.lo[2]) * 1.6, 5.0)


def build():
    m = build_agumon("bushiagumon")
    bd, hd = "body", "head"
    m.box(bd, -3.7, 9.6, -3.0, 3.7, 17.0, 4.0, kimonof)                                # kimono
    m.box(bd, -3.8, 10.0, -3.2, 3.8, 11.4, 4.2, fabric(P, "violet", "violet_dark", axis="x", period=0.8))  # sash
    for sx in (-1, 1):                                                                # haori sleeves
        m.box(bd, min(sx * 3.4, sx * 5.4), 11.0, -2.4, max(sx * 3.4, sx * 5.4), 16.4, 2.4, KIMONO,
              rotation=(0, 0, sx * 12), pivot=(sx * 3.4, 16.4, 0))
    for nm in ("leg_left", "leg_right"):                                              # ragged hakama
        sx = 1 if nm == "leg_left" else -1
        m.box(nm, sx * 2.6 - 2.6, 2.6, -2.2, sx * 2.6 + 2.6, 9.6, 3.2, HAKAMA)
        for ang in (0, 90, 180, 270):
            m.box(nm, sx * 2.6 - 2.8, 0.8, -2.4, sx * 2.6 + 2.8, 3.4, -2.4, cutout(ragged, HAKAMA),
                  rotation=(0, ang, 0), pivot=(sx * 2.6, 2.0, 0.4))
    for i in range(7):                                                                # topknot crest
        spike(m, hd, (0, 21.8, -3.0 + i * 0.9), (0, 1, 0.5 + 0.12 * i), 1.4, 3.6 - abs(i - 3) * 0.4,
              solid(P, "hair" if i % 2 else "hair_tip"), tip=0.4)
    kb = m.bone("sword", "arm_right", (-4.0, 11.0, -4.4))                            # the katana
    rod(m, kb, (-4.0, 12.4, -4.4), (-4.0, 9.4, -4.6), 0.8, solid(P, "hilt"), extend=0.1)
    m.box(kb, -5.0, 9.2, -5.4, -3.0, 9.6, -3.6, solid(P, "violet"))
    pts = [(-4.0, 9.4, -4.6), (-4.6, 4.0, -6.0), (-5.6, -0.6, -6.6), (-7.0, -4.0, -6.4)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, kb, p0, p1, 0.6, STEEL, extend=0.2, t2=1.2)
    return m
