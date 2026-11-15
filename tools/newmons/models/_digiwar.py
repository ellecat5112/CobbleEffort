"""An armoured humanoid body for the Digimon warriors (CobbleEffort: Digital): legs with armoured shins and boots,
hips, an armoured chest, shoulders, arms with gauntlets and a helmeted head, all from one palette, so each warrior
module adds only what makes it itself (weapons, wings, hair, capes). 40 units tall."""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _route import pal, tone


def make_palette(base, shiny):
    def P(v):
        return pal(base, shiny, v)
    return P


def solid_of(P):
    def solid(key, glow=False):
        def s(x, y, z, face, variant, **k):
            p = P(variant)
            c = p[key]
            if len(c) == 4:
                return c, (c[:3] if glow else None)
            return tone(c, face), (c if glow else None)
        return s
    return solid


def plated(P, key, dark, every=3.0):
    """Armour with darker seams every few units."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face not in ("up", "down") and y % every < 0.35:
            return tone(p[dark], face), None
        return tone(p[key], face), None
    return s


def warrior(name, P, keys, eye_key="eye", bulk=1.0, visor=True):
    """keys: suit, armour, armour_dark, skin (face), boot. Returns (model, bones)."""
    solid = solid_of(P)
    arm = plated(P, keys["armour"], keys["armour_dark"])
    suit = solid(keys["suit"])
    b = bulk

    def headf(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north" and abs(y - 35.6) < 0.5 and 0.5 < abs(x) < 1.9:
            return p[eye_key], p[eye_key]
        if face == "north" and visor and y < 35.0:
            return tone(p[keys["skin"]], face), None
        return tone(p[keys["armour"]], face), None

    m = Model(name)
    top = m.bone(name, None, (0, 0, 0))
    bd = m.bone("body", top, (0, 21, 0))
    m.round_box(bd, 0, 0.3, 2.8 * b, 2.0 * b, 18.5, 22.5, suit, cut=0.6)               # hips
    m.round_box(bd, 0, 0.2, 3.0 * b, 2.0 * b, 22.0, 27.0, suit, cut=0.6)               # waist
    m.round_box(bd, 0, 0.0, 3.8 * b, 2.6 * b, 26.5, 32.5, arm, cut=1.0)                # chest armour
    hd = m.bone("head", bd, (0, 32.5, 0))
    m.round_box(hd, 0, -0.2, 2.1, 2.3, 32.5, 38.0, headf, cut=0.7)
    bones = {"top": top, "body": bd, "head": hd}
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 4.2 * b, 31.0, 0.0))
        m.round_box(a, sx * 4.8 * b, 0.0, 1.9 * b, 1.9 * b, 29.0, 33.0, arm, cut=0.6)  # pauldron
        rod(m, a, (sx * 4.8 * b, 30.0, 0.0), (sx * 5.4 * b, 25.0, -0.4), 1.4 * b, suit, extend=0.3)
        m.round_box(a, sx * 5.5 * b, -0.6, 1.3 * b, 1.4 * b, 19.8, 25.4, arm, cut=0.4)  # gauntlet
        m.box(a, sx * 5.5 * b - 0.9 * b, 18.4, -1.6, sx * 5.5 * b + 0.9 * b, 20.0, 0.2, suit)   # hand
        bones[nm] = a
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8 * b, 19.0, 0.2))
        m.round_box(lg, sx * 1.9 * b, 0.3, 1.6 * b, 1.7 * b, 10.5, 19.5, suit, cut=0.5)  # thigh
        m.round_box(lg, sx * 2.0 * b, 0.0, 1.7 * b, 1.8 * b, 2.0, 11.0, arm, cut=0.5)    # armoured shin
        m.box(lg, sx * 2.0 * b - 1.6 * b, 0.0, -2.6, sx * 2.0 * b + 1.6 * b, 2.2, 1.8, solid(keys["boot"]))
        bones[nm] = lg
    return m, bones, solid
