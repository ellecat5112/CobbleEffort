"""TV Rotom (Electric/Dark), after the user's Rotom doodle sheet (artist not named): Rotom haunting a flat-screen TV.
A purple-framed screen showing a shadowy figure in a hat and dark glasses over a "this program is unavailable" bar,
on a slim stand, with a purple plasma wisp curling from behind it.

Front is -z, y is up. 24 units tall; about 1.1 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _rotomform import palette, solid
from _route import tone

P = palette({"frame": (120, 70, 190), "frame_light": (160, 110, 220), "screen": (22, 26, 52), "shadow": (8, 8, 14),
             "aura": (150, 90, 230), "aura_light": (220, 190, 255)}, {"frame": (220, 200, 90), "frame_light": (246, 230, 140)})
HEIGHT = 24
SCALE = round(1.1 * 16 / HEIGHT, 3)
HITBOX = [1.2, HEIGHT / 16]
KIND = "floater"
K = 4
LOOK = "a purple flat-screen TV showing a shadowy figure in a hat and dark glasses, with a purple plasma wisp"


def screen(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        if abs(x) > 9.2 or y < 7.0 or y > 20.2:
            return p["frame"], None
        if 7.8 <= y <= 9.0 and abs(x) <= 6:
            return (p["white"] if int((x + 6) * 2) % 3 else p["screen"]), p["white"]   # the caption bar
        if 16.6 <= y <= 17.6 and abs(x) <= 4.0 or 17.6 < y <= 19.6 and abs(x) <= 2.4:
            return p["shadow"], None                        # the hat
        if math.hypot(x / 2.2, (y - 14.4) / 2.6) < 1:
            if 14.6 <= y <= 15.6 and 0.3 < abs(x) < 2.0:
                return p["charcoal"], None                  # dark glasses
            return p["shadow"], None
        if 9.6 <= y <= 12 and abs(x) <= 4.2 - (y - 9.6) * 0.6:
            return p["shadow"], None                        # shoulders
        return p["screen"], p["screen"]
    return tone(p["frame"], face), None


def build() -> Model:
    m = Model("rotom_tv")
    top = m.bone("rotom_tv", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.box(bd, -10, 6, -1.5, 10, 21, 1.5, screen)                          # the TV
    rod(m, bd, (0, 6, 0.5), (0, 2, 0.5), 1.4, solid(P, "frame_light"), extend=0.3)
    m.box(bd, -4, 0.5, -2, 4, 1.8, 3, solid(P, "frame_light"))           # stand
    wisp = m.bone("tail", bd, (-6, 6, 2))
    pts = [(-6, 7, 2), (-10, 4, 5), (-14, 6, 8), (-15, 11, 9), (-13, 14, 8)]
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        rod(m, wisp, a, b, 2.2 - i * 0.3, solid(P, "aura", glow=True), extend=0.5)       # the plasma wisp
    return m
