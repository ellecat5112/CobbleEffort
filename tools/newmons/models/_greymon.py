"""Greymon's body, shared with MetalGreymon (CobbleEffort: Digital): a hunched orange tyrant with blue tiger stripes, a
skull helmet with a nose horn and two side horns, an open jaw full of white fangs, clawed arms and feet and a long
striped tail. MetalGreymon adds a steel helmet, a steel chest plate with a glowing hatch, a steel Trident Arm, tattered
purple wings and red spines."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import P, claw_fan, eye, solid, striped, teeth_row
from _route import tone


def hornf(base_key, tip_key):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)
        return tone(p[tip_key] if t > 0.55 else p[base_key], face), None
    return s


def helmetf(key, dark):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("east", "west"):
            c = eye(p, z + 10.0, y - 31.2, 1.4, iris="red")
            if c is not None:
                return c, None
            if math.hypot(z + 10.0, y - 31.2) < 2.1:
                return tone(p[dark], face), None                       # the eye hole
        if face == "down":
            return tone(p[dark], face), None
        return tone(p[key], face), None
    return s


def mouthf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("up", "down"):
        return p["mouth"], None
    return striped(seed=2)(x, y, z, face, variant)


def build_body(name: str, metal: bool) -> Model:
    m = Model(name)
    hide = striped(seed=1)
    top = m.bone(name, None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 3))
    m.round_box(bd, 0, 3.0, 6.0, 6.5, 12.0, 23.0, hide, cut=2.0)             # the hunched body
    m.round_box(bd, 0, -1.5, 5.2, 4.8, 21.0, 28.0, hide, cut=1.8)            # chest and shoulders
    if metal:
        m.box(bd, -4.6, 18.0, -6.6, 4.6, 27.0, -4.8, solid("metal"))        # the steel chest plate
        m.box(bd, -2.0, 21.0, -7.0, 2.0, 24.0, -6.4, solid("red", glow=True))   # its glowing hatch
    hd = m.bone("head", bd, (0, 28, -4))
    helm = helmetf("metal" if metal else "helmet", "metal_dark" if metal else "helmet_dark")
    m.round_box(hd, 0, -5.5, 4.6, 5.0, 26.5, 33.0, hide, cut=1.4)            # the skull
    m.box(hd, -3.6, 27.0, -15.0, 3.6, 30.6, -8.0, hide)                       # the upper snout
    m.box(hd, -5.0, 30.4, -12.0, 5.0, 35.0, -1.5, helm)                       # the helmet over the skull
    m.box(hd, -3.9, 30.2, -15.6, 3.9, 32.6, -11.6, helm)                      # and over the snout
    hk = ("metal_dark", "metal_light") if metal else ("horn", "horn_tip")
    spike(m, hd, (0, 32.4, -13.2), (0, 1, -0.35), 2.6, 6.0, hornf(*hk), tip=0.6)          # the nose horn
    for sx in (-1, 1):
        spike(m, hd, (sx * 4.6, 33.4, -3.5), (sx * 1, 0.9, 0.35), 2.2, 6.5, hornf(*hk), tip=0.6)   # side horns
    teeth_row(m, hd, [(sx * 3.2, 27.2, z) for sx in (-1, 1) for z in (-14.2, -12.4, -10.6, -8.8)], (0, -1, 0), 1.0, 1.6)
    jw = m.bone("jaw", hd, (0, 27.0, -5.0))
    m.box(jw, -3.4, 24.6, -14.0, 3.4, 27.0, -5.0, mouthf, rotation=(18, 0, 0), pivot=(0, 27.0, -5.0))
    for sx in (-1, 1):
        for z in (-12.8, -10.6, -8.6):
            spike(m, jw, (sx * 2.8, 26.8 + (z + 5) * -0.32, z), (0, 1, 0), 0.9, 1.4, solid("teeth"), tip=0.3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 5.4, 24.0, -2.0))
        if metal and sx == 1:                                                  # the steel Trident Arm
            rod(m, a, (sx * 5.6, 24.5, -1.5), (sx * 8.0, 18.0, -6.0), 5.0, solid("metal"), extend=0.8)
            rod(m, a, (sx * 8.0, 18.0, -6.0), (sx * 8.6, 16.0, -11.0), 4.0, solid("metal_dark"), extend=0.6)
            claw_fan(m, a, (sx * 8.6, 15.6, -12.0), (0, -0.2, -1), 3, 1.6, 7.0, 1.7, key="metal_light")
        else:
            rod(m, a, (sx * 5.4, 24.0, -2.0), (sx * 7.0, 18.5, -7.0), 3.6, hide, extend=0.6)
            claw_fan(m, a, (sx * 7.0, 18.0, -8.4), (0, -0.4, -1), 3, 1.3, 4.0, 1.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.6, 14.0, 3.0))
        m.round_box(lg, sx * 4.8, 3.5, 3.4, 4.2, 6.0, 15.5, hide, cut=1.4)       # thighs
        m.round_box(lg, sx * 4.8, 2.5, 2.4, 2.6, 2.4, 7.0, hide, cut=0.8)
        m.box(lg, sx * 4.8 - 3.0, 0.0, -3.2, sx * 4.8 + 3.0, 2.8, 4.6, hide)     # feet
        claw_fan(m, lg, (sx * 4.8, 0.9, -3.2), (0, -0.1, -1), 3, 1.3, 3.2, 1.9)
    pts = [(0, 15.5, 8.5), (0, 12.5, 15.5), (0, 10.5, 22.5), (0, 9.5, 29.0), (0, 10.0, 34.0)]
    t1 = m.bone("tail", bd, pts[0])
    t2 = m.bone("tail_2", t1, pts[2])
    for i, (a, b, t) in enumerate(zip(pts, pts[1:], (7.0, 5.5, 4.0, 2.6))):
        rod(m, t1 if i < 2 else t2, a, b, t, striped(seed=3 + i), extend=1.0)
    if metal:
        for i, (z, y) in enumerate(((-2.5, 34.5), (0.5, 33.0), (3.0, 31.0))):      # red spines behind the helmet
            spike(m, hd, (0, y, z), (0, 0.6, 1), 2.0, 5.5 - i, solid("red"), tip=0.5)
        for sx, nm in ((1, "wing_left"), (-1, "wing_right")):                     # tattered purple wings
            w = m.bone(nm, bd, (sx * 3.0, 27.0, 5.0))
            x0, x1 = sorted((sx * 3.0, sx * 3.0))
            m.box(w, sx * 3.0, 24.0, 4.0, sx * 3.0, 42.0, 26.0, wingf, rotation=(0, sx * 55, sx * 10),
                  pivot=(sx * 3.0, 27.0, 5.0))
    return m


def wingf(x, y, z, face, variant, **k):
    """A tattered wing (a cut-out plane in the yz plane): ragged strips trailing back, darker veins."""
    p = P(variant)
    u, v = z - 4.0, y - 24.0                                            # 0..22 back, 0..18 up
    top = 18.0 - u * 0.35
    if v > top or v < 2.0 + u * 0.55:
        return (0, 0, 0, 0), None
    strip = (v + u * 0.25) % 4.2
    if strip < 0.6 and u > 6:
        return (0, 0, 0, 0), None                                       # gaps between the ragged strips
    if u > 16 and (v * 1.7) % 3 < 1:
        return (0, 0, 0, 0), None
    if strip < 1.1:
        return tone(p["wing_dark"], face), None
    return tone(p["wing"], face), None
