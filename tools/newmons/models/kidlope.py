"""Kidlope, the Kid Pokémon (Grass/Dark; the user's art, artist not named; our name): a chibi black goat-kid with long
rabbit ears, little ridged horns, huge glossy yellow eyes, a grey muzzle, a ruff of leaves round its neck, stubby arms
with grey hooves for hands, and a sprouting leafy sprig of a tail.

Front is -z, y is up. 17 units tall; baseScale 0.5 (0.5 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _lope import P, ear, eye, furry, hoofed, horn, ruff, solid, sprig
from _route import tone

SCALE = 0.5
HITBOX = [0.7, 1.05]
KIND = "biped"
K = 6
HEIGHT = 17
LOOK = ("a chibi black goat-kid with long rabbit ears, little horns, huge yellow eyes, a leafy ruff and a sprouting "
        "leaf tail")


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = eye(p, x - sx * 1.9, y - 11.7, 1.45)
            if e:
                return e, None
    return tone(p["fur"] if y < 14 or face != "up" else p["fur_light"], face), None


def build() -> Model:
    m = Model("kidlope")
    top = m.bone("kidlope", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 0.2, 2.8, 2.4, 3.6, 8.2, furry(), cut=1.0)
    ruff(m, bd, 8.0, 3.4, 9, 1.8)
    hd = m.bone("head", bd, (0, 8.2, 0))
    m.round_box(hd, 0, 0, 4.0, 3.6, 7.8, 14.6, head, cut=1.4)
    m.round_box(hd, 0, -3.1, 1.5, 0.9, 8.8, 10.8, hoofed("grey"), cut=0.5)            # the grey muzzle
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.6, 11.0, 0.6), (sx, -0.2, 0.3), 1.6, 1.8, solid("fur"), tip=0.6)   # cheek tufts
        horn(m, hd, (sx * 2.2, 14.0, 0.4), sx, 4.0, 1.2)
        ear(m, hd, (sx * 1.4, 14.2, 0.8), (sx * 0.28, 1, 0.15), 7.0, 2.8, 1.0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 2.8, 7.0, 0))
        rod(m, a, (sx * 2.6, 7.0, 0), (sx * 5.0, 5.6, -0.8), 1.5, solid("fur"))
        m.round_box(a, sx * 5.2, -1.0, 1.0, 0.9, 4.4, 6.2, hoofed("grey", "z", -1.0), cut=0.4)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.5, 4.2, 0))
        m.round_box(lg, sx * 1.5, 0.0, 1.1, 1.1, 1.2, 4.4, solid("fur"), cut=0.4)
        m.round_box(lg, sx * 1.5, -0.3, 1.2, 1.4, 0.0, 1.4, hoofed("grey", "x", sx * 1.5), cut=0.4)
    tl = m.bone("tail", bd, (0, 5, 2.4))
    sprig(m, tl, (0, 5.0, 2.4), (0, 0.6, 0.8), 2.6)
    return m
