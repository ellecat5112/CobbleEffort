"""Shared parts for the tardigrade line (after @victorious_trainer's Pokémon Victory art, names kept): Tardigrub and
Aristograd. Plump, glossy, segmented water bears: teal bodies with darker bellies and grooves, a round red mouth ring set
in a black X-shaped face, round spots on the sides of the head and stubby legs with little toe nubs. Aristograd is a
great lavender-and-white ball with four pods in its back, Tardigrubs peeking out of two of them.

`grub(m, bone, c, s, P, leg_bone)` builds a whole Tardigrub at any scale (the minis riding in Aristograd's pods)."""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _route import pal, tone

BASE = {"teal": (128, 222, 210), "teal_light": (176, 240, 232), "teal_dark": (74, 156, 158), "teal_deep": (52, 118, 124),
        "mouth": (196, 62, 70), "mouth_dark": (84, 30, 44), "mask": (30, 30, 36), "white": (250, 250, 250),
        "lav": (176, 172, 234), "lav_light": (232, 232, 252), "lav_dark": (120, 112, 196), "lav_deep": (84, 76, 152),
        "pink": (232, 104, 176), "pink_dark": (150, 50, 110), "claw": (34, 34, 40), "hole": (26, 24, 40)}


def palette(shiny):
    def P(v):
        return pal(BASE, shiny, v)
    return P, solid_of(P), ramp_of(P)


def face_ring(p, u, v, s, ring="mouth", inner="mouth_dark", mask="mask", reach=2.4):
    """The round mouth ring in a black X: (u, v) = offset from the mouth's centre on the face, in model units."""
    r = math.hypot(u, v)
    if r < 0.55 * s:
        return p[inner]
    if r < 1.2 * s:
        return p[ring]
    if r < reach * s and abs(abs(u) - abs(v)) < 0.55 * s + (reach * s - r) * 0.35:
        return p[mask]
    return None


def grub(m, bone, c, s, P, leg_bone=None, glossy=True, head_bone=None):
    """A whole Tardigrub at scale s, centred on c = (x, y-bottom, z), facing -z. Legs on leg_bone(i, side) bones when
    given (the full-size Pokémon), else on `bone`."""
    cx, cy, cz = c
    hz = cz - 6.6 * s                                                   # the head's front

    def body(x, y, z, face, variant, **k):
        p = P(variant)
        lz = (z - cz) / s
        ly = (y - cy) / s
        if ly < 2.6:
            return tone(p["teal_dark"], face), None                    # the darker belly
        if face in ("up", "east", "west") and -3.8 < lz < 5.4 and abs((lz + 0.4) % 2.4 - 1.2) < 0.2 + 0.15 / s:
            return tone(p["teal_dark"], face), None                    # grooves between the segments
        if glossy and face == "up" and abs((x - cx) / s + 1.5) < 0.6 and -2 < lz < 2:
            return tone(p["teal_light"], face), None                   # a glossy highlight
        return tone(p["teal"], face), None

    def head(x, y, z, face, variant, **k):
        p = P(variant)
        hy = cy + 5.0 * s
        if face == "north":
            col = face_ring(p, x - cx, y - hy, s)
            if col is not None:
                return col, None
        if face in ("east", "west"):
            d = math.hypot(y - hy - 0.3 * s, z - (hz + 1.6 * s))
            if d < 1.1 * s:
                return (p["teal_light"] if d < 0.85 * s else p["teal_deep"]), None   # round side spots
        if (y - cy) / s < 2.6:
            return tone(p["teal_dark"], face), None
        return tone(p["teal"], face), None

    for y0, y1, rx, rz in ((1.0, 2.6, 4.2, 5.8), (2.6, 6.6, 5.0, 6.6), (6.6, 8.2, 4.3, 6.0), (8.2, 9.2, 3.2, 4.8)):
        m.round_box(bone, cx, cz + 0.6 * s, rx * s, rz * s, cy + y0 * s, cy + y1 * s, body,
                    cut=max(0.5, round(min(rx, rz) * s * 0.4, 1)))
    m.round_box(head_bone or bone, cx, hz + 1.8 * s, 3.4 * s, 2.0 * s, cy + 1.8 * s, cy + 7.8 * s, head,
                cut=max(0.5, round(1.0 * s, 1)))                       # the head, a little narrower
    for i, lz in enumerate((-3.6, -1.0, 1.8, 4.6)):                     # four pairs of stubby legs
        for sx, side in ((1, "left"), (-1, "right")):
            lb = leg_bone(i, side) if leg_bone else bone
            lx = cx + sx * 4.4 * s
            m.round_box(lb, lx, cz + lz * s, 1.3 * s, 1.3 * s, cy, cy + 2.6 * s,
                        lambda x, y, z, face, variant, **k: (tone(P(variant)["teal_dark" if y < cy + 1.2 * s else "teal"],
                                                                  face), None), cut=max(0.4, round(0.4 * s, 1)))
            if s >= 0.8:
                for dz in (-0.8, 0.8):                                 # little toe nubs
                    m.box(lb, lx + sx * 0.6 * s - 0.5, cy, cz + (lz + dz) * s - 0.5, lx + sx * 0.6 * s + 0.5, cy + 1,
                          cz + (lz + dz) * s + 0.5, lambda x, y, z, face, variant, **k: (tone(P(variant)["teal_deep"], face), None))
