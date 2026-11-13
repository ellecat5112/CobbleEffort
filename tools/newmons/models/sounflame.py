"""Sounflame, the Ember Bat Pokémon (Fire/Flying), the fire starter, after the art of the A. Fakemon fanpage (the art's
own name): a little red bat with a round head, two huge pointed ears (yellow inside), a yellow mask running from a
flame-shaped crest down to a beaky muzzle, magenta eyes, a thin body, little clawed feet and wings whose membranes are
yellow-orange flames.

Shiny: deep blue with pale cyan flames.

Front is -z, y is up. 26 units tall to its ear tips; baseScale 0.25 (0.4 m).
"""
from __future__ import annotations

from _afake import round_eye
from _boxmodel import Model, mix, rod, spike
from _firebat import P, membrane, solid, tongues
from _route import tone

SCALE = 0.25
HITBOX = [1.4, 1.6]
KIND = "floater"
K = 6
HEIGHT = 26
LOOK = ("a little red bat with huge pointed ears, a yellow mask and beaky muzzle, magenta eyes and wings of "
        "yellow-orange flame")
ANIM = {"wing_flap": 14}


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = round_eye(x - sx * 1.8, y - 13.4, 0.95, p, "pink", ry=1.1, look=(-sx * 0.1, 0))
            if e:
                return e, None
        if abs(x) < 1.0 + max(0.0, 12.4 - y) * 0.5 or (x > 0.6 and 12.2 < y < 14.8 and x < 3.0):
            return tone(p["yellow"], face), None                              # the yellow mask
    if face == "up" and abs(x) < 0.9:
        return tone(p["yellow"], face), None
    return tone(p["red"], face), None


def earf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    from _route import along
    t = along(z, box)
    cx = box.lo[0] + box.size[0] / 2
    if face in ("up", "down") and 0.12 < t < 0.8 and abs(x - cx) < 1.0 * (1 - t):
        return p["yellow"], None                                              # the yellow inside of its ears
    return tone(p["red"], face), None


def wing_colour(p, u, y, top, bottom):
    t = (top - y) / max(1.0, top - bottom)
    return mix(p["yellow_light"], p["orange"], min(1.0, t * 1.3))


def build() -> Model:
    m = Model("sounflame")
    top = m.bone("sounflame", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    rod(m, bd, (0, 10.0, 0.0), (0, 4.0, 1.0), 2.6, solid("red"), extend=0.5)   # its thin body
    m.round_box(bd, 0, 0.6, 1.6, 1.4, 4.0, 7.0, solid("red_light"), cut=0.6)
    for sx in (-1, 1):                                                         # little legs with grey claws
        rod(m, bd, (sx * 0.8, 4.6, 1.0), (sx * 1.6, 1.6, 0.4), 1.2, solid("red"), extend=0.3)
        spike(m, bd, (sx * 1.6, 1.6, 0.4), (0, -0.4, -1), 1.0, 2.2, solid("claw"))

    hd = m.bone("head", bd, (0, 10, 0))
    m.round_box(hd, 0, 0.0, 3.4, 3.0, 9.5, 16.0, headf, cut=1.2)
    m.box(hd, -1.6, 10.0, -4.4, 1.6, 12.4, -2.8, solid("yellow"))              # the beaky muzzle
    spike(m, hd, (0, 10.4, -4.2), (0, -1, -0.5), 1.4, 1.6, solid("yellow"))
    spike(m, hd, (0.3, 15.4, -2.4), (0.2, 1, 0.1), 1.8, 3.0, solid("yellow"), tip=0.9)   # its flame crest
    for sx in (-1, 1):
        rod(m, hd, (sx * 2.2, 15.0, 0.0), (sx * 7.5, 25.0, 1.0), 3.6, earf, extend=0.4, t2=1.4)   # huge ears

    for sx, side in ((-1, "left"), (1, "right")):
        w = m.bone(f"wing_{side}", bd, (sx * 1.5, 8, 0))
        rod(m, w, (sx * 1.5, 8.0, 0.0), (sx * 6.0, 10.0, 0.0), 1.2, solid("red"), extend=0.3)
        rod(m, w, (sx * 6.0, 10.0, 0.0), (sx * 11.0, 7.0, 0.0), 1.2, solid("red"), extend=0.3)
        for tip in ((sx * 14.0, 9.6, 0.0), (sx * 15.4, 7.0, 0.0), (sx * 13.6, 4.4, 0.0)):   # finger claws
            rod(m, w, (sx * 11.0, 7.0, 0.0), tip, 1.0, solid("red_dark"), extend=0.2)
        x0, x1 = sorted((sx * 1.5, sx * 16.0))
        m.box(w, x0, -4.0, 0.3, x1, 10.0, 0.3, membrane(
            1.5, 16.0, lambda u: 9.6 if u < 0.65 else 9.6 - (u - 0.65) / 0.35 * 3.5,
            lambda u: 3.5 - 1.5 * u - tongues(u, [(0.2, 5, 0.12), (0.45, 6, 0.13), (0.7, 5.5, 0.12), (0.93, 4, 0.1)]),
            wing_colour))
    return m
