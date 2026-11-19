"""Brass Rotom (Ghost/Steel), after The_Aussie_Artist's Pokémon Abyss art: Rotom haunting a trumpet. A dark lacquered
trumpet held at a jaunty angle: a flared bell, a looped lead pipe and a mouthpiece, and a valve block whose two
silver valve caps are its eyes, with three pink valve keys below like teeth; orange plasma notes curl from the bell.

Shiny: pale ivory lacquer with teal keys.

Front is -z, y is up. 18 units tall, 34 long; about 1.1 blocks tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _rotomform import ABYSS, ABYSS_SHINY, disc_x, note_plane, palette, solid
from _route import tone

P = palette({**ABYSS, "aura": (250, 160, 100), "aura_light": (255, 226, 196)}, ABYSS_SHINY, aura_turn=0.0)
HEIGHT = 18
SCALE = round(1.1 * 16 / HEIGHT, 3)
HITBOX = [1.6, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a haunted dark trumpet whose silver valve caps are its eyes, with pink keys and orange plasma notes"


def valves(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for vx in (-2.6, 2.6):                              # silver valve caps: the eyes
            d = math.hypot(x - vx, y - 10.6)
            if d < 1.9:
                if d < 0.7:
                    return p["ink_dark"], None
                if d < 1.2:
                    return p["aura"], p["aura"]
                return p["silver"], p["silver"]
        if 6.4 <= y <= 8.4 and abs(x) <= 4.6:              # pink keys like teeth
            return (p["pink"] if abs((x + 4.6) % 3.1 - 1.55) < 1.2 else p["ink_dark"]), None
    return tone(p["ink"], face), None


def build() -> Model:
    m = Model("rotom_brass")
    top = m.bone("rotom_brass", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.box(bd, -5.5, 5, -2.5, 5.5, 13.5, 2.5, valves)                                  # the valve block (its face)
    rod(m, bd, (5.5, 9.5, 0), (12, 11, 0), 2.2, solid(P, "ink"), extend=0.4)          # tube to the bell
    for i, (x0, r) in enumerate([(12, 2.0), (14, 2.8), (16, 3.8), (17.5, 4.8), (18.5, 5.6)]):
        disc_x(m, bd, x0, x0 + 2, 11.5, 0, r, solid(P, "ink" if i < 4 else "ink_light"))   # the flared bell
    disc_x(m, bd, 20.3, 20.6, 11.5, 0, 4.4, solid(P, "ink_dark"))                    # the bell's dark mouth
    rod(m, bd, (-5.5, 9.5, 0), (-12, 8, 0), 1.6, solid(P, "ink"), extend=0.4)         # lead pipe
    rod(m, bd, (-12, 8, 0), (-15.5, 7.6, 0), 0.9, solid(P, "silver"), extend=0.2)     # mouthpiece
    m.round_box(bd, -16, 0, 1.0, 1.0, 6.8, 8.6, solid(P, "silver"), cut=0.4)
    rod(m, bd, (-5, 6, 1.5), (5, 6, 1.5), 1.4, solid(P, "ink_light"), extend=0.2)     # the tuning loop
    rod(m, bd, (-5, 4, 1.5), (5, 4, 1.5), 1.4, solid(P, "ink_light"), extend=0.2)
    for x, y, z, w, h in [(17, 18, -1, 4, 5), (22, 12, 1, 3.5, 4.5), (13, 1, -2, 3, 4)]:
        note_plane(m, bd, x, y, z, w, h, P)
    return m
