"""Larvorub, the Horn Grub Pokémon (Bug), after the art by @artworks218_ (the art's own name, used with the creator's
permission): a plump lavender-white grub on six white stubby legs, its back banded cream with a yellow spot on each
side and a brown cap at the rear with two thin whiskers. Its dark brown head has two big round cheeks at the front,
huge green eyes with darker four-leaf clover pupils, and two horns, brown at the root with chevroned yellow tips.

Shiny: a navy head with pink eyes.

Front is -z, y is up. 19 units tall to its horn tips; baseScale 0.42 (0.5 m).
"""
from __future__ import annotations

from _boxmodel import Model
from _route import tone
from _scarab import BASE, SHINY, P, clover, eye_colour, horn, solid
from _sense import whisker

SCALE = 0.42
HITBOX = [0.75, 1.2]
KIND = "quadruped"
K = 6
HEIGHT = 19
LOOK = ("a plump lavender-white grub with a cream-banded back, yellow side spots, a brown head with round cheeks, "
        "huge green eyes with clover pupils and two yellow-tipped horns")


def segf(kind):
    """The grub's body segments: lavender below, cream above (brown above on the rear one), yellow side spots."""
    spot = {1: (-1.6, 4.8, "ochre"), 2: (2.6, 6.4, "yellow")}.get(kind)
    split = {1: 6.0, 2: 6.0, 3: 5.4}[kind]

    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "down":
            return p["body_shade"], None
        if spot and face in ("east", "west"):
            sz, sy, key = spot
            if ((z - sz) / 1.0) ** 2 + ((y - sy) / 1.4) ** 2 < 1:
                return tone(p[key], face), None
        if face == "up" or y > split:
            return tone(p["brown"] if kind == 3 else p["cream"], face), None
        return tone(p["body"], face), None
    return s


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 0.25 and y < 5.6:
        return p["brown_dark"], None                                      # the parting between its cheeks
    return tone(p["brown"], face), None


def eyef(sx):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        light = 0.55 if y > 9.0 else 0.0
        if face == "north":
            return eye_colour(p, clover(x - sx * 2.9, y - 7.9, 1.05), light), None
        if face in ("east", "west") and abs(x) > 4.2:
            return eye_colour(p, clover(z + 8.0, y - 7.9, 0.9), light), None
        if face == "up":
            return p["eye_light"], None
        return tone(p["eye"], face), None
    return s


def build() -> Model:
    m = Model("larvorub")
    top = m.bone("larvorub", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, -1.5, 5.0, 2.6, 1.0, 10.0, segf(1), cut=1.6)            # the three body segments
    m.round_box(bd, 0, 2.6, 4.6, 2.2, 1.2, 9.4, segf(2), cut=1.4)
    m.round_box(bd, 0, 6.2, 3.8, 2.0, 1.6, 8.2, segf(3), cut=1.2)
    for sx in (-1, 1):                                                          # two thin whiskers at the back
        whisker(m, bd, (sx * 0.8, 8.0, 7.6), (sx * 2.4, 12.6, 11.0), BASE, SHINY, key="brown_dark", thick=0.25)

    hd = m.bone("head", bd, (0, 5, -4))
    m.round_box(hd, 0, -6.5, 4.2, 2.8, 3.0, 10.4, headf, cut=1.4)              # brown head
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.9, -9.0, 2.0, 1.6, 2.2, 5.6, headf, cut=0.8)    # its round cheeks
        x0, x1 = sorted((sx * 1.2, sx * 4.4))
        m.box(hd, x0, 6.2, -9.9, x1, 9.6, -6.6, eyef(sx))                     # huge green eyes
        horn(m, hd, (sx * 1.8, 9.6, -5.6), (sx * 2.2, 14.0, -5.8), (sx * 3.2, 19.0, -6.8), 1.8, 1.6)

    for sx, side in ((-1, "left"), (1, "right")):                              # six stubby white legs
        for role, z in (("front", -3.4), (None, 1.4), ("back", 5.2)):
            bn = m.bone(f"leg_{role}_{side}", top, (sx * 4.2, 2.4, z)) if role else bd
            m.round_box(bn, sx * 4.4, z, 1.3, 1.2, 0.0, 2.6, solid("cream"), cut=0.6)
    return m
