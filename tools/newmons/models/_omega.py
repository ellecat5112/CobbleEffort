"""The Omegamon Alter knights (CobbleEffort: Digital), one builder for both: a towering knight on long digitigrade legs
with golden talons, plated armour trimmed in gold, spiked gold pauldrons, a horned crested helmet with a red visor, a
long tattered black cape, a long sword on one arm and a lion-head shield with a great cannon on the other.
Alter-S: white armour, a golden blade, a red lion. Alter-B: black armour seamed with glowing red, a red-black blade, a
black lion with a gold cannon."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import P, solid
from _route import tone

SCHEMES = {
    "S": {"armour": "knight", "armour_dark": "knight_dark", "trim": "gold", "blade": "blade", "edge": "gold",
          "lion": "lion", "cannon": "cannon", "seam": None},
    "B": {"armour": "cape", "armour_dark": "cape_light", "trim": "gold", "blade": "red", "edge": "red_dark",
          "lion": "cape", "cannon": "gold", "seam": "glow"},
}


def plate(sc, key="armour"):
    """Armour plate: the scheme's colour, gold trim along the top edge of each plate; Alter-B's seams glow red."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        top = box.lo[1] + box.size[1]
        if face not in ("up", "down") and top - y < 0.6 and box.size[1] > 2:
            return tone(p[sc["trim"]], face), None
        if sc["seam"] and face not in ("up", "down"):
            a = {"north": x, "south": -x, "east": z, "west": -z}[face]
            if abs(((a + y * 0.6) % 6.0) - 3.0) < 0.22:
                return p["glow"], p["glow"]
        return tone(p[sc[key]], face), None
    return s


def capef(sc):
    """The tattered black cape (a cut-out plane in the xy plane): ragged tears along its lower edge."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        hem = 4.0 + 3.5 * abs(math.sin(x * 0.9)) + 2.0 * abs(math.sin(x * 2.3 + 1))
        if y < hem:
            return (0, 0, 0, 0), None
        if (x * 1.3 + y * 0.2) % 5 < 0.25:
            return tone(p["cape_light"], face), None
        return tone(p["cape"], face), None
    return s


def visorf(sc):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north" and 50.2 < y < 51.0 and 0.6 < abs(x) < 2.4:
            return p["red"], p["glow"]
        return plate(sc)(x, y, z, face, variant, **k)
    return s


def lionf(sc):
    """The lion-head shield: a snarling face with glowing eyes."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            cx, cy = box.lo[0] + box.size[0] / 2, box.lo[1] + box.size[1] / 2
            if any(math.hypot(x - cx - ox, y - cy - 1.6) < 0.8 for ox in (-1.6, 1.6)):
                return p["blade"], p["blade"]
            if abs(y - cy + 1.6) < 0.5 and abs(x - cx) < 2.2:
                return p["pupil"], None
        return tone(p[sc["lion"]], face), None
    return s


def bladef(sc):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        lx = x - (box.lo[0] + box.size[0] / 2)
        if abs(lx) > box.size[0] / 2 - 0.6:
            return tone(p[sc["edge"]], face), (p["glow"] if sc["seam"] else None)
        return tone(p[sc["blade"]], face), (p["glow"] if sc["seam"] else None)
    return s


