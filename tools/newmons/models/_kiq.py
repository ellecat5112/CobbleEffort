"""Kiq's body, shared by Kiq and its Gi form (after @magikdex's Cornera region art): a tall kickboxer of rounded,
quilted grey-blue segments: big round shoulder pads with dark crescents, a V-shaped muscular chest, a black tunic with
a white hem and belt (two white tails hanging in front), thick segmented legs and big rounded feet, and arms raised in
a boxing guard (or, on the Gi form, palms pressed together)."""
from __future__ import annotations

import math

from _boxmodel import rod
from _gi import seamed
from _route import tone

HEAD_Y = 33.0                              # the head's centre height


def build_body(m, top, P, solid, gi=False, face=None):
    """Bones body/head/arms/legs on `top`; `face(x, y, face, p)` paints the head first (colour or None). Returns (body,
    head) bones."""
    paint_face = face
    bd = m.bone("body", top, (0, 15, 0))

    def tunic(x, y, z, face, variant, **k):
        p = P(variant)
        if y < 13.4 and face not in ("up", "down"):
            return tone(p["ice_teal" if gi else "white"], face), None                 # the hem
        if gi and face == "north" and abs(x) < (y - 12.6) * 0.38 and y < 18.5:
            return tone(p["ice_teal"], face), None                                   # the Gi's teal front panel
        return tone(p["black"], face), None

    m.round_box(bd, 0, 0.2, 5.4, 3.6, 12.6, 16.2, tunic, cut=1.2)                 # the black tunic, flaring at the hem
    m.round_box(bd, 0, 0.2, 4.6, 3.2, 16.0, 19.4, tunic, cut=1.1)
    m.round_box(bd, 0, 0.2, 4.8, 3.4, 19.0, 20.6, solid("white"), cut=1.1)        # the white belt

    def tails(x, y, z, face, variant, **k):
        p = P(variant)
        return tone(p["black"] if abs(x) < 0.3 else p["white"], face), None
    m.box(bd, -1.8, 12.0, -3.8, 1.8, 20.0, -2.8, tails)                            # its two tails, hanging in front

    chest = seamed(P, "skin", [("x", 0), ("y", 25.2), ("y", 22.6)])
    m.round_box(bd, 0, 0.2, 4.2, 2.9, 20.4, 24.0, chest, cut=1.0)                  # waist
    m.round_box(bd, 0, 0.2, 5.8, 3.5, 23.8, 28.4, chest, cut=1.3)                  # broad chest (a V)

    def pad(sx):
        def s(x, y, z, face, variant, **k):
            p = P(variant)
            outer = sx * x > 7.6
            if (face == "up" and sx * x > 6.4) or (outer and y > 26.4 and face not in ("down",)):
                return tone(p["black"], face), None                                   # dark crescents on the pads
            if abs(y - 25.8) < 0.22 and face not in ("up", "down"):
                return tone(p["seam"], face), None
            return tone(p["skin"], face), None
        return s
    hd = m.bone("head", bd, (0, 28.5, 0))

    def head(x, y, z, face, variant, **k):
        p = P(variant)
        if paint_face:
            c = paint_face(x, y, face, p)
            if c is not None:
                return tone(c, face), None
        if face == "up" and abs(x + 0.3) < 0.22:
            return tone(p["seam"], face), None
        if face == "north" and abs(y - HEAD_Y + 0.3) < 0.24 and abs(x) > 1.8:
            return tone(p["seam"], face), None
        return tone(p["skin"], face), None
    m.round_box(hd, 0, -0.2, 1.8, 1.8, 27.8, HEAD_Y - 2.4, solid("skin"), cut=0.6)             # a short thick neck
    m.round_box(hd, 0, -0.4, 3.2, 3.2, HEAD_Y - 2.8, HEAD_Y + 3.0, head, cut=1.1)
    m.round_box(hd, 0, -0.4, 2.4, 2.4, HEAD_Y + 2.9, HEAD_Y + 3.6, head, cut=0.8)

    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 7.2, 26.5, 0))
        m.round_box(a, sx * 7.4, 0.2, 2.8, 2.8, 24.4, 29.6, pad(sx), cut=1.0)    # big round shoulder pads
        rod(m, a, (sx * 7.8, 25.0, 0.2), (sx * 8.6, 20.6, -1.2), 3.2, seamed(P, "skin", [("y", 23.0)]))
        if gi:                                                                     # palms pressed together
            rod(m, a, (sx * 8.6, 20.6, -1.2), (sx * 2.2, 24.6, -6.2), 3.0, seamed(P, "skin", [("y", 22.4)]))
            m.round_box(a, sx * 1.6, -6.6, 1.4, 1.8, 23.6, 29.4, seamed(P, "skin", [("y", 26.0)]), cut=0.6)
            rod(m, a, (sx * 3.6, 23.8, -5.4), (sx * 2.6, 24.6, -6.4), 2.4, solid("black"), extend=0.2)   # wrist bands
        else:                                                                      # a boxing guard
            rod(m, a, (sx * 8.6, 20.6, -1.2), (sx * 6.2, 24.4, -5.6), 3.2, seamed(P, "skin", [("z", -3.4)]))
            m.round_box(a, sx * 5.8, -6.6, 2.2, 2.2, 23.4, 28.2, seamed(P, "skin", [("y", 26.2), ("x", sx * 5.8)]),
                        cut=0.9)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.8, 13.5, 0))
        m.round_box(lg, sx * 2.8, 0.2, 1.6, 1.6, 12.8, 14.0, solid("black"), cut=0.6)   # dark hip joints
        m.round_box(lg, sx * 3.0, 0.0, 2.5, 2.5, 8.2, 13.0, seamed(P, "skin", [("y", 10.6)]), cut=0.9)
        m.round_box(lg, sx * 3.2, -0.2, 2.8, 2.9, 2.0, 8.6, seamed(P, "skin", [("y", 5.4), ("x", sx * 3.2)]), cut=1.0)
        m.round_box(lg, sx * 3.2, -1.2, 3.0, 3.8, 0.0, 2.4, seamed(P, "skin", [("z", -2.6)]), cut=1.2)
    return bd, hd


def mask_x(P, key, eyes, half=0.62, reach=7.2, flat_to=3.2):
    """The horizontal band of an X-shaped mask as a cut-out plane in front of the face: full height across the face,
    tapering to points far out to the sides; eye holes at `eyes` [(x, y, r, colour)]."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        for ex, ey, r, col in eyes:
            if math.hypot(x - ex, y - ey) < r:
                return (p[col], None) if col else ((0, 0, 0, 0), None)
        h = half if abs(x) < flat_to else half * max(0.0, (reach - abs(x)) / (reach - flat_to))
        if abs(y - HEAD_Y) < h:
            return p[key], None
        return (0, 0, 0, 0), None
    return s
