"""Nozzlurm, the Spray Worm Pokémon (Bug/Water; after the art of the user's friend on r/fakemon, signed "sno", shared
with permission; our name): a grey velvet worm on four stubby legs, orange rings across its back, a blue neck and
belly, an orange tail curling up with a cyan jelly band, a grey head under an orange hood, red eye discs with a white
slit, and a long cyan nozzle snout with a bulb at its end, which it sprays water and glue from.

Front is -z, y is up. 18 units tall; baseScale 0.75 (0.85 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _scarab import slab_xy
from _velvet import P, eye_disc, jelly, segf, solid, toes
from _route import tone

SCALE = 0.75
HITBOX = [1.4, 1.2]
KIND = "quadruped"
K = 5
HEIGHT = 18
LOOK = ("a grey velvet worm on stubby legs with orange rings across its back, a blue neck and belly, an orange tail "
        "curling up, a grey head under an orange hood, red eye discs with a white slit and a long cyan nozzle snout")


def bodyf(x, y, z, face, variant, box=None, **k):
    """Grey sides, orange rings across the back, a blue belly."""
    p = P(variant)
    if face == "down" or (face in ("east", "west") and y < 6.4):
        return tone(p["blue"], face), None
    if (face == "up" or y > 9.0) and int((z + 20) // 1.6) % 2 == 0:
        return tone(p["orange"], face), None
    return tone(p["grey"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye_disc(p, z + 6.6, y - 13.4, 1.5, iris="eye_red", slit=True)
        if c is not None:
            return c, None
    if face != "down" and y > 14.8:
        return tone(p["orange"], face), None                          # the orange hood
    if face != "down" and abs(y - 14.4) < 0.4:
        return tone(p["blue"], face), None                            # a blue line under it
    return tone(p["grey"], face), None


def build() -> Model:
    m = Model("nozzlurm")
    top = m.bone("nozzlurm", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 1))
    slab_xy(m, bd, 0, 7.6, 3.4, 3.0, -3, 6, bodyf)                     # the long body
    nk = m.bone("neck", bd, (0, 8, -2.5))
    rod(m, nk, (0, 8, -2.5), (0, 12, -4.5), 4, segf("blue", band=0, spotted=False), extend=0.8)
    m.box(nk, -1.4, 9.0, -5.6, 1.4, 12.0, -4.6, solid("orange"))      # an orange stripe up its neck
    hd = m.bone("head", nk, (0, 12.5, -5))
    m.round_box(hd, 0, -6.4, 2.4, 2.6, 11.6, 16.6, headf, cut=0.8)
    m.box(hd, -1.4, 11.8, -9.6, 1.4, 14.0, -8.6, solid("grey"))        # the snout
    rod(m, hd, (0, 13.0, -9.4), (0, 12.4, -15.0), 1.4, jelly, extend=0.2)   # the long cyan nozzle
    m.box(hd, -1.2, 11.4, -16.6, 1.2, 13.8, -14.4, jelly)               # its bulb
    for leg, (lx, lz) in (("leg_front_left", (2.2, -1.6)), ("leg_front_right", (-2.2, -1.6)),
                          ("leg_back_left", (2.4, 4.6)), ("leg_back_right", (-2.4, 4.6))):
        lg = m.bone(leg, top, (lx, 5.5, lz))
        m.round_box(lg, lx, lz, 1.5, 1.6, 0.6, 6.2, segf("grey", band=0, spotted=False, belly="grey_dark"), cut=0.5)
        toes(m, lg, lx, 0, lz - 0.6, 3, 0.9, 1.0, 1.2, key="orange")
    tl = m.bone("tail", bd, (0, 8.5, 6))
    tp = [(0, 8.5, 6), (0, 10, 8.6), (0, 12.6, 9.6), (0, 14.6, 9)]
    for i, (a, b, t) in enumerate(zip(tp, tp[1:], (2.8, 2.4, 2.0))):
        rod(m, tl, a, b, t, segf("orange", band=0.7 if i == 1 else 0, spotted=False), extend=0.6)
    return m
