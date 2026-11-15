"""Agumon's body, shared by its variants (CobbleEffort: Digital): Agumon (the hand-built original keeps its own module),
Agumon (Black), the X-Antibody Agumon (longer chrome claws, a striped tail), Agumon Hakase (mortarboard, lab coat and
pointer) and Agumon: Burst Mode (floating, arms spread, wrapped in a translucent pink glow)."""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import P, claw_fan, eye, solid, teeth_row
from _route import tone

ORANGE = {"hide": "orange", "dark": "orange_dark", "belly": "belly", "stripe": "stripe"}
BLACK = {"hide": "char", "dark": "char_dark", "belly": "char_belly", "stripe": "xstripe"}


def hidef(keys, stripes=False):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "down":
            return tone(p[keys["dark"]], face), None
        if face == "north" and abs(x) < 2.0 and 8 < y < 15:
            return tone(p[keys["belly"]], face), None
        if stripes and face in ("east", "west", "up") and (y + z * 0.5) % 3.2 < 0.7 and z > 2:
            return tone(p[keys["stripe"]], face), None
        return tone(p[keys["hide"]], face), None
    return s


def glowwing(x, y, z, face, variant, **k):
    """A wing of translucent pink spirit-light (a cut-out plane): broad at the body, fraying into points."""
    p = P(variant)
    u, v = abs(x) - 2.5, y - 6.0                                       # 0..11.5 out, 0..16 up
    lo, hi = 3.0 + u * 0.35, 15.5 - u * 0.25
    if not (lo < v < hi) or (u > 7 and (v + u) % 3.0 < 1.0):
        return (0, 0, 0, 0), None
    return p["burst"], None


def build_agumon(name, keys=ORANGE, x_antibody=False, hakase=False, burst=False) -> Model:
    hide = hidef(keys, stripes=x_antibody)
    claw = "chrome" if x_antibody else "claw"

    def headf(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("east", "west"):
            c = eye(p, z + 2.6, y - 20.4, 1.25)
            if c is not None:
                return c, None
        if face == "north" and 19.0 < y < 19.6 and abs(abs(x) - 1.0) < 0.35:
            return p["pupil"], None
        return hide(x, y, z, face, variant)

    m = Model(name)
    top = m.bone(name, None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 1))
    m.round_box(bd, 0, 1.0, 3.4, 3.2, 7.0, 13.0, hide, cut=1.2)
    m.round_box(bd, 0, 0.0, 3.0, 2.8, 12.8, 16.6, hide, cut=1.0)
    hd = m.bone("head", bd, (0, 16.5, -0.5))
    m.round_box(hd, 0, -1.8, 3.4, 3.6, 16.2, 22.2, headf, cut=1.4)
    m.box(hd, -2.6, 17.4, -9.2, 2.6, 20.4, -4.6, headf)
    m.box(hd, -2.1, 20.2, -8.6, 2.1, 20.8, -4.6, headf)
    teeth_row(m, hd, [(sx * 2.3, 17.5, z) for sx in (-1, 1) for z in (-8.4, -6.9, -5.4)], (0, -1, 0), 0.7, 0.8)
    jw = m.bone("jaw", hd, (0, 17.2, -2.5))
    m.box(jw, -2.3, 15.6, -8.4, 2.3, 17.3, -3.0, hide)
    teeth_row(m, jw, [(sx * 2.0, 17.2, z) for sx in (-1, 1) for z in (-7.6, -6.0)], (0, 1, 0), 0.6, 0.6)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 3.0, 14.2, -0.6))
        if burst:                                                     # arms spread wide, like wings
            rod(m, a, (sx * 3.0, 14.2, -0.6), (sx * 9.0, 15.0, -1.0), 2.4, hide, extend=0.5)
            claw_fan(m, a, (sx * 9.6, 15.0, -1.0), (sx * 1, 0.1, -0.2), 3, 0.8, 1.6, 0.75, side=(0, 0, 1))
        else:
            rod(m, a, (sx * 3.0, 14.2, -0.6), (sx * 4.0, 11.6, -3.6), 2.4, hide, extend=0.5)
            claw_fan(m, a, (sx * 4.0, 11.2, -4.4), (0, -0.35, -1), 3, 0.8, 2.8 if x_antibody else 1.8, 0.75, key=claw)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 8.0, 1.0))
        m.round_box(lg, sx * 2.6, 1.4, 2.1, 2.5, 2.4, 8.6, hide, cut=0.8)
        m.box(lg, sx * 2.6 - 2.0, 0, -2.6, sx * 2.6 + 2.0, 2.6, 3.0, hide)
        claw_fan(m, lg, (sx * 2.6, 0.8, -2.6), (0, -0.1, -1), 3, 0.9, 2.6 if x_antibody else 1.8, 1.2, key=claw)
    tl = m.bone("tail", bd, (0, 9.5, 4))
    rod(m, tl, (0, 9.5, 3.6), (0, 6.5, 9.0), 3.6, hide, extend=0.6)
    rod(m, tl, (0, 6.5, 9.0), (0, 4.0, 13.0), 2.4, hide, extend=0.5)
    if hakase:
        cp = m.bone("cap", hd, (0, 22.2, -1.8))
        m.box(cp, -2.6, 22.0, -4.2, 2.6, 23.2, 0.6, solid("cap"))           # the mortarboard
        m.box(cp, -4.4, 23.2, -6.0, 4.4, 23.8, 2.4, solid("cap"))
        rod(m, cp, (3.8, 23.6, -5.4), (4.6, 20.4, -6.0), 0.6, solid("tassel"), extend=0.1)
        m.box(bd, -3.9, 6.0, -3.0, 3.9, 16.8, 5.0, solid("coat"))           # the lab coat (open at the front)
        m.box(bd, -3.9, 6.0, -3.2, -1.6, 16.8, -3.0, solid("coat_dark"))
        m.box(bd, 1.6, 6.0, -3.2, 3.9, 16.8, -3.0, solid("coat_dark"))
        rod(m, m.bone("pointer", bd, (4.0, 11.0, -4.4)), (4.0, 11.0, -4.4), (5.0, 22.0, -6.0), 0.6, solid("metal"),
            extend=0.1)
        m.box(bd, 4.6, 21.6, -6.4, 5.4, 22.4, -5.6, solid("metal_light"))
    if burst:                                                         # the translucent spirit glow round it
        ab = m.bone("aura", bd, (0, 12, 1))
        for sx in (-1, 1):
            x0, x1 = sorted((sx * 2.5, sx * 14.0))
            m.box(ab, x0, 6.0, 2.0, x1, 22.0, 2.0, glowwing)
        m.round_box(ab, 0, 1.0, 4.2, 4.2, 6.0, 22.5, solid("burst_core"), cut=2.0)
    return m
