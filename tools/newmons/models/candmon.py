"""Candmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a living candle. A stout white wax candle with wax dripping down its sides and wing-like wax arms, a red-
eyed grinning face in the wax, a flame for a head with its own cheeky face, a golden candlestick-bell base, and a
little fireball at its side. Child stage.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import cutout, flame_inside, local, metal, mix, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.0)
KIND = "floater"
K = 4
LOOK = ("a stout white wax candle with dripping sides, wax wings, a red-eyed grin, a flame head with its own face and "
        "a golden candlestick-bell base")
BASE = {"wax": (236, 244, 250), "wax_dark": (176, 196, 214), "eye": (220, 30, 40), "pupil": (40, 10, 10),
        "mouth": (60, 20, 30), "tooth": (255, 255, 255), "gold": (226, 176, 60), "gold_dark": (150, 100, 20),
        "flame": (255, 150, 30, 230), "flame_core": (255, 230, 120, 240), "face": (60, 120, 230), "white": (255, 255, 255)}
SHINY = {"wax": (250, 200, 220), "wax_dark": (210, 140, 170), "flame": (120, 200, 255, 230),
         "flame_core": (220, 245, 255, 240), "face": (230, 90, 40)}


def P(v):
    return pal(BASE, SHINY, v)


WAX = skin(P, "wax", dark="wax_dark", var=0.03)
GOLD = metal(P, "gold", dark="gold_dark")


def waxf(x, y, z, face, variant, box=None, **k):
    """Wax with drips running down from the top edge; the face on the front."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.2, y - 17.4)
            if d < 1.2:
                return tone(p["pupil"] if d < 0.45 else p["eye"], face), None
        if 13.0 < y < 15.2 and abs(x) < 2.6 - (15.2 - y) * 0.5:
            return tone(p["tooth"] if (x * 1.6) % 1.2 < 0.4 and y > 14.4 else p["mouth"], face), None
    drip = 20.6 - 2.4 * abs(math.sin(x * 1.3 + z * 0.9))
    if y < drip and face != "up":
        return WAX(x, y, z, face, variant, box=box, **k)
    return tone(mix(p["wax"], p["wax_dark"], 0.15), face), None


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6)
    if face in ("north", "south") and 0.25 < b < 0.4 and abs(abs(a) - 0.15) < 0.06:
        return p["face"][:3] + (255,), None                                    # the flame's eyes
    if face in ("north", "south") and 0.15 < b < 0.2 and abs(a) < 0.14:
        return p["face"][:3] + (255,), None                                    # its grin
    c = p["flame_core"] if b < 0.3 else p["flame"]
    return c, c[:3]


def build():
    m = Model("candmon")
    top = m.bone("candmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for r, y0, y1 in ((3.4, 0.0, 1.6), (2.0, 1.6, 4.0), (3.0, 4.0, 5.4), (4.6, 5.4, 7.0)):   # candlestick base
        m.round_box(bd, 0, 0, r, r, y0, y1, GOLD, cut=1)
    m.round_box(bd, 0, 0, 5.4, 4.8, 7.0, 21.0, waxf, cut=2)                                   # the candle
    for sx in (-1, 1):                                                                         # wax wings
        for j in range(3):
            m.box(bd, min(sx * 5.0, sx * (11.0 - j * 1.6)), 15.0 - j * 2.0, -1.0 + j * 0.3,
                  max(sx * 5.0, sx * (11.0 - j * 1.6)), 19.0 - j * 2.0, 1.0 + j * 0.3, WAX,
                  rotation=(0, 0, -sx * (10 + j * 8)), pivot=(sx * 5.0, 18.0, 0))
    hd = m.bone("head", bd, (0, 21, 0))
    rod(m, hd, (0, 21.0, 0), (0, 22.6, 0), 1, solid(P, "mouth"), extend=0)                     # wick
    for ang in (0, 60, 120):                                                                   # the flame head
        m.box(hd, -4.0, 22.0, 0, 4.0, 31.0, 0, cutout(flame_inside(5, 0.0, ang // 60), flamef),
              rotation=(0, ang, 0), pivot=(0, 22.0, 0))
    fb = m.bone("fireball", bd, (8, 6, -2))
    for ang in (0, 90):
        m.box(fb, 6.0, 2.0, -2.0, 10.0, 8.0, -2.0, cutout(flame_inside(4, 0.2, 9), flamef),
              rotation=(0, ang, 0), pivot=(8.0, 2.0, -2.0))
    return m
