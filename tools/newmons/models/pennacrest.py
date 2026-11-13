"""Pennacrest, the Crested Nest Pokémon (Normal/Flying), Pinnant evolved: a great bird that broods over the nest. Its
long white neck has a red stripe down each side and a red back, and its head wears a broad red crest that sweeps out
to both sides like the brim of a hat, over big grey eyes with dark marks beneath them and a yellow beak; a black and
grey plume trails from the back of its head. A spiky white ruff marked with two black chevrons covers its chest,
brown wings with red coverts fold over its red-brown body, and four long streamers banded black and grey, tipped red,
arch up behind it.

Front is -z, y is up. 38 units tall to the crest; baseScale 0.8 (1.9 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _pinbird import P, beakf, eye, feetf, redf, streamer, whitef
from _route import tone

SCALE = 0.8
HITBOX = [1.75, 2.4]
KIND = "biped"
K = 4
HEIGHT = 38
LOOK = ("a great brooding bird with a long white neck striped red, a broad hat-brim red crest, big grey eyes with dark "
        "marks, a spiky white chest ruff with black chevrons, folded brown wings and four long banded streamers")


def neckf(cz):
    """White neck, red down the back and along the back half of each side."""
    def s(x, y, z, face, variant, **k):
        if face == "south" or (face in ("east", "west") and z > cz + 0.1):
            return redf(x, y, z, face, variant)
        return whitef(x, y, z, face, variant)
    return s


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    for sx in (-1, 1):
        c = eye(face, x, y, sx * 1.35, 33.6, 0.95, variant)
        if c is not None:
            return c, None
        if face == "north" and abs(x - sx * 1.35) < 0.28 and 31.4 < y < 32.7:
            return p["black"], None                                       # the dark marks under its eyes
    if face == "south" or (face in ("east", "west") and z > -4.4):
        return redf(x, y, z, face, variant)
    return whitef(x, y, z, face, variant)


def ruff(x, y, z, face, variant, **k):
    """The white chest ruff with two black chevrons."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx = x - sx * 2.0
            if abs(dx) < 1.5 and abs((y - 14.6) - (-0.6 * dx * sx)) < 0.36:
                return p["black"], None
    return whitef(x, y, z, face, variant)


def foldf(x, y, z, face, variant, **k):
    """A folded wing: red coverts at the top front, brown flight feathers with pale edges behind."""
    p = P(variant)
    if y > 13.5 and z < 2.5:
        return tone(p["red"], face), None
    if face in ("east", "west") and (z % 2.2) < 0.35 and z > 2:
        return p["brown_light"], None
    return tone(p["brown"], face), None


def build() -> Model:
    m = Model("pennacrest")
    top = m.bone("pennacrest", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 1))
    m.round_box(bd, 0, 2, 6.2, 7.2, 3.5, 17, redf, cut=2.6)                 # broad brooding body
    m.round_box(bd, 0, -3.6, 4.6, 2.6, 10.5, 19, ruff, cut=1.4)             # chest ruff
    for i, x in enumerate((-3.8, -2.3, -0.8, 0.8, 2.3, 3.8)):              # its spiky lower edge
        spike(m, bd, (x, 11.2, -5.4), (x * 0.18, -1, -0.45), 1.4, 2.4 + (i % 2) * 0.8, whitef)
    for sx in (-1, 1):
        for y in (13, 16):
            spike(m, bd, (sx * 4.4, y, -4.2), (sx, -0.3, -0.5), 1.3, 2.2, whitef)
    nk = m.bone("neck", bd, (0, 18, -3.4))
    for i in range(7):                                                      # the long white neck, striped red
        y0 = 17.5 + i * 2.1
        cz = -3.3 - i * 0.22
        m.round_box(nk, 0, cz, 2.3, 2.1, y0, y0 + 2.4, neckf(cz), cut=0.8)
    hd = m.bone("head", nk, (0, 31, -4.6))
    m.round_box(hd, 0, -5.0, 2.8, 3.2, 30.4, 36.0, headf, cut=1.0)
    rod(m, hd, (0, 33.0, -8.0), (0, 32.0, -10.6), 1.6, beakf, extend=0.2)     # beak
    rod(m, hd, (0, 32.2, -10.4), (0, 31.3, -10.7), 1.0, beakf, extend=0.1)
    m.box(hd, -2.7, 35.6, -7.6, 2.7, 37.0, -2.6, redf)                        # the broad crest
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 2.4, sx * 8.2))
        m.box(hd, x0, 35.6, -7.0, x1, 36.8, -3.0, redf, rotation=(0, 0, -sx * 14), pivot=(sx * 2.4, 36.2, -5.0))
    streamer(m, hd, [(0, 36.2, -2.8), (0.5, 35.2, 0.6), (1.1, 31.5, 2.6), (1.5, 26.5, 3.4)], 2.2, 1.4, period=2.0)
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):                   # folded wings
        w = m.bone(nm, bd, (sx * 6.6, 16, 1))
        x0, x1 = sorted((sx * 5.6, sx * 7.2))
        m.box(w, x0, 6.5, -4.0, x1, 16.8, 10.0, foldf)
    tl = m.bone("tail", bd, (0, 11, 7.5))
    rod(m, tl, (0, 11, 7), (0, 13.4, 10.6), 5, redf, extend=0.3, t2=2.2)      # red tail coverts
    for sx, j in ((-1, 0.5), (-1, 1.5), (1, 0.5), (1, 1.5)):               # four long streamers fanning out behind
        k = sx * j
        streamer(m, tl, [(k * 1.2, 11.5, 8.5), (k * 2.4, 14.5, 13.5), (k * 3.8, 18.5 - j, 19), (k * 5.0, 21 - j * 1.5, 24),
                         (k * 5.8, 21.5 - j * 2.5, 28.5)], 2.1, 1.2, tip="red", period=2.4)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, top, (sx * 3, 6, 1))
        rod(m, lg, (sx * 3, 7, 1), (sx * 3.2, 0.9, 0.4), 1.6, feetf, extend=0.1)
        for dx, dz in ((-1.1, -2.6), (1.1, -2.6), (0, 1.3)):                  # talons
            rod(m, lg, (sx * 3.2, 0.7, 0.4), (sx * 3.2 + dx, 0.25, 0.4 + dz), 0.8, feetf, extend=0.1)
    return m
