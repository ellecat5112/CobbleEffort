"""Grand Rotom (Ghost/Psychic), after The_Aussie_Artist's Pokémon Abyss art: Rotom haunting a grand piano. A dark
lacquered piano case on three slim legs, its lid raised showing a big pink swirl, a keyboard of pale pink keys
with black keys, and its face on the fallboard above the keys (magenta-rimmed eyes, a pink smile); a magenta plasma
hand plays it and notes float up.

Shiny: pale ivory lacquer with teal inlay.

Front is -z, y is up. 30 units tall; about 1.5 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _rotomform import ABYSS, ABYSS_SHINY, abyss_eye, note_plane, palette, solid
from _route import tone

P = palette({**ABYSS, "aura": (230, 80, 200), "aura_light": (255, 200, 245)}, ABYSS_SHINY, aura_turn=0.0)
HEIGHT = 30
SCALE = round(1.5 * 16 / HEIGHT, 3)
HITBOX = [1.6, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a haunted grand piano with its face above the keys, a pink swirl under the lid and a magenta plasma hand"


def keys(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        u = (x + 11) % 2.0
        if z < -6.2 and int((x + 11) // 2) % 7 not in (2, 6) and abs(u - 2.0) < 0.55 or (z < -6.2 and u < 0.55 and int((x + 11) // 2) % 7 not in (3, 0)):
            return p["ink_dark"], None                      # the black keys
        return (p["keywhite"] if abs(u - 1.0) < 0.85 else p["pink_dark"]), None
    if face == "north":
        return p["pink"], None
    return tone(p["ink"], face), None


def fallboard(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = abyss_eye(x - 3.0 * sx, y - 15.6, 1.0, 1.6, p)
            if e:
                return e
        if 13.0 <= y <= 13.8 and abs(x) <= 2.4 - (13.8 - y) * 0.8:
            return p["pink"], None                          # the smile
    return tone(p["ink"], face), None


def lid(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":                                        # on the raised lid: a big pink swirl
        a = math.atan2(z - 5, x - 1)
        d = math.hypot(z - 5, x - 1)
        t = (a + math.pi) / (2 * math.pi)
        if abs(((d - t * 2.6) % 2.6) - 1.3) < 0.42 and d < 8:
            return p["pink"], None
        return p["ink_dark"], None
    return tone(p["ink"], face), None


def build() -> Model:
    m = Model("rotom_grand")
    top = m.bone("rotom_grand", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.box(bd, -11, 9, -6, 11, 15, 6, solid(P, "ink"))                                 # the case: front...
    m.box(bd, -11, 9, 6, 6, 15, 13, solid(P, "ink"))                                  # ...curving narrower...
    m.box(bd, -11, 9, 13, 1, 15, 17, solid(P, "ink"))                                 # ...to the tail
    m.box(bd, -11, 10.5, -9, 11, 12, -6, keys)                                        # the keyboard
    m.box(bd, -10, 12, -7, 10, 18, -6, fallboard)                                     # fallboard: its face
    hd = m.bone("head", bd, (0, 15, -6))
    m.box(hd, -11, 15, -6, 11, 15.8, 16, lid, rotation=(30, 0, 0), pivot=(0, 15, -6))   # the open lid
    for x, z in ((-9, -4), (9, -4), (-6, 14)):                                        # three slim legs
        rod(m, bd, (x, 9, z), (x * 1.08, 0, z - 1), 1.4, solid(P, "ink"), extend=0.3)
        m.box(bd, x * 1.08 - 1, 0, z - 2, x * 1.08 + 1, 0.8, z, solid(P, "pink_dark"))
    hand = m.bone("arm_right", bd, (-12, 12, -8))
    rod(m, hand, (-11, 12, 0), (-15, 15, -6), 1.4, solid(P, "aura", glow=True), extend=0.4)   # the plasma hand
    rod(m, hand, (-15, 15, -6), (-12, 12.5, -9), 1.6, solid(P, "aura", glow=True), extend=0.4)
    for i in range(4):
        rod(m, hand, (-12, 12.5, -9), (-11 + i * 1.3, 11.6, -10.5), 0.6, solid(P, "aura_light", glow=True), extend=0.2)
    for x, y, z, w, h in [(-16, 22, -2, 4, 5), (12, 24, 2, 3.5, 4.5), (2, 27, 8, 3, 4)]:
        note_plane(m, bd, x, y, z, w, h, P)
    return m