def build_knight(name: str, scheme: str) -> Model:
    sc = SCHEMES[scheme]
    m = Model(name)
    arm = plate(sc)
    gold = solid("gold")
    top = m.bone(name, None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 1))
    m.round_box(bd, 0, 1.0, 4.0, 3.2, 27.0, 32.0, solid("joint"), cut=1.0)        # the waist
    m.round_box(bd, 0, 0.5, 6.2, 4.6, 31.5, 42.0, arm, cut=1.8)                  # the chest
    m.box(bd, -2.4, 35.0, -4.5, 2.4, 39.0, -3.9, solid("red", glow=True))         # the chest emblem
    for sx in (-1, 1):
        rod(m, bd, (sx * 0.6, 39.5, -4.2), (sx * 4.4, 34.0, -4.0), 1.0, gold, extend=0.2)   # gold V trim
    cp = m.bone("cape", bd, (0, 42, 5))                                           # the long tattered cape
    m.box(cp, -13.0, 2.0, 6.5, 13.0, 43.0, 6.5, capef(sc), rotation=(-8, 0, 0), pivot=(0, 42, 6.5))
    hd = m.bone("head", bd, (0, 43, 0))
    m.round_box(hd, 0, -0.5, 3.0, 3.2, 42.5, 49.0, arm, cut=1.0)
    m.round_box(hd, 0, -1.2, 3.2, 3.4, 48.5, 52.5, visorf(sc), cut=1.0)
    for sx in (-1, 1):                                                            # horned crest
        spike(m, hd, (sx * 1.6, 52.0, -1.0), (sx * 0.35, 1, 0.5), 1.4, 6.0, gold, tip=0.4)
    spike(m, hd, (0, 52.2, -2.6), (0, 1, -0.2), 1.6, 4.0, gold, tip=0.4)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 7.5, 40.0, 0.5))
        m.round_box(a, sx * 9.0, 0.5, 3.6, 3.6, 38.0, 44.0, arm, cut=1.4)        # pauldron
        for i, d in enumerate(((sx * 0.4, 1, 0.1), (sx * 1, 0.7, 0.2), (sx * 0.8, 1, -0.5))):
            spike(m, a, (sx * (9.5 + i * 0.6), 43.0, 0.5 - i), d, 1.8, 5.5 - i, gold, tip=0.4)
        rod(m, a, (sx * 9.0, 38.0, 0.5), (sx * 10.0, 30.5, -1.5), 3.0, solid("joint"), extend=0.6)
        m.round_box(a, sx * 10.2, -2.5, 2.4, 2.8, 23.5, 31.0, arm, cut=0.8)        # forearm
        if sx == -1:                                                              # the sword arm
            m.box(a, sx * 10.2 - 2.6, 24.0, -5.0, sx * 10.2 + 2.6, 28.0, 0.0, gold)   # golden gauntlet
            rod(m, a, (sx * 10.4, 25.0, -5.0), (sx * 13.0, 3.0, -16.0), 3.2, bladef(sc), extend=0.2, t2=0.8)
            spike(m, a, (sx * 13.0, 3.0, -16.0), (0.12, -0.85, -0.45), 3.0, 4.0, bladef(sc), tip=0.4)
        else:                                                                     # the lion shield and cannon
            m.box(a, sx * 10.2 - 4.4, 22.0, -9.0, sx * 10.2 + 4.4, 31.0, -5.0, lionf(sc))
            for i, ang in enumerate(range(0, 360, 45)):                           # a mane of gold spikes
                d = (math.cos(math.radians(ang)), math.sin(math.radians(ang)), -0.2)
                spike(m, a, (sx * 10.2 + d[0] * 4.0, 26.5 + d[1] * 4.0, -7.0), d, 1.6, 3.2, gold, tip=0.4)
            rod(m, a, (sx * 10.2, 23.5, -5.0), (sx * 11.5, 12.0, -20.0), 4.6, solid(sc["cannon"]), extend=0.2)
            m.box(a, sx * 11.5 - 1.2, 11.0, -21.6, sx * 11.5 + 1.2, 13.4, -20.6, solid("pupil"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 28.0, 1.0))
        m.round_box(lg, sx * 4.4, 0.5, 2.8, 3.2, 18.5, 28.5, arm, cut=1.0)         # thigh
        spike(m, lg, (sx * 4.4, 18.0, -2.6), (0, 0.4, -1), 1.8, 3.4, gold, tip=0.4)   # knee spike
        rod(m, lg, (sx * 4.6, 19.0, 0.5), (sx * 4.8, 5.0, 3.5), 3.6, arm, extend=0.8)   # shin, swept back
        m.box(lg, sx * 4.8 - 2.0, 2.0, 1.0, sx * 4.8 + 2.0, 5.5, 5.5, arm)
        for k in (-1, 0, 1):                                                       # golden talons
            spike(m, lg, (sx * 4.8 + k * 1.4, 2.4, 1.2), (k * 0.25, -0.35, -1), 1.3, 6.0, gold, tip=0.3)
        spike(m, lg, (sx * 4.8, 2.4, 5.4), (0, -0.4, 1), 1.2, 3.0, gold, tip=0.3)
    return m
