"""Drill Rotom (Electric/Steel), after the Joseon Region fakemon art: Rotom inside a tracked drilling rig. Two black
caterpillar tracks with orange wheel hubs, a grey ribbed engine in an orange casing, a black frame with an orange
grab bar at the back, and a long orange drill mast with a T-handle and Rotom's spike, angled down to the drilling
head: a round orange head with one big lens eye and a mouth full of grinding teeth round a grey drill bit. Pale teal
plasma crackles round it.

Front is -z, y is up. 32 units tall; about 1.8 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _rotomform import ball, bolt_plane, palette, rotom_eye, solid
from _route import tone

P = palette({"aura": (150, 230, 220), "aura_light": (225, 255, 250), "iris": (150, 232, 226)})
HEIGHT = 32
SCALE = round(1.8 * 16 / HEIGHT, 3)
HITBOX = [1.4, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a tracked drilling rig with an orange drill mast and a one-eyed drilling head full of grinding teeth"


def track(sx):
    hubs = [(-3.0, 2.6), (1.5, 2.6), (6.0, 2.6)]

    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == ("east" if sx < 0 else "west"):
            for hz, hy in hubs:
                d = math.hypot(z - hz, y - hy)
                if d < 1.5:
                    return tone(p["orange"], face), None
                if d < 1.9:
                    return p["charcoal"], None
        if face in ("up", "down", "north", "south") and int((z + y) * 1.4) % 2 == 0:
            return p["charcoal"], None
        return tone(p["black"], face), None
    return s


def engine(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        return tone(p["orange"], face), None
    if face == "up":
        return (p["grey_dark"] if int(z) % 2 == 0 else p["grey_light"]), None
    return tone(p["grey"] if int(y) % 3 else p["grey_dark"], face), None


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        e = rotom_eye(x - 0.0, y - 14.6, 1.9, p)
        if e:
            return e
        d = math.hypot(x, y - 11.0)
        if d < 2.7:                                         # the grinding mouth: a ring of teeth round the bit
            a = math.atan2(y - 11.0, x)
            if d > 1.7:
                return (p["white"] if int((a + math.pi) / (2 * math.pi) * 12) % 2 == 0 else p["mouth"]), None
            return p["mouth"], None
    return tone(p["orange"], face), None


def build() -> Model:
    m = Model("rotom_drill")
    top = m.bone("rotom_drill", None, (0, 0, 0))
    body = m.bone("body", top, (0, 8, 0))
    for sx in (-1, 1):                                      # caterpillar tracks
        m.box(body, 5 * sx if sx > 0 else -9, 0, -6, 9 if sx > 0 else -5, 5, 8, track(sx))
    m.box(body, -5, 3, -4, 5, 11, 6, engine)                # the ribbed engine in its orange casing
    m.box(body, -5.5, 11, -2, 5.5, 12, 4, solid(P, "charcoal"))
    for sx in (-1, 1):                                      # the back frame and its orange grab bar
        m.box(body, 3.5 * sx - 0.75, 11, 6, 3.5 * sx + 0.75, 19, 7.5, solid(P, "black"))
    m.box(body, -4.5, 19, 5.5, 4.5, 20.5, 8, solid(P, "orange"))
    mast = m.bone("mast", body, (0, 12, 2))
    rod(m, mast, (0, 30, 10), (0, 13, -13), 2.4, solid(P, "orange"))          # the drill mast
    rod(m, mast, (0, 11.5, 1.5), (0, 20.5, -2.5), 1.6, solid(P, "charcoal"))  # strut from the engine
    rod(m, mast, (0, 30, 10), (0, 33.5, 11.5), 1.2, solid(P, "black"), extend=0.5)
    m.box(mast, -3.5, 32.5, 10.5, 3.5, 34, 12, solid(P, "black"))             # T-handle
    spike(m, mast, (0, 25, 4.5), (0, 1, -0.4), 1.6, 3.5, solid(P, "orange_light"), tip=0.9)
    hd = m.bone("head", mast, (0, 12, -16))
    ball(m, hd, 0, 12.5, -16.5, 4.2, head)                                    # the drilling head
    spike(m, hd, (0, 11.0, -20.2), (0, -0.2, -1), 1.8, 4.5, solid(P, "grey_light"), tip=0.9)
    for i, (x, y, z, w, h, pl, fl) in enumerate([(-11, 7, -3, 6, 11, "zy", False), (10, 16, -9, 5, 10, "zy", True),
                                                 (-6, 21, -12, 6, 9, "xy", False), (5, 3, -12, 5, 8, "xy", True)]):
        bolt_plane(m, body, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
