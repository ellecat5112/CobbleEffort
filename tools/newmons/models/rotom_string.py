"""String Rotom (Ghost/Grass), after The_Aussie_Artist's Pokémon Abyss art: Rotom haunting a violin. A dark lacquered
figure-eight body with its face on the upper bowl (green-rimmed eyes, a pink smile, pink swirls on its cheeks), pink
scroll-and-ring inlay on the lower bowl, four pale strings down a black fingerboard, a scrolled head with pegs, and
its bow made of glowing green plasma, with green notes drifting round it.

Shiny: pale ivory lacquer with teal inlay.

Front is -z, y is up. 34 units tall; about 1.5 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _rotomform import ABYSS, ABYSS_SHINY, abyss_eye, note_plane, palette, solid
from _route import tone

P = palette({**ABYSS, "aura": (110, 220, 120), "aura_light": (210, 255, 210)}, ABYSS_SHINY, aura_turn=0.0)
HEIGHT = 34
SCALE = round(1.5 * 16 / HEIGHT, 3)
HITBOX = [0.9, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a haunted dark violin with a smiling face on its upper bowl and a bow of green plasma"


def body(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        if abs(x) <= 1.3 and 21 <= y <= 31:                # the fingerboard on the neck
            return (p["grey_light"] if abs((x * 2.4) % 1.2 - 0.6) < 0.14 else p["ink_dark"]), None
        for sx in (-1, 1):
            e = abyss_eye(x - 2.9 * sx, y - 17.6, 1.3, 1.8, p)
            if e:
                return e
            if 2 <= abs(x) <= 5 and sx * x > 0 and abs(math.hypot(abs(x) - 4.2, y - 14.6) - 0.9) < 0.35:
                return p["pink"], None                      # cheek swirls
        if 12.4 <= y <= 15.2 and abs(x) <= 2.6 and (y - 15.2) > -1.6 - (2.6 - abs(x)) * 0.5 and y - 15.2 < -0.2 + abs(x) * 0.15:
            return p["pink"], None                          # the smile
        if abs(x) <= 1.3 and 4 <= y <= 21 and abs((x * 2.4) % 1.2 - 0.6) < 0.12:
            return p["grey_light"], None                    # the strings over its face
        if 2 <= y <= 9:                                     # inlay on the lower bowl: a ring between two scrolls
            if abs(math.hypot(x, y - 5.2) - 2.0) < 0.5:
                return p["pink"], None
            for sx in (-1, 1):
                if abs(math.hypot(x - 4.5 * sx, y - 5.2) - 1.3) < 0.35 and (y - 5.2) * sx < 0.8:
                    return p["pink"], None
    return tone(p["ink"], face), None


def build() -> Model:
    m = Model("rotom_string")
    top = m.bone("rotom_string", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for cy, r, n in ((5.6, 6.2, 5), (16.4, 5.4, 4)):                       # the two bowls, round slices
        hs = 2 * r / n
        for i in range(n):
            y0 = cy - r + i * hs
            t = (y0 + hs / 2 - cy) / r
            w = max(2.0, (r + 1.3) * math.sqrt(max(0.0, 1 - t * t)))
            m.box(bd, -w, y0, -2.4, w, y0 + hs + 0.05, 2.4, body)
    m.box(bd, -4.0, 10.6, -2.2, 4.0, 12.2, 2.2, body)                       # waist
    hd = m.bone("head", bd, (0, 21, 0))
    m.box(hd, -1.3, 21, -1.6, 1.3, 31, 0.8, body)                           # neck and fingerboard
    m.box(hd, -2.2, 30.5, -1.4, 2.2, 33, 1.2, solid(P, "ink_dark"))         # pegbox
    m.box(hd, -1.4, 33, -0.8, 1.4, 34.5, 1.6, solid(P, "ink"))              # scroll
    for sx in (-1, 1):
        m.box(hd, 2.2 * sx - (1.4 if sx > 0 else 0), 31, -0.4, 2.2 * sx + (0 if sx > 0 else 1.4), 31.9, 0.4, solid(P, "ink_light"))
    bow = m.bone("bow", bd, (8, 2, -3))
    rod(m, bow, (9.5, 1, -3.5), (11.5, 31, -3.5), 1.0, solid(P, "aura", glow=True), extend=0.3)   # the plasma bow
    rod(m, bow, (8.6, 2.5, -3.5), (10.6, 29, -3.5), 0.4, solid(P, "aura_light", glow=True), extend=0.2)
    for x, y, z, w, h in [(-12, 20, -2, 4, 5), (-10, 6, -3, 3, 4), (12, 18, -1, 3.5, 4.5)]:
        note_plane(m, bd, x, y, z, w, h, P)
    return m
