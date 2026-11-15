"""The CobbleEffort Nidoking (Fire/Dragon; the user's "Kiruvian" regional art, artist not named): a huge hunched
charcoal brute on massive forearms armoured in pale hexagonal stone at the shoulders and elbows (and on its knees),
with a row of translucent quartz crystals down its back, a spiky crest, cream crescent ears, a grimacing mouth of cream
teeth, a grey belly, white claws, and a long thick tail curving up, its magma patches glowing through the hide.

Front is -z, y is up. 34 units tall; baseScale 0.9 (1.9 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _nidoflame import P, claws, crystal, eye, hexplate, patched, solid, spikes
from _route import tone

SCALE = 0.9
HITBOX = [2.2, 2.1]
KIND = "quadruped"
K = 4
HEIGHT = 34
ANIM = {"leg_amp": 16}
LOOK = ("a huge hunched charcoal brute on massive forearms armoured in pale hexagonal stone, translucent quartz crystals "
        "down its back, a spiky crest, cream crescent ears, a grimace of cream teeth, a grey belly, white claws and a "
        "long thick tail curving up")


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down" or (face == "north" and y < 16):
        return tone(p["belly"], face), None
    return patched(spacing=4.4, size=0.9, seed=5)(x, y, z, face, variant)


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 12.0, y - 22.6, 1.3, -1)
        if c is not None:
            return c, None
    if face == "north" and 19.0 < y < 20.6 and abs(x) < 2.6:                 # a grimace of cream teeth
        if abs(y - 19.8) < 0.2:
            return p["pupil"], None
        return (p["cream"] if (x + 3) % 1.0 < 0.8 else p["pupil"]), None
    if face in ("east", "west") and abs(y - 19.8) < 0.25 and z < -11:
        return p["pupil"], None
    return patched(spacing=3.6, size=0.6, seed=7)(x, y, z, face, variant)


def crescent(x, y, z, face, variant, box=None, **k):
    """A cream crescent ear (a cut-out plate in the xy plane)."""
    p = P(variant)
    cx, cy = box.lo[0] + box.size[0] / 2, box.lo[1] + box.size[1] / 2
    r = box.size[1] / 2
    d1 = math.hypot(x - cx, y - cy)
    d2 = math.hypot(x - cx - math.copysign(r * 0.45, cx), y - cy - r * 0.25)
    if d1 < r and d2 > r * 0.72:
        return tone(p["cream"], face), None
    return (0, 0, 0, 0), None


def build() -> Model:
    m = Model("nidoking_cobbleeffortian")
    top = m.bone("nidoking", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 2))
    # the hunched body: high shoulders, sloping down to the hips
    m.round_box(bd, 0, -2, 7.0, 6.5, 10, 23, bodyf, cut=2.5)
    m.round_box(bd, 0, 7.5, 6.0, 5.0, 9, 18, bodyf, cut=2.0)
    m.round_box(bd, 0, 1.5, 6.0, 4.0, 22, 25.5, bodyf, cut=2.0)
    # translucent quartz crystals down its back
    for i, (z, y, h) in enumerate(((-4, 25, 6.5), (-0.5, 25.5, 8.0), (3, 24.5, 7.0), (6.5, 19.5, 5.5),
                                   (9.5, 18.0, 4.5))):
        spike(m, bd, (0, y, z), (0, 1, 0.45), 2.6 - 0.2 * i, h, crystal(), tip=0.8)
        for sx in (-1, 1):
            if i < 3:
                spike(m, bd, (sx * 2.4, y - 1.5, z + 0.5), (sx * 0.5, 1, 0.4), 1.6, h * 0.55, crystal(), tip=0.6)

    hd = m.bone("head", bd, (0, 21, -8))
    m.round_box(hd, 0, -11.0, 3.6, 3.6, 18.6, 25.8, headf, cut=1.4)
    m.box(hd, -3.0, 18.6, -15.8, 3.0, 23.0, -13.8, headf)                       # the blunt muzzle
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.6, 18.8, -15.4), (sx * 0.1, -1, -0.2), 1, 1.6, solid("cream"), tip=0.4)   # tusks
    spike(m, hd, (0, 25.0, -13.4), (0, 1, -0.5), 3.0, 5.0, crystal(), tip=0.7)            # the brow crystal
    spikes(m, hd, (0, 25.6, -9.0), [(0, 1, 0.5), (0.7, 1, 0.8), (-0.7, 1, 0.8), (0, 0.6, 1), (1, 0.5, 0.5),
                                    (-1, 0.5, 0.5)], 1.8, 4.2, patched(seed=3))
    for sx, nm in ((1, "ear_left"), (-1, "ear_right")):                        # cream crescent ears
        e = m.bone(nm, hd, (sx * 4.0, 24.0, -9.0))
        x0, x1 = sorted((sx * 3.6, sx * 9.6))
        m.box(e, x0, 22.0, -9.0, x1, 28.0, -9.0, crescent, rotation=(0, -sx * 25, sx * 10), pivot=(sx * 3.6, 24, -9))

    # massive forearms: hexagonal stone on the shoulders and elbows
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        a = m.bone(nm, top, (sx * 7.5, 20, -4))
        m.round_box(a, sx * 7.8, -4.5, 3.4, 3.6, 15, 23, patched(seed=sx), cut=1.4)
        m.round_box(a, sx * 8.4, -5.0, 3.0, 3.2, 3, 15.5, patched(seed=sx + 3), cut=1.2)
        m.round_box(a, sx * 8.4, -5.6, 3.4, 3.8, 0, 3, solid("char_dark"), cut=1.2)      # the fist
        x0, x1 = sorted((sx * 6.0, sx * 12.0))
        m.box(a, x0, 20.0, -8.6, x1, 24.6, 0.0, hexplate(cell=2.2))                    # the shoulder plate
        x0, x1 = sorted((sx * 6.6, sx * 11.6))
        m.box(a, x0, 9.5, -8.6, x1, 14.0, -2.0, hexplate(cell=1.8))            # the elbow plate
        claws(m, a, sx * 8.4, 0.8, -9.2, 4, 1.0, 2.0, 1.3)
    for sx, nm in ((1, "leg_back_left"), (-1, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 6.0, 11, 9))
        m.round_box(lg, sx * 6.4, 9.5, 3.0, 3.6, 4, 13, patched(seed=sx * 2), cut=1.2)
        m.round_box(lg, sx * 6.4, 8.8, 2.4, 2.6, 0, 4.5, patched(seed=sx * 4), cut=1.0)
        x0, x1 = sorted((sx * 4.0, sx * 9.2))
        m.box(lg, x0, 6.0, 5.0, x1, 10.0, 6.0, hexplate(cell=1.6))              # the knee plate
        claws(m, lg, sx * 6.4, 0.6, 6.0, 3, 0.9, 1.6, 1.1)

    pts = [(0, 14, 12), (0, 12.5, 18), (0, 13, 24), (0, 16.5, 29), (0, 22, 31.5)]   # the long tail, curving up
    t1 = m.bone("tail", bd, pts[0])
    t2 = m.bone("tail_2", t1, pts[2])
    for i, (a, b, t) in enumerate(zip(pts, pts[1:], (6.5, 5.5, 4.5, 3.5))):
        rod(m, t1 if i < 2 else t2, a, b, t, patched(seed=11), extend=1.2)
    spike(m, t2, (0, 22, 31.5), (0, 1, 0.3), 3, 3.5, crystal(), tip=0.8)
    return m
