"""The CobbleEffort Nidorino (Fire/Dragon; the user's "Kiruvian" regional art, artist not named): a charcoal beast with
spiky head fur, a big round ear with a peach inside, a translucent quartz horn on its brow, an orange-gold eye, an
open pink mouth with white fangs, a dark-red chest and belly plate, glowing magma patches on its flanks and legs, and
white claws.

Front is -z, y is up. 20 units tall; baseScale 0.75 (0.95 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _nidoflame import P, claws, crystal, earf, eye, patched, plate, solid, spikes
from _route import tone

SCALE = 0.75
HITBOX = [1.4, 1.3]
KIND = "quadruped"
K = 5
HEIGHT = 20
LOOK = ("a charcoal beast with spiky head fur, a big round peach-lined ear, a translucent quartz horn, an orange-gold "
        "eye, an open mouth with white fangs, a dark-red chest plate and glowing magma patches on its flanks and legs")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 7.2, y - 12.2, 1.3, -1)
        if c is not None:
            return c, None
    return patched(spacing=4.0, size=0.6, seed=2)(x, y, z, face, variant)


def mouthf(x, y, z, face, variant, **k):
    """The open mouth: pink inside, white fangs along its edge."""
    p = P(variant)
    if face in ("up", "down") or (face == "north" and abs(x) < 1.4):
        return p["mouth"], None
    return tone(p["char"], face), None


def build() -> Model:
    m = Model("nidorino_cobbleeffortian")
    top = m.bone("nidorino", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 1))
    m.round_box(bd, 0, 2.0, 4.0, 7.0, 5.0, 11.0, patched(seed=1), cut=2.0)          # the body
    m.round_box(bd, 0, -2.6, 3.0, 2.4, 4.6, 9.6, plate("red_dark", "red_dark"), cut=1.0)   # the dark-red chest plate
    for i, z in enumerate((-1.0, 1.6, 4.2, 6.8)):                                      # dark dorsal spines
        spike(m, bd, (0, 10.6, z), (0, 1, 0.6), 1.6, 3.6 - 0.4 * i, solid("char_dark"), tip=0.6)
    hd = m.bone("head", bd, (0, 10, -4))
    m.round_box(hd, 0, -6.4, 3.0, 3.0, 9.4, 15.4, headf, cut=1.2)
    m.box(hd, -2.0, 11.0, -11.0, 2.0, 13.4, -8.8, headf)                               # the upper snout
    jw = m.bone("jaw", hd, (0, 10.4, -7))
    m.box(jw, -1.8, 9.4, -10.4, 1.8, 10.6, -8.0, mouthf, rotation=(-14, 0, 0), pivot=(0, 10.4, -8.0))  # mouth open
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.2, 11.2, -10.6), (0, -1, -0.15), 0.8, 1.4, solid("white"), tip=0.3)    # fangs
    spike(m, hd, (0, 14.6, -8.4), (0, 1, -0.55), 2.6, 5.4, crystal(), tip=0.6)  # the quartz horn
    spikes(m, hd, (0, 15.2, -5.0), [(0, 1, 0.4), (0.6, 1, 0.6), (-0.6, 1, 0.6), (0, 0.5, 1)], 1.6, 3.4, patched())
    for sx, nm in ((1, "ear_left"), (-1, "ear_right")):                               # big round ears
        e = m.bone(nm, hd, (sx * 2.6, 14.0, -4.0))
        rod(m, e, (sx * 2.6, 14.0, -4.0), (sx * 6.0, 18.0, -2.4), 4.6, earf("char", "inner"), extend=0.3, t2=1)
    for leg, (lx, lz) in (("leg_front_left", (2.4, -2.6)), ("leg_front_right", (-2.4, -2.6)),
                          ("leg_back_left", (2.8, 6.2)), ("leg_back_right", (-2.8, 6.2))):
        lg = m.bone(leg, top, (lx, 5.0, lz))
        m.round_box(lg, lx, lz, 1.5, 1.6, 0, 5.6, patched(spacing=2.4, size=0.6, seed=lx + lz), cut=0.6)
        claws(m, lg, lx, 0.5, lz - 1.5, 3, 0.7, 1.2, 0.7)
    tl = m.bone("tail", bd, (0, 9, 8.6))
    rod(m, tl, (0, 9, 8.6), (0, 11.5, 12.0), 1.6, patched(), extend=0.3, t2=0.8)
    return m
