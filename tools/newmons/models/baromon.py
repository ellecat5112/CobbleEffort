"""Baromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little demon-masked shaman. A big red-and-orange ceremonial mask with bulging eyes, gold-capped
crown beads and a fanged grin, a ruff of white hair spikes, a tattered red-orange cape, a green tunic with a gold
amulet, red fists and stout brown boots. 15 blocks tall.

Front is -z, y is up. 42 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape
from _digidetail import armour, cutout, fabric, leather, local, plane, skin, solid, strands
from _route import pal, tone

HEIGHT = 42
SCALE, HITBOX = sized(15, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a demon-masked shaman: a big red ceremonial mask with gold crown beads and a fanged grin, a ruff of white "
        "hair spikes, a tattered red cape, a green tunic with a gold amulet and brown boots")
BASE = {"red": (210, 50, 30), "red_dark": (130, 20, 10), "orange": (240, 140, 40), "gold": (240, 200, 70),
        "white": (240, 240, 244), "white_dark": (180, 180, 190), "green": (60, 160, 80), "green_dark": (24, 90, 40),
        "boot": (150, 100, 60), "boot_dark": (90, 56, 30), "skin": (200, 120, 80), "eye": (40, 140, 220),
        "tooth": (250, 250, 240), "mouth": (90, 10, 20)}
SHINY = {"red": (60, 80, 180), "red_dark": (20, 30, 100), "green": (190, 100, 40), "green_dark": (110, 50, 16)}


def P(v):
    return pal(BASE, SHINY, v)


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if math.hypot(a - sx * 2.2, b - 34.0) < 1.3:
                return (p["eye"] if math.hypot(a - sx * 2.2, b - 34.0) < 0.7 else p["white"]), None
        if abs(a) < 3.4 and 29.0 < b < 31.4:
            jag = abs(((a * 1.2) % 2) - 1)
            return (p["tooth"] if (b < 29.0 + jag or b > 31.4 - jag) else p["mouth"]), None
        if abs(a) < 0.6 and 31.6 < b < 33.6:
            return tone(p["orange"], face), None
    return armour(P, "red", "red_dark")(x, y, z, face, variant, box=box, **k)


def torn(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.18 * abs(math.sin((box.lo[0] + u) * 2.0)) + 0.03


def build():
    m = Model("baromon")
    top = m.bone("baromon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 5.4, 4.0, 10.0, 24.0, fabric(P, "green", "green_dark"), cut=1)  # tunic
    m.box(bd, -1.0, 17.0, -4.6, 1.0, 20.0, -3.8, solid(P, "gold"))                       # amulet
    rod(m, bd, (-2.0, 24.0, -3.8), (0, 20.0, -4.4), 1, solid(P, "gold"), extend=0)
    rod(m, bd, (2.0, 24.0, -3.8), (0, 20.0, -4.4), 1, solid(P, "gold"), extend=0)
    hd = m.bone("head", bd, (0, 24, 0))
    m.round_box(hd, 0, -0.6, 5.6, 4.6, 26.0, 38.0, maskf, cut=2)                        # big mask
    for i in range(5):                                           # gold crown beads
        ball(m, hd, (-3.6 + i * 1.8, 38.6, -2.6), 1.0, solid(P, "gold"), layers=2)
    for i in range(14):                                          # white hair spikes round the mask
        ang = math.radians(-100 + i * (200 / 13))
        spike(m, hd, (5.0 * math.sin(ang), 32.0 + 6.0 * math.cos(ang), 1.6), (math.sin(ang), math.cos(ang), 0.5),
              1.4, 4.0, strands(P, "white", "white_dark"), tip=0.5)
    cb = m.bone("cap", bd, (0, 24, 3))
    cape(m, cb, 25.0, 13.0, 22.0, cutout(torn, fabric(P, "red", "red_dark")), z=4.4, flare=1.1, panels=7,
         sweep=(0, 6))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.6, 22.0, 0))
        h = (sx * 8.0, 15.0, -3.0)
        rod(m, ab, (sx * 5.6, 22.0, 0), h, 3, fabric(P, "green", "green_dark"), extend=0.4)
        m.round_box(ab, h[0], h[2], 1.8, 1.8, h[1] - 2.4, h[1] + 1.0, skin(P, "skin"), cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 10.0, 0))
        m.round_box(lg, sx * 2.8, 0, 2.0, 2.0, 6.0, 11.0, fabric(P, "green", "green_dark"), cut=1)
        m.round_box(lg, sx * 3.0, -0.8, 2.6, 3.4, 0.0, 6.4, leather(P, "boot", "boot_dark"), cut=1)
    return m
