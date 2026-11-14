"""Shadelope, the Brooding Pokémon (Grass/Dark; the user's art, artist not named; our name): Kidlope grown into a lanky
teen that stands upright: shaggy black bangs hide one eye, the other stares out half-lidded and yellow; one ear stands up
and the other flops; a leafy scarf with dangling vines, green bands on its arms, big grey hands, a pale belly, hooves,
and a long vine tail ending in three leaves.

Front is -z, y is up. 33 units tall; baseScale 0.55 (1.1 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod, spike
from _lope import P, ear, eye, furry, hoofed, horn, ruff, solid, sprig
from _route import tone

SCALE = 0.55
HITBOX = [0.9, 2.0]
KIND = "biped"
K = 4
HEIGHT = 33
LOOK = ("a lanky black goat-rabbit with bangs over one eye, one floppy ear, a leafy scarf with dangling vines, green arm "
        "bands and a long vine tail")


def torso(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y < 15.5 and abs(x) < 1.8 - (15.5 - y) * 0.1:
        return tone(p["grey"], face), None                            # the pale belly
    return tone(p["fur"], face), None


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        e = eye(p, x - 1.2, y - 23.0, 0.95, lid=0.3)
        if e:
            return e, None
    return tone(p["fur"], face), None


def bangs(x, y, z, face, variant, **k):
    """Shaggy black bangs over its right eye: cut out below a zigzag."""
    p = P(variant)
    edge = 21.4 + 0.9 * abs(((x + 4) * 0.9) % 2 - 1) + (x + 2.8) * 0.15
    if y < edge:
        return (0, 0, 0, 0), None
    return tone(p["fur_light"] if int((x + 4) * 1.2) % 3 == 0 else p["fur"], face), None


def build() -> Model:
    m = Model("shadelope")
    top = m.bone("shadelope", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 13, 0))
    m.round_box(bd, 0, 0.2, 3.2, 2.4, 11.0, 19.2, torso, cut=1.1)
    ruff(m, bd, 19.0, 3.9, 10, 2.2)                                   # the leafy scarf
    for sx in (-1, 1):                                                # its dangling vines
        chain(m, bd, [(sx * 1.4, 18.6, -2.6), (sx * 1.7, 16.0, -3.0), (sx * 1.5, 14.2, -2.9)], [0.9, 0.9], solid("vine"))
        for d in ((-0.7, -1, -0.3), (0.7, -1, -0.3), (0, -1, -0.6)):
            spike(m, bd, (sx * 1.5, 14.2, -2.9), d, 1.0, 1.6, solid("leaf_light"), tip=0.5)
    hd = m.bone("head", bd, (0, 19.5, 0))
    m.round_box(hd, 0, 0, 2.7, 2.6, 19.4, 25.2, head, cut=1.0)
    m.round_box(hd, 0, -2.9, 1.3, 0.8, 19.8, 22.0, hoofed("grey"), cut=0.4)          # the muzzle
    m.box(hd, -2.9, 20.6, -2.9, 0.8, 25.6, -2.9, bangs)                               # bangs over one eye
    spike(m, hd, (-0.6, 25.0, -1.4), (-0.4, 0.4, -1), 2.4, 2.4, solid("fur"), tip=1.0)
    for sx in (-1, 1):
        horn(m, hd, (sx * 1.7, 25.0, 0.4), sx, 4.2, 1.2)
    ear(m, hd, (1.0, 25.0, 0.6), (0.22, 1, 0.2), 7.5, 2.6, 1.0)                       # one ear up...
    ear(m, hd, (-1.0, 25.0, 0.6), (-1, 0.12, 0.45), 6.4, 2.6, 1.0)                    # ...one flopped
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 3.4, 18.4, 0))
        rod(m, a, (sx * 3.4, 18.4, 0), (sx * 4.6, 14.0, -0.4), 1.8, furry())
        rod(m, a, (sx * 4.6, 14.0, -0.4), (sx * 5.0, 10.8, -1.4), 1.8, furry(bands=(12.9,)))
        m.round_box(a, sx * 5.0, -1.6, 1.4, 1.2, 8.0, 11.0, hoofed("grey", "z", -1.6), cut=0.5)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 12.0, 0))
        rod(m, lg, (sx * 1.8, 12.0, 0), (sx * 2.2, 7.0, -0.6), 2.2, solid("fur"))
        rod(m, lg, (sx * 2.2, 7.0, -0.6), (sx * 2.4, 2.0, 0.2), 1.8, solid("fur"))
        m.round_box(lg, sx * 2.4, -0.4, 1.4, 1.8, 0.0, 1.8, hoofed("grey", "x", sx * 2.4), cut=0.5)
    tl = m.bone("tail", bd, (0, 12, 2.2))
    chain(m, tl, [(0, 12.0, 2.2), (1.2, 13.6, 5.2), (2.4, 16.8, 6.6), (2.8, 19.4, 6.2)], [0.9, 0.9, 0.9], solid("vine"))
    sprig(m, tl, (2.8, 19.4, 6.2), (0.1, 1, -0.1), 0.6)
    return m
