"""Kaguyamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the moon princess puppet: a slender doll in a long white robe edged in yellow and violet with
long dark hair and a pale masked face under a tall teal-and-yellow crescent headdress, wide white sleeves, thin jointed
silver puppet arms with teal joint beads reaching out on each side, a magenta lantern base it floats on, and a ring of
floating cyan crystal blades. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, cutout, fabric, gem, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = ("a slender moon-princess puppet in a long white robe under a tall crescent headdress, with thin jointed puppet "
        "arms, a magenta lantern base and floating cyan crystal blades")
BASE = {"white": (244, 246, 250), "white_dark": (170, 176, 196), "yellow": (240, 210, 60), "violet": (130, 60, 180),
        "teal": (60, 200, 190), "teal_light": (200, 255, 250), "magenta": (200, 50, 160), "magenta_dark": (110, 14, 80),
        "hair": (40, 40, 56), "hair_dark": (14, 14, 22), "face": (240, 236, 236), "eye": (200, 40, 60),
        "silver": (200, 204, 216), "silver_dark": (100, 104, 120), "crystal": (140, 220, 255, 190),
        "crystal_light": (230, 250, 255, 220)}
SHINY = {"white": (60, 60, 80), "white_dark": (20, 20, 30), "teal": (240, 140, 60), "teal_light": (255, 220, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def robef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if face == "north" and (abs(x) < 0.5 or abs(abs(x) - 3.0) < 0.3):
        return tone(p["yellow"] if abs(x) >= 0.5 else p["violet"], face), None
    return fabric(P, "white", "white_dark")(x, y, z, face, variant, box=box, **k)


def shard_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6), v / max(H, 1e-6)
    return abs(a - 0.5) < 0.5 * (1 - abs(b - 0.5) * 2) + 0.02


def shardf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["crystal_light"] if abs(u - W / 2) < 0.4 else p["crystal"]
    return c, c[:3]


def build():
    m = Model("kaguyamon")
    top = m.bone("kaguyamon", None, (0, 0, 0))
    m.round_box(top, 0, 0, 3.0, 3.0, 0.0, 6.0, armour(P, "magenta", "magenta_dark", trim="yellow"), cut=1)  # lantern base
    bd = m.bone("body", top, (0, 6, 0))
    for j in range(6):                                                               # long white robe
        r = 7.0 - j * 0.8
        m.round_box(bd, 0, 0.6, r, r * 0.8, 6.0 + j * 7.0, 13.4 + j * 7.0, robef, cut=max(1, int(r * 0.3)))
    for sx in (-1, 1):                                                               # wide sleeves
        m.round_box(bd, sx * 5.4, -1.4, 2.6, 3.0, 36.0, 47.0, robef, cut=1)
    hd = m.bone("head", bd, (0, 49, 0))
    m.round_box(hd, 0, 0, 2.2, 2.4, 48.0, 53.6, skin(P, "face", dark="white_dark"), cut=1)
    m.box(hd, -1.4, 51.0, -2.5, 1.4, 51.4, -2.4, solid(P, "eye"))
    for i in range(9):                                                               # long dark hair
        ang = math.radians(-100 + i * 25)
        rod(m, hd, (2.2 * math.sin(ang), 53.0, 0.6 + 1.2 * math.cos(ang)), (3.2 * math.sin(ang), 32.0, 2.4), 1,
            strands(P, "hair", "hair_dark"), extend=0.3, t2=2)
    pts = [(0, 53.6, 0), (2.0, 58.0, 0), (4.0, 63.0, 0), (5.0, 66.0, 0)]             # tall crescent headdress
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 3 - j, armour(P, "teal", "teal", trim="yellow", trim_w=0.3), extend=0.4)
    m.round_box(hd, 0, -2.2, 1.0, 0.4, 54.0, 56.0, solid(P, "yellow"), cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # thin jointed puppet arms
        ab = m.bone(nm, bd, (sx * 6.0, 40.0, 0))
        pts = [(sx * 6.0, 40.0, 0), (sx * 14.0, 34.0, -2.0), (sx * 20.0, 26.0, -1.0), (sx * 22.0, 16.0, 0.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 1, metal(P, "silver", dark="silver_dark"), extend=0, t2=1)
            m.round_box(ab, p1[0], p1[2], 0.9, 0.9, p1[1] - 0.9, p1[1] + 0.9, gem(P, "teal", "teal_light"), cut=0)
    rb = m.bone("ring_blades", bd, (0, 40, 0))                                        # floating crystal blades
    for i in range(6):
        ang = 2 * math.pi * i / 6
        c = (18.0 * math.cos(ang), 46.0 + 8.0 * math.sin(ang * 2), 6.0 + 4.0 * math.sin(ang))
        m.box(rb, c[0] - 1.6, c[1] - 6.0, c[2], c[0] + 1.6, c[1] + 6.0, c[2], cutout(shard_in, shardf),
              rotation=(0, 0, math.degrees(ang) - 90 + 30), pivot=c)
    return m
