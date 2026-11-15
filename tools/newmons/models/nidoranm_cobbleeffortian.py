"""The CobbleEffort Nidoran♂ (Fire/Dragon; the user's "Kiruvian" regional art, artist not named): a little charcoal
beast with spiky fur, big ears edged in red, an orange-gold eye under a red mark, small white fangs and a red nose,
red dorsal spines, and a big round magma-red rump with dark patches.

Front is -z, y is up. 15 units tall; baseScale 0.55 (0.5 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _nidoflame import P, claws, earf, eye, patched, plate, solid, spikes
from _route import tone

SCALE = 0.55
HITBOX = [0.9, 0.85]
KIND = "quadruped"
K = 6
HEIGHT = 15
LOOK = ("a little charcoal beast with spiky fur, big red-edged ears, an orange-gold eye under a red mark, small fangs, red "
        "dorsal spines and a big round magma-red rump")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 5.6, y - 7.8, 1.2, -1)
        if c is not None:
            return c, None
        if abs(z + 5.0) < 1.2 and 8.6 < y < 9.6:
            return tone(p["red"], face), p["ember"]                    # the red mark over the eye
    if face == "north" and abs(x) < 0.5 and 6.6 < y < 7.4:
        return p["red"], None                                          # a little red nose
    return patched(spacing=4.0, size=0.6)(x, y, z, face, variant)


def build() -> Model:
    m = Model("nidoranm_cobbleeffortian")
    top = m.bone("nidoranm", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 1))
    m.round_box(bd, 0, 3.2, 3.0, 3.0, 1.6, 2.8, plate(), cut=1.4)                  # the big round red rump, in slices
    m.round_box(bd, 0, 3.2, 3.6, 3.6, 2.6, 7.4, plate(), cut=1.8)
    m.round_box(bd, 0, 3.2, 3.0, 3.0, 7.2, 8.6, plate(), cut=1.4)
    m.round_box(bd, 0, 3.2, 2.0, 2.0, 8.4, 9.2, plate(), cut=0.8)
    m.round_box(bd, 0, -1.0, 2.8, 2.8, 2.0, 7.4, patched(), cut=1.0)               # the dark chest
    for i, (z, h) in enumerate(((0.4, 5.0), (2.4, 6.0), (4.4, 5.4), (6.2, 4.0))):  # red dorsal spines
        spike(m, bd, (0, 8.6, z), (0, 1, 0.5), 1.6, h, solid("red" if i % 2 == 0 else "red_dark"), tip=0.7)
    hd = m.bone("head", bd, (0, 6, -2))
    m.round_box(hd, 0, -4.2, 3.2, 3.0, 4.4, 10.2, headf, cut=1.2)
    m.box(hd, -1.6, 5.0, -8.0, 1.6, 7.6, -6.8, headf)                              # the snout
    for sx in (-1, 1):
        m.box(hd, sx * 0.9 - 0.4, 4.2, -7.8, sx * 0.9 + 0.4, 5.0, -7.0, solid("white"))   # little fangs
    spikes(m, hd, (0, 9.6, -3.4), [(0, 1, -0.4), (0.5, 1, 0.1), (-0.5, 1, 0.1), (0, 0.6, 0.8)], 1.4, 3.0, patched())
    for sx, nm in ((1, "ear_left"), (-1, "ear_right")):                           # big ears, edged in red
        e = m.bone(nm, hd, (sx * 2.2, 9.0, -3.0))
        rod(m, e, (sx * 2.2, 9.4, -3.0), (sx * 5.2, 14.4, -2.4), 3.8, earf(), extend=0.3, t2=1)
        spike(m, e, (sx * 5.0, 14.0, -2.4), (sx * 0.4, 1, 0.2), 1.2, 1.8, solid("red"), tip=0.5)
    for leg, (lx, lz) in (("leg_front_left", (1.8, -1.6)), ("leg_front_right", (-1.8, -1.6)),
                          ("leg_back_left", (2.4, 4.0)), ("leg_back_right", (-2.4, 4.0))):
        lg = m.bone(leg, top, (lx, 3.0, lz))
        m.round_box(lg, lx, lz, 1.2, 1.3, 0, 3.4, patched(spacing=2.0, size=0.5, seed=lx), cut=0.5)
        claws(m, lg, lx, 0.4, lz - 1.2, 3, 0.6, 1.0, 0.6)
    return m
