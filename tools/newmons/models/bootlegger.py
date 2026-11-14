"""Bootlegger, the Smuggler Pokémon (Dark), a Liquor Meadows Pokémon (the user's design): a sneaky little raccoon kit
with a black bandit mask and shining eyes, a flat cap pulled low, a ringed tail and a ceramic jug tied on its back.

Shiny: a ginger kit.

Front is -z, y is up. 13 units tall; baseScale 0.45 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _raccoon import P, SHINY, jug, maskface, ramp, ringtail, solid  # noqa: F401

SCALE = 0.45
HITBOX = [0.7, 0.75]
KIND = "quadruped"
K = 6
HEIGHT = 13
LOOK = "a sneaky raccoon kit with a bandit mask, a flat cap, a ringed tail and a ceramic jug on its back"


def build() -> Model:
    m = Model("bootlegger")
    top = m.bone("bootlegger", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, 0.6, 2.6, 4.4, 2.8, 7.6, solid("coon"), cut=0.9)
    jug(m, bd, 0.0, 7.4, 1.4, 0.9)                                            # the jug on its back
    hd = m.bone("head", bd, (0, 7, -4))
    m.round_box(hd, 0, -5.0, 2.6, 2.2, 5.6, 10.0, maskface(0.0, 8.2), cut=0.8)
    m.round_box(hd, 0, -7.4, 0.9, 0.7, 6.0, 7.4, solid("coon_light"), cut=0.3)
    m.box(hd, -0.4, 7.0, -8.2, 0.4, 7.6, -7.8, solid("black"))
    m.round_box(hd, 0, -5.2, 2.8, 2.6, 9.8, 11.0, solid("hat"), cut=0.9)       # flat cap
    m.box(hd, -2.0, 9.8, -8.4, 2.0, 10.3, -7.0, solid("hat"))                  # its peak
    for sx in (-1, 1):
        m.round_box(hd, sx * 2.0, -4.6, 0.7, 0.5, 10.6, 12.0, solid("coon_dark"), cut=0.3)   # ears poking out
    tl = m.bone("tail", bd, (0, 6, 4.4))
    ringtail(m, tl, (0, 6.0, 4.6), (0, 9.4, 10.4), 1.8)
    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -2.6), ("back", 3.0)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 1.6, 3.2, z))
            m.round_box(lb, sx * 1.6, z, 0.8, 0.8, 0.0, 3.4, solid("coon_dark"), cut=0.3)
    return m
