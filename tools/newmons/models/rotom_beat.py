"""Beat Rotom (Ghost/Fighting), after The_Aussie_Artist's Pokémon Abyss art: Rotom haunting a drum kit. A big dark
bass drum whose head is its face (red-rimmed eyes, a stern little frown, a pink centre circle), two tom drums in
front, two dark cymbals on thin stands above, and arms of red plasma drumming with glowing sticks, red notes flying.

Shiny: pale ivory shells with teal heads.

Front is -z, y is up. 26 units tall; about 1.4 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _rotomform import ABYSS, ABYSS_SHINY, abyss_eye, disc_z, note_plane, palette, solid
from _route import tone

P = palette({**ABYSS, "aura": (236, 90, 90), "aura_light": (255, 200, 190)}, ABYSS_SHINY, aura_turn=0.0)
HEIGHT = 26
SCALE = round(1.4 * 16 / HEIGHT, 3)
HITBOX = [1.4, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a haunted drum kit: a bass drum with a stern face, two toms, two cymbals and red plasma arms with drumsticks"


def bass(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x, y - 11)
        if d > 7.4:
            return p["ink_light"], None                    # the hoop
        for sx in (-1, 1):
            e = abyss_eye(x - 2.6 * sx, y - 14.2, 0.9, 1.4, p)
            if e:
                return e
        if 12.3 <= y <= 12.9 and abs(x) <= 1.1:
            return p["ink_dark"], None                     # a stern little frown
        if math.hypot(x, y - 8.6) < 2.6:
            return p["pink"], None
        return p["ink"], None
    if face in ("east", "west", "up", "down") and int((z + 0.3) * 1.2) % 4 == 0:
        return p["ink_light"], None                        # shell lugs
    return tone(p["ink"], face), None


def tom(cx, cy):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            return (p["pink"] if math.hypot(x - cx, y - cy) < 1.4 else p["ink_dark"] if math.hypot(x - cx, y - cy) > 3.2
                    else p["ink"]), None
        if int((z + y) * 1.2) % 3 == 0:
            return p["ink_light"], None
        return tone(p["ink"], face), None
    return s


def build() -> Model:
    m = Model("rotom_beat")
    top = m.bone("rotom_beat", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    disc_z(m, bd, 0, 11, -4, 4, 8, bass)                                   # the bass drum (its face)
    for sx in (-1, 1):                                                       # tom drums in front
        disc_z(m, bd, 8.2 * sx, 4.2, -8, -3, 3.8, tom(8.2 * sx, 4.2))
        rod(m, bd, (5.5 * sx, 13, 2), (11 * sx, 23, 2), 0.6, solid(P, "silver"), extend=0.2)   # cymbal stands
        m.round_box(bd, 11.5 * sx, 2, 4.5, 4.5, 23, 23.8, solid(P, "ink_dark"), cut=1.6)        # cymbals
        m.box(bd, 11.5 * sx - 0.5, 23.8, 1.5, 11.5 * sx + 0.5, 24.6, 2.5, solid(P, "ink_light"))
    for sx in (-1, 1):                                                       # red plasma arms with sticks
        arm = m.bone(f"arm_{'left' if sx > 0 else 'right'}", bd, (7 * sx, 12, 0))
        rod(m, arm, (7 * sx, 12, 0), (13 * sx, 16, -2), 1.2, solid(P, "aura", glow=True), extend=0.4)
        rod(m, arm, (13 * sx, 16, -2), (11 * sx, 10, -7), 1.2, solid(P, "aura", glow=True), extend=0.4)
        rod(m, arm, (11 * sx, 10, -7), (9 * sx, 6, -11), 0.7, solid(P, "aura_light", glow=True), extend=0.2)
        m.round_box(arm, 9 * sx, -11.2, 0.9, 0.9, 5.2, 6.8, solid(P, "aura", glow=True), cut=0.4)
    for x, y, z, w, h in [(-16, 10, -2, 3.5, 4.5), (13, 6, -3, 3, 4), (-3, 22, -1, 3, 4)]:
        note_plane(m, bd, x, y, z, w, h, P)
    return m
