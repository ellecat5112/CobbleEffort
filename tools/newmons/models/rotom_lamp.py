"""Lamp Rotom (Electric/Fairy), after the user's Rotom doodle sheet (artist not named): Rotom inside a table lamp.
A glowing yellow bulb whose lens eyes peer out from under a pale grey shade, a dark stand and base, a pull cord,
and a soft cone of yellow light shining down from it.

Front is -z, y is up. 28 units tall; about 1.0 block.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _rotomform import ball, face_on, palette, solid

P = palette({"aura": (250, 230, 110), "aura_light": (255, 250, 210), "bulb": (252, 236, 130), "shade": (214, 216, 224),
             "beam": (255, 240, 150, 90), "iris": (240, 160, 60)}, {"bulb": (180, 240, 255), "beam": (170, 230, 255, 90)})
HEIGHT = 28
SCALE = round(1.0 * 16 / HEIGHT, 3)
HITBOX = [0.8, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a table lamp whose glowing yellow bulb peers out with lens eyes under a pale shade, shining a cone of light"


def bulb(x, y, z, face, variant, **k):
    out = face_on(P, (0, 13, -3.4), eyes=[(-1.2, 0.4, 1.0), (1.2, 0.4, 1.0)], mouth=(0, -1.2, 1.6, 0.6, 3), base="bulb")(
        x, y, z, face=face, variant=variant)
    c = out[0]
    return c, (out[1] or c)


def beam(x, y, z, face, variant, **k):
    c = P(variant)["beam"]
    return c, c[:3]


def build() -> Model:
    m = Model("rotom_lamp")
    top = m.bone("rotom_lamp", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 4.5, 4.5, 0, 1.6, solid(P, "charcoal"), cut=1.4)            # base
    rod(m, bd, (0, 1.6, 2.5), (0, 10, 2.5), 1.2, solid(P, "charcoal"), extend=0.3)   # stand
    hd = m.bone("head", bd, (0, 13, 0))
    ball(m, hd, 0, 13, 0, 3.4, bulb)                                                  # the glowing bulb (its face)
    for i, (r, y0) in enumerate([(5.2, 15), (4.4, 17), (3.6, 19), (2.8, 21)]):       # the shade
        m.round_box(hd, 0, 0, r, r, y0, y0 + 2, solid(P, "shade"), cut=max(0.8, r * 0.35))
    rod(m, hd, (3, 15, -1), (3.2, 10, -1.5), 0.4, solid(P, "grey_dark"), extend=0.1)  # pull cord
    m.round_box(hd, 3.2, -1.5, 0.5, 0.5, 9.2, 10.2, solid(P, "grey"), cut=0.2)
    for i, r in enumerate((3.6, 4.6, 5.6)):                                           # a soft cone of light below the bulb
        m.round_box(bd, 0, -1, r, r, 7.2 - i * 2.4, 9.6 - i * 2.4, beam, cut=max(0.8, r * 0.35))
    return m
