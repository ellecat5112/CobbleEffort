"""Creepish, the Lagoon Lurker Pokémon (Water/Dark), Fishugly evolved, after the art of the A. Fakemon fanpage (the
art's own name): a creepy fish-man crouched on bent frog legs, its long blue arms raised with clawed, finned hands. Its
green fish face with goggle-like ringed eyes and a toothy mouth peers out of a great black frill; its belly is blue
and scaled, its back and legs are dark green, black knobs cap its knees and a fin-tail trails behind it.

Shiny: violet arms, a lilac belly and rose-green skin.

Front is -z, y is up. 35 units tall to its raised claws; baseScale 0.68 (1.5 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _fishface import P, fin, grimace, ring_eye, solid
from _route import tone

SCALE = 0.68
HITBOX = [1.5, 2.2]
KIND = "biped"
K = 3
HEIGHT = 35
LOOK = ("a creepy fish-man on bent frog legs with raised clawed blue arms, a green fish face with ringed goggle eyes "
        "and a toothy mouth in a great black frill, a scaled blue belly and a dark green back")


def bellyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        row = math.floor((y - 11.0) / 1.6)
        xx = ((x + row * 0.8) % 1.6) - 0.8
        yy = (y - 11.0) % 1.6
        if abs(yy - (1.6 - math.sqrt(max(0.0, 0.64 - xx * xx)))) < 0.16:
            return p["blue_dark"], None                                       # scales
        return tone(p["blue"], face), None
    return tone(p["green_dark"], face), None


def chestf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" or (face in ("east", "west") and z < -1.0):
        return tone(p["blue"], face), None
    return tone(p["green_dark"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = ring_eye(p, x - sx * 1.4, y - 26.6, 1.05)
            if e:
                return e, None
        g = grimace(p, x, y, 1.7, 23.0, 24.9, pointed=True)
        if g:
            return g, None
        for sx in (-1, 1):
            if abs(x - sx * 2.2) < 0.35 and 23.4 < y < 25.4:
                return p["blue"], None                                        # blue streaks down its cheeks
    return tone(p["green"], face), None


def frill(a, b):
    r, t = math.hypot(a, b - 24.5), math.atan2(a, b - 24.5)
    return r < 7.6 + 1.0 * math.cos(t * 7) and b > 17.0


def frill_colour(p, a, b):
    t = math.atan2(a, b - 24.5)
    return p["cream"] if abs(abs(t) - 2.2) < 0.3 and math.hypot(a, b - 24.5) > 4.5 else p["black"]


def build() -> Model:
    m = Model("creepish")
    top = m.bone("creepish", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0.0, 3.6, 2.8, 11.0, 18.0, bellyf, cut=1.2)             # scaled blue belly
    m.round_box(bd, 0, 0.0, 4.4, 3.0, 18.0, 24.0, chestf, cut=1.4)             # its chest and shoulders
    m.box(bd, -9.0, 17.0, -3.4, 9.0, 33.4, -3.4, fin(frill, frill_colour))       # the great black frill

    hd = m.bone("head", bd, (0, 24, -1))
    m.round_box(hd, 0, -2.0, 3.0, 3.0, 22.5, 28.2, headf, cut=1.0)
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.8, 28.0, -1.0), (sx * 0.4, 1, 0.2), 1.2, 1.8, solid("black"))   # little head fins

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 3.0, 13, 0.5))
        rod(m, lb, (sx * 3.0, 13.0, 0.5), (sx * 6.5, 8.0, -1.5), 3.4, solid("blue"), extend=0.6)     # thighs
        m.round_box(lb, sx * 6.6, -1.6, 1.6, 1.6, 6.6, 9.6, solid("black"), cut=0.6)                   # knee knobs
        rod(m, lb, (sx * 6.5, 8.0, -1.5), (sx * 5.5, 2.0, 0.5), 2.8, solid("green_dark"), extend=0.6)
        m.round_box(lb, sx * 5.5, -1.2, 2.4, 3.2, 0.0, 1.6, solid("green_dark"), cut=0.8)              # webbed feet
        for dx in (-1.2, 0.0, 1.2):
            spike(m, lb, (sx * 5.5 + dx, 0.6, -4.2), (0, -0.2, -1), 1.0, 1.8, solid("black"))

        ar = m.bone(f"arm_{side}", bd, (sx * 4.4, 23, 0))                       # long arms, raised
        rod(m, ar, (sx * 4.4, 23.0, 0.0), (sx * 10.0, 27.0, -1.0), 2.8, solid("blue"), extend=0.6)
        rod(m, ar, (sx * 10.0, 27.0, -1.0), (sx * 12.0, 33.0, -3.0), 2.6, solid("blue"), extend=0.6)
        spike(m, ar, (sx * 11.0, 30.0, -2.0), (sx * 1, -0.3, 0.3), 1.6, 3.0, solid("cream"))          # arm fins
        spike(m, ar, (sx * 6.6, 25.0, -0.4), (sx * 0.3, -1, 0.3), 1.6, 2.6, solid("cream"))
        m.round_box(ar, sx * 12.4, -3.6, 1.8, 1.6, 32.0, 34.6, solid("blue"), cut=0.6)                # hands
        for dx in (-1.0, 0.0, 1.0):
            spike(m, ar, (sx * 12.4 + dx, 33.0, -5.0), (0, -0.7, -1), 0.9, 2.4, solid("blue_dark"))   # claws

    tl = m.bone("tail", bd, (0, 13, 2.5))
    rod(m, tl, (0, 13.0, 2.5), (0, 9.0, 10.0), 2.4, solid("green_dark"), extend=0.5)
    m.box(tl, 0, 6.0, 4.0, 0, 13.0, 11.0, fin(                                   # its fin-tail
        lambda a, b: a > 4.0 and abs(b - (13.0 - (a - 2.5) * 0.53)) < 1.6 + (a - 4.0) * 0.25,
        lambda p, a, b: p["green_dark"]))
    return m
