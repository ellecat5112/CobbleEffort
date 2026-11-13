"""Pinnant, the Pennant Bird Pokémon (Normal/Flying), Pinlet evolved: a red-brown bird with a white face and bib (a
black chevron on it), a red hood swept back into a crest, big grey eyes, a hooked yellow beak, broad brown wings with
red coverts held half open, two long tail streamers banded black and grey that trail behind it like pennants, and
yellow feet. It brings berries back to the nest for the chicks.

Front is -z, y is up. 25 units tall to the crest; baseScale 0.55 (0.85 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _pinbird import P, beakf, bodyf, eye, feetf, redf, streamer, whitef, wingf

SCALE = 0.55
HITBOX = [1.45, 1.55]
KIND = "biped"
K = 4
HEIGHT = 25
LOOK = ("a red-brown bird with a white face and bib, a swept-back red crest, big grey eyes, a hooked yellow beak, "
        "half-open brown wings and two long black-and-grey banded tail streamers")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    for sx in (-1, 1):
        c = eye(face, x, y, sx * 1.3, 19.7, 0.95, variant)
        if c is not None:
            return c, None
    if face == "up" or y > 21.0 or face == "south" or (face in ("east", "west") and (y > 20.2 or z > 0.6)):
        return redf(x, y, z, face, variant)                                # the red hood
    return whitef(x, y, z, face, variant)


def build() -> Model:
    m = Model("pinnant")
    top = m.bone("pinnant", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0.5, 3.8, 3.6, 7, 17, bodyf(17, 2.7, chevrons=((0, 14.2),)), cut=1.5)   # white bib, chevron
    hd = m.bone("head", bd, (0, 17, -0.5))
    m.round_box(hd, 0, -0.8, 3.0, 2.8, 16.5, 22.5, headf, cut=1.1)
    rod(m, hd, (0, 19.4, -3.4), (0, 18.7, -5.3), 1.3, beakf, extend=0.2)        # hooked beak
    rod(m, hd, (0, 18.8, -5.1), (0, 18.0, -5.4), 0.8, beakf, extend=0.1)
    rod(m, hd, (0, 22.0, -1.0), (0, 24.4, 2.6), 2.2, redf, extend=0.2, t2=1.2)  # swept-back crest
    rod(m, hd, (0, 21.2, 0.8), (0, 22.6, 3.6), 1.4, redf, extend=0.2, t2=0.8)
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):                       # broad half-open wings
        w = m.bone(nm, bd, (sx * 3.6, 15.5, 0))
        x0, x1 = sx * 3.4, sx * 12.5
        m.box(w, min(x0, x1), 15.5, -2.2, max(x0, x1), 15.5, 5.2, wingf(x0, x1, -2.2, 5.2, feathers=5),
              rotation=(0, 0, -sx * 28), pivot=(sx * 3.5, 15.5, 0))
    tl = m.bone("tail", bd, (0, 9, 3))
    rod(m, tl, (0, 9.4, 2.8), (0, 8.4, 6.4), 2.6, redf, extend=0.2, t2=0.8)     # short tail
    for sx in (-1, 1):                                                          # two long pennant streamers
        streamer(m, tl, [(sx * 0.7, 8.6, 3.4), (sx * 1.0, 5.4, 6.2), (sx * 1.2, 2.6, 10), (sx * 1.3, 1.2, 14.5),
                         (sx * 1.4, 0.9, 18.5)], 1.5, 1.0, period=2.2)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, top, (sx * 1.8, 7.5, 0))
        m.round_box(lg, sx * 1.8, 0, 1.3, 1.4, 4.6, 8.5, redf, cut=0.5)       # feathered thighs
        rod(m, lg, (sx * 1.8, 5.0, 0), (sx * 2.0, 0.8, -0.4), 1.1, feetf, extend=0.1)
        for dx, dz in ((-0.8, -2.0), (0.8, -2.0), (0, 1.0)):                    # talons
            rod(m, lg, (sx * 2.0, 0.6, -0.4), (sx * 2.0 + dx, 0.2, dz - 0.4), 0.6, feetf, extend=0.1)
    return m
