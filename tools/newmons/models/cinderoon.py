"""Cinderoon, the Cinder Cocoon Pokémon (Fire/Bug), hand-built from boxes from the user's design.

A teardrop cocoon of smouldering ash you can see through: the shell is a translucent layer of dark grey ash flecked
with embers and crossed by glowing orange zigzag bands, with two little coal horns on top. Inside, curled up with its
head at the top, is the Coalarva it was: ruby eyes peering out and its burning abdomen glowing through the ash.

Front is -z, y is up. 25 units tall with its horns; baseScale 0.64 (1.0 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _coal import coal, fire, glowing_segment, hashf, ruby

SCALE = 0.64
HITBOX = [0.8, 1.0]
KIND = "quadruped"
K = 4
LOOK = ("a teardrop cocoon of see-through smouldering ash with glowing zigzag bands and embers, the Coalarva inside "
        "curled up with its ruby eyes peering out and its abdomen glowing through")

# the shell's profile, bottom to top: (y0, y1, rx, rz)
SHELL = [(0, 2, 2, 1.5), (2, 4, 3, 2.5), (4, 7, 4, 3.5), (7, 11, 5, 4), (11, 15, 5.5, 4.5), (15, 18, 5, 4), (18, 20, 4, 3.5),
         (20, 22, 3, 2.5)]
ASH_ALPHA = 128
# the larva's curled abdomen inside: (cy, cz, r) round segments going down and curling forward
INNER = [(12.5, 1.0, 2.5), (9.5, 1.5, 2.5), (6.8, 0.5, 2.0), (4.8, -1.0, 1.5)]


def zigzag(x, y, z, face):
    """True on the glowing zigzag bands (chevrons pointing down) across the front of the shell."""
    if face != "north" and face not in ("east", "west"):
        return False
    u = x if face == "north" else z
    for yc in (6.5, 11.0):
        v = y - yc - 1.6 * abs((u * 0.45 + 1) % 2 - 1)      # a zigzag line across the shell
        if abs(v) < 0.5:
            return True
    return False


def shell(x, y, z, face, variant, **k):
    if zigzag(x, y, z, face):
        c = fire(0.72, variant)
        return c, c
    h = hashf(x * 1.3, y * 1.3, z * 1.3)
    if h > 0.965:                                   # embers in the ash
        c = fire(0.6 + 0.3 * h, variant)
        return c, c
    base = (74, 66, 64) if variant != "shiny" else (150, 150, 158)
    shade = 0.8 + 0.35 * hashf(x * 0.5, y * 0.7, z * 0.5)
    col = tuple(int(c * shade) for c in base)
    a = ASH_ALPHA + int(40 * hashf(x * 0.4 + 3, y * 0.4, z * 0.4))   # thicker and thinner ash
    return col + (a,), None


def larva_head(x, y, z, face, variant, **k):
    if face == "north":
        for sx in (-1, 1):
            e = ruby(x - sx * 1.3, y - 16.6, 0.9, 0.85, variant)
            if e:
                return e
    return coal(x, y, z, face, variant)


def larva_body(x, y, z, face, variant, **k):
    return coal(x, y, z, face, variant)


def larva_abdomen(x, y, z, face, variant, box=None, **k):
    cy_box = box.lo[1] + box.size[1] / 2
    cy, cz, r = min(INNER, key=lambda s: abs(s[0] - cy_box))
    t_y = 0.5 + 0.5 * math.tanh((z - cz) / max(r, 1e-6))    # brighter towards the front, where it shows
    band = max(0.0, 1 - abs(y - cy) / 0.8)
    return glowing_segment(1 - t_y * 0.5, band, variant)


def build() -> Model:
    m = Model("cinderoon")
    top = m.bone("cinderoon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for y0, y1, rx, rz in SHELL:
        m.round_box(bd, 0, 0, rx, rz, y0, y1, shell, cut=1)
    for sx in (-1, 1):                                           # coal horns on top
        spike(m, bd, (sx * 1.6, 21.5, 0), (sx * 0.5, 1, 0.1), 1, 3, larva_body)
    # the Coalarva inside, curled up
    inner = m.bone("larva", bd, (0, 12, 0))
    m.box(inner, -2, 12.5, -1.5, 2, 15.5, 2, larva_body)        # thorax
    hd = m.bone("head", inner, (0, 15, -0.5))
    m.round_box(hd, 0, -0.8, 2.5, 2, 14.5, 19, larva_head, cut=1)
    for cy, cz, r in INNER:
        m.round_box(inner, 0, cz, r, r, cy - r * 0.6, cy + r * 0.6, larva_abdomen, cut=max(1, round(r * 0.4)))
    return m
