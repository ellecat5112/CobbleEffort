"""Koromon (Normal; a Digimon of the CobbleEffort: Digital crossover, built after the official art): a little pink blob
with big red eyes, two tiny fangs and two long wavy ear-stalks streaming back from the top of its head.

Front is -z, y is up. 13 units tall (the ears); baseScale 0.5 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import P, eye, solid
from _route import tone

SCALE = 0.5
HITBOX = [0.8, 0.7]
KIND = "floater"
K = 8
HEIGHT = 13
LOOK = "a little pink blob with big red eyes, two tiny fangs and two long wavy ear-stalks streaming back from its head"


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 1.7, y - 4.4, 1.2, iris="red")
            if c is not None:
                return c, None
            if abs(x - sx * 1.7) < 1.4 and abs(y - 5.7 - 0.3 * sx * (x - sx * 1.7)) < 0.25:
                return p["pupil"], None                                # a fierce brow line over each eye
        if abs(y - 2.2) < 0.2 and abs(x) < 1.6:
            return p["pupil"], None                                    # its mouth
    if face == "down":
        return tone(p["pink_dark"], face), None
    return tone(p["pink"], face), None


def build() -> Model:
    m = Model("koromon")
    top = m.bone("koromon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    for y0, y1, rx, rz in ((0, 1, 2.6, 2.4), (1, 2.4, 3.8, 3.4), (2.4, 5.4, 4.4, 3.8), (5.4, 6.8, 3.8, 3.3),
                           (6.8, 7.8, 2.8, 2.4)):
        m.round_box(bd, 0, 0, rx, rz, y0, y1, bodyf, cut=1.0)
    for sx in (-1, 1):
        spike(m, bd, (sx * 0.9, 2.1, -3.7), (0, -1, -0.2), 0.6, 0.9, solid("teeth"), tip=0.3)   # two tiny fangs
    for sx, nm in ((1, "ear_left"), (-1, "ear_right")):            # long wavy ear-stalks streaming back
        e = m.bone(nm, bd, (sx * 1.2, 7.6, 0.6))
        pts = [(sx * 1.2, 7.6, 0.6), (sx * 2.2, 10.2, 1.6), (sx * 2.8, 11.4, 4.0), (sx * 4.2, 12.6, 6.0),
               (sx * 4.8, 12.2, 8.6)]
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            rod(m, e, a, b, 1.6 - 0.25 * i, solid("pink"), extend=0.3, t2=0.8)
        spike(m, e, pts[-1], (sx * 0.4, 0.3, 1), 0.8, 1.6, solid("pink_dark"), tip=0.3)
    return m
