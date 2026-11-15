"""Onychydra, the Velvet Worm Pokémon (Bug/Dragon; after the art of the user's friend on r/fakemon, signed "sno", shared
with permission; our name): a great hunched worm-dragon of red-orange rings joined by glossy cyan jelly bands, yellow
spots along its back, its rearing neck fronted by a huge cyan water sac over a blue throat, more sacs on its thick
legs, a black underside, dark-red lobed toes and a segmented tail ending in a grey spike. A red hood with a black band
over a round orange eye disc, a hooked grey beak and a cyan tongue.

Front is -z, y is up. 38 units tall; baseScale 1.0 (2.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _scarab import slab_xy
from _velvet import P, eye_disc, jelly, segf, solid, tip_spike, toes
from _route import tone

SCALE = 1.0
HITBOX = [2.4, 2.3]
KIND = "quadruped"
K = 3
HEIGHT = 38
ANIM = {"leg_amp": 14}
LOOK = ("a great hunched worm-dragon of red-orange rings joined by glossy cyan jelly bands, a rearing neck fronted by a "
        "huge cyan water sac, sacs on its thick legs, dark-red lobed toes, a segmented tail with a grey spike, a red hood "
        "with a black band, round orange eye discs and a hooked grey beak")


def hoodf(x, y, z, face, variant, **k):
    p = P(variant)
    if face != "down" and abs(y - (34.2 - 0.25 * (z + 8))) < 0.9 and face != "north":
        return tone(p["black"], face), None                         # the black band over the hood
    if face in ("east", "west"):
        c = eye_disc(p, z + 12.6, y - 31.0, 2.6)
        if c is not None:
            return c, None
    if face == "north":
        for sx in (-1, 1):
            c = eye_disc(p, x - sx * 2.6, y - 31.0, 2.0)
            if c is not None:
                return c, None
        return tone(p["orange"], face), None                         # the orange face disc
    return segf(seed=4)(x, y, z, face, variant, box=k.get("box"))


def build() -> Model:
    m = Model("onychydra")
    top = m.bone("onychydra", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 13, 4))
    # the body: a hunched shoulder ring and three body rings falling back to the hips
    slab_xy(m, bd, 0, 16, 8.5, 8.0, -7, 1, segf(seed=1, belly="black"))
    slab_xy(m, bd, 0, 14, 7.6, 7.0, 1, 7, segf(seed=2, belly="black"))
    slab_xy(m, bd, 0, 12, 6.5, 6.0, 7, 13, segf(seed=3, belly="black"))
    slab_xy(m, bd, 0, 11, 6.0, 5.5, 13, 18, segf(seed=5, belly="black"))
    m.box(bd, -5, 5, -4, 5, 7, 16, solid("black"))                   # the black underside
    for sx in (-1, 1):                                               # water sacs on its flanks
        x0, x1 = sorted((sx * 6.6, sx * 7.6))
        m.box(bd, x0, 10, 8, x1, 15, 12, jelly)

    # the rearing neck: red rings up the back, a huge cyan sac down the front over the blue throat
    nk = m.bone("neck", bd, (0, 18, -4))
    pts = [(0, 17, -4), (0, 22, -6), (0, 27, -7.5)]
    for a, b, t in zip(pts, pts[1:], (9, 8)):
        rod(m, nk, a, b, t, segf(seed=6), extend=1.0)
    m.box(nk, -3.6, 12, -10.5, 3.6, 26, -7.5, jelly)                 # the throat sac
    m.box(nk, -3.0, 11, -9.0, 3.0, 15, -5.0, solid("blue"))          # the blue throat below it

    hd = m.bone("head", nk, (0, 28, -8))
    m.round_box(hd, 0, -8.5, 4.6, 5.0, 27.5, 36.5, hoodf, cut=1.6)     # the red hood and face
    m.box(hd, -2.4, 26.2, -16.0, 2.4, 29.2, -12.8, solid("beak"))      # the hooked grey beak
    m.box(hd, -1.6, 25.0, -16.0, 1.6, 26.4, -14.4, solid("grey_dark"))
    m.box(hd, -1.0, 26.6, -14.2, 1.0, 27.4, -11.0, solid("tongue"))    # a cyan tongue

    # thick front legs: red rings, a big cyan sac on the elbow, dark-red toes
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        lg = m.bone(nm, top, (sx * 6.5, 14, -3))
        slab_xy(m, lg, sx * 7.6, 10.5, 3.8, 3.8, -7, 0, segf(seed=sx, band=0), cut=1)
        m.round_box(lg, sx * 7.6, -3.4, 3.4, 3.4, 2, 9, segf(seed=sx + 2, spotted=False, band=0), cut=1.0)
        x0, x1 = sorted((sx * 10.6, sx * 11.6))
        m.box(lg, x0, 4, -6, x1, 11, -1, jelly)                            # the elbow sac
        m.box(lg, sx * 7.4 - 2.6, 0, -6.4, sx * 7.4 + 2.6, 2.0, -0.6, solid("blue"))
        toes(m, lg, sx * 7.4, 0, -6.2, 3, 1.5, 1.7, 1.8)
    for sx, nm in ((1, "leg_back_left"), (-1, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 5.5, 9, 13))
        m.round_box(lg, sx * 6.2, 13.5, 3.2, 3.4, 0.5, 8, segf(seed=sx + 5, spotted=False, band=0), cut=1.0)
        x0, x1 = sorted((sx * 8.6, sx * 9.4))
        m.box(lg, x0, 3, 11.5, x1, 7, 15, jelly)
        m.box(lg, sx * 6.2 - 2.4, 0, 10.6, sx * 6.2 + 2.4, 1.6, 15.5, solid("grey"))
        toes(m, lg, sx * 6.2, 0, 10.8, 3, 1.3, 1.5, 1.6)

    # the segmented tail, rising a little to a grey spike
    t1 = m.bone("tail", bd, (0, 11, 18))
    tp = [(0, 11, 18), (0, 12, 22), (0, 14, 25.5), (0, 16.5, 28.5)]
    for i, (a, b, t) in enumerate(zip(tp, tp[1:], (8, 6.5, 5))):
        rod(m, t1, a, b, t, segf(seed=8 + i, belly="grey"), extend=0.8)
    tip_spike(m, t1, (0, 16.5, 28.5), (0, 0.6, 1), 4, 5)
    return m
