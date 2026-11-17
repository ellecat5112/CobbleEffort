"""Blikmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a boxy toy robot. A tall white head block with a pink chevron brow, a pale cyan visor slit, a grille
mouth of dark slots and yellow lamp "ears"; a broad white body block with two yellow panel lights and a round port
on each side; short grey arms ending in red C-shaped claws; and two tread blocks for feet. 25 blocks tall.

Front is -z, y is up. 46 units tall; Perfect stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _digi import sized
from _digidetail import armour, local, metal, solid
from _route import pal, tone

HEIGHT = 46
SCALE, HITBOX = sized(25, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a boxy white toy robot with a pink chevron brow, a cyan visor, a grille mouth, yellow lamp ears, yellow "
        "panel lights, red C-shaped claws and tread feet")
BASE = {"white": (240, 240, 246), "white_dark": (170, 172, 186), "grey": (150, 152, 164), "grey_dark": (70, 72, 84),
        "pink": (236, 60, 110), "pink_dark": (160, 24, 70), "cyan": (150, 230, 250), "yellow": (250, 236, 60),
        "yellow_dark": (200, 170, 20), "red": (230, 20, 30), "red_dark": (140, 8, 16), "slot": (40, 40, 48)}
SHINY = {"white": (60, 62, 74), "white_dark": (24, 24, 32), "pink": (60, 220, 160), "pink_dark": (20, 140, 90),
         "red": (40, 120, 240), "red_dark": (14, 50, 150), "yellow": (250, 140, 40), "yellow_dark": (190, 90, 10)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", seams=(12.0, 24.0))
GREY = metal(P, "grey", dark="grey_dark")
RED = armour(P, "red", "red_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 35.5 < y < 37.0 and abs(x) < 4.0:
            return p["cyan"], p["cyan"]                                     # visor slit
        if 29.0 < y < 34.5 and abs(x) < 4.6:                               # grille: dark slots between white bars
            return tone(p["slot"] if (x + 4.6) % 1.84 < 1.0 else p["white"], face), None
    return WHITE(x, y, z, face, variant, box=box, **k)


def treadf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    rib = (z if face in ("east", "west", "up", "down") else y) % 1.6 < 0.6
    return tone(p["grey_dark"] if rib else p["grey"], face), None


def build():
    m = Model("blikmon")
    top = m.bone("blikmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.box(bd, -9.0, 7.0, -6.0, 9.0, 27.0, 6.0, WHITE)                                    # body block
    m.box(bd, -9.4, 25.0, -6.4, 9.4, 27.4, 6.4, WHITE)                                   # shoulder rim
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 2.0, sx * 6.0))
        m.box(bd, x0, 18.0, -6.6, x1, 21.6, -6.0, solid(P, "yellow", glow=True))         # panel lights
        x0, x1 = sorted((sx * 9.0, sx * 9.8))
        m.box(bd, x0, 15.0, -2.4, x1, 21.0, 2.4, GREY)                                   # side ports
        m.box(bd, min(sx * 9.8, sx * 10.2), 16.2, -1.2, max(sx * 9.8, sx * 10.2), 19.8, 1.2, solid(P, "slot"))
    hd = m.bone("head", bd, (0, 27, 0))
    m.box(hd, -6.4, 27.0, -5.6, 6.4, 45.0, 5.6, headf)                                  # head block
    for sx in (-1, 1):                                                                    # chevron brow
        x0, x1 = sorted((0.0, sx * 5.0))
        m.box(hd, x0, 39.0, -6.2, x1, 41.0, -5.4, solid(P, "pink"), rotation=(0, 0, sx * 12), pivot=(0, 39.5, -5.8))
        x0, x1 = sorted((sx * 6.4, sx * 8.4))
        m.box(hd, x0, 35.0, -2.4, x1, 39.6, 2.4, solid(P, "yellow", glow=True))          # lamp ears
    m.box(hd, -0.6, 45.0, -0.6, 0.6, 46.0, 0.6, GREY)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 9.0, 22.0, 0))
        rod(m, ab, (sx * 9.0, 22.0, 0), (sx * 13.0, 22.0, -1.0), 4, GREY, extend=0.4)
        cx = sx * 15.0                                                                  # the C-claw, open to the side
        m.box(ab, min(cx - sx * 2.0, cx), 18.0, -3.0, max(cx - sx * 2.0, cx), 26.0, 1.0, RED)
        for yy in (18.0, 23.6):
            m.box(ab, min(cx, cx + sx * 3.0), yy, -3.0, max(cx, cx + sx * 3.0), yy + 2.4, 1.0, RED)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.5, 8.0, 0))
        x0, x1 = sorted((sx * 1.6, sx * 7.6))
        m.box(lg, x0, 0.0, -5.4, x1, 8.0, 5.0, treadf)
        m.box(lg, min(x0, x1) + 0.6, 6.0, -4.0, max(x0, x1) - 0.6, 9.0, 3.6, GREY)
    return m
