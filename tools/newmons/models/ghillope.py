"""Ghillope, the Ghillie Pokémon (Grass/Dark; the user's art, artist not named; our name): a tall, broad goat-rabbit
hunter of the deep woods in a ghillie cloak of leaves bound with crossing vines: a mantle of leaves over its shoulders,
a leafy tunic with a ragged hem, vine bands round its arms and legs, huge grey hands, hooves, long upright ears, ridged
horns, a grey muzzle with a little goatee, and narrow yellow eyes.

Front is -z, y is up. 41 units tall; baseScale 0.7 (1.8 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _lope import P, ear, eye, furry, hoofed, horn, ruff, solid
from _route import tone

SCALE = 0.7
HITBOX = [1.3, 2.5]
KIND = "biped"
K = 3
HEIGHT = 41
LOOK = ("a tall goat-rabbit hunter in a ghillie cloak of leaves bound with crossing vines, with long upright ears, horns, "
        "narrow yellow eyes and huge grey hands")


def cloak(x, y, z, face, variant, **k):
    """Leaves layered like scales, a vine belt and two vines crossing the chest."""
    p = P(variant)
    if face not in ("up", "down") and abs(y - 15.6) < 0.5:
        return tone(p["vine"], face), None
    if face == "north" and y > 16.4 and abs(abs(x) - abs(y - 21.0) * 0.95) < 0.5:
        return tone(p["vine"], face), None
    row = int((y + 30) / 1.4)
    col = int((x + z + 30 + (row % 2) * 0.9) / 1.8)
    return tone(p["leaf_dark"] if (row + col) % 3 else p["leaf"], face), None


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = eye(p, x - sx * 1.3, y - 29.4, 0.8, lid=0.25, slant=-sx * 0.5)
            if e:
                return e, None
        if abs(x) < 0.35 and y > 28.6:
            return tone(p["grey_dark"], face), None                     # a grey stripe down the face
    return tone(p["fur"], face), None


def build() -> Model:
    m = Model("ghillope")
    top = m.bone("ghillope", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 15, 0))
    m.round_box(bd, 0, 0.3, 4.6, 3.2, 13.0, 25.2, cloak, cut=1.5)
    m.round_box(bd, 0, 0.3, 5.0, 3.6, 10.2, 14.0, cloak, cut=1.6)                     # the tunic's skirt
    ruff(m, bd, 10.8, 5.0, 14, 2.0, shader=solid("leaf_dark"), droop=2.2, phase=0.5)  # its ragged hem
    ruff(m, bd, 24.8, 5.2, 12, 2.6, droop=0.15)                                       # the leafy mantle
    hd = m.bone("head", bd, (0, 25.5, 0))
    m.round_box(hd, 0, 0, 2.6, 2.8, 25.4, 31.6, head, cut=1.0)
    m.round_box(hd, 0, -3.0, 1.4, 1.0, 25.8, 28.4, hoofed("grey"), cut=0.4)           # the long muzzle
    spike(m, hd, (0, 25.8, -3.2), (0, -1, -0.3), 1.0, 1.8, solid("fur"), tip=0.5)      # goatee
    for sx in (-1, 1):
        horn(m, hd, (sx * 1.8, 31.0, 0.6), sx, 5.0, 1.4)
        ear(m, hd, (sx * 1.0, 31.4, 0.8), (sx * 0.3, 1, 0.1), 9.0, 3.0, 1.0)
        spike(m, hd, (sx * 2.5, 27.6, 0.2), (sx, -0.3, 0.3), 1.4, 1.8, solid("fur"), tip=0.6)   # cheek tufts
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 5.2, 23.5, 0))
        rod(m, a, (sx * 5.2, 23.5, 0), (sx * 6.6, 17.5, -0.4), 2.8, furry(bands=(19.4, 21.0)))
        rod(m, a, (sx * 6.6, 17.5, -0.4), (sx * 7.0, 12.6, -1.2), 2.6, furry(bands=(15.6, 14.0)))
        m.round_box(a, sx * 7.0, -1.4, 1.9, 1.5, 9.0, 12.8, hoofed("grey", "z", -1.4), cut=0.6)
        for dz in (-2.6, -1.8, -1.0):                                                  # big fingers
            m.box(a, sx * 7.0 - 1.0, 8.0, dz - 0.35, sx * 7.0 + 1.0, 9.2, dz + 0.35, solid("grey"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 13.6, 0))
        rod(m, lg, (sx * 2.6, 13.6, 0), (sx * 3.2, 8.0, -0.6), 2.8, solid("fur"))
        rod(m, lg, (sx * 3.2, 8.0, -0.6), (sx * 3.4, 2.4, 0.2), 2.4, furry(bands=(4.4,)))
        m.round_box(lg, sx * 3.4, -0.6, 1.8, 2.2, 0.0, 2.4, hoofed("grey", "x", sx * 3.4), cut=0.6)
    return m
