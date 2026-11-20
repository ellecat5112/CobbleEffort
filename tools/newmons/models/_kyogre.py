"""A Kyogre-shaped body for the Gen 3 paradox Kyogres (Pristine Aqua, Iron Deluge): a broad whale body (wide, deep
and long, the mouth at its front), two great flat pectoral fins swept forward and down, small dorsal fins and a
three-pronged tail fluke. Shaders: hull (the body), fin (the pectorals' faces), fluke.
"""
from __future__ import annotations

import math

from _boxmodel import rod, spike
from _regi import ellipsoid

CY = 9.0
FIN_LEN, FIN_W = 13.0, 9.0


def body(m, bone, hull, rx=7.6, ry=6.0, rz=12.0):
    ellipsoid(m, bone, 0, CY, 1.0, rx, ry, rz, hull, step=1)


def fin_box(m, bone, sx, shader, y=8.0, z=-1.0, down=18.0, sweep=22.0, thick=2.0):
    """A flat pectoral fin from the shoulder out to the side, tilted down and swept forward. Its shader gets the box's
    own unrotated coordinates: x runs out from the shoulder (u = sx * (x - shoulder)), z across the fin."""
    x0, x1 = sorted((sx * 6.0, sx * (6.0 + FIN_LEN)))
    m.box(bone, x0, y - thick / 2, z - FIN_W / 2, x1, y + thick / 2, z + FIN_W / 2, shader,
          rotation=(0, -sx * sweep, sx * down), pivot=(sx * 6.0, y, z))
    return (sx * 6.0, y, z)


def fluke(m, bone, shader, z0=11.0):
    """The tail: a short tapering stalk and a three-pronged fluke."""
    rod(m, bone, (0, CY + 1.0, z0), (0, CY + 2.0, z0 + 6.0), 4.0, shader, extend=0.6)
    for d in ((0, 0.9, 1), (0.7, 0.2, 1), (-0.7, 0.2, 1)):
        spike(m, bone, (0, CY + 2.0, z0 + 5.6), d, 2.8, 7.0, shader, tip=1.2)


def dorsal(m, bone, shader):
    for sx in (-1, 1):
        spike(m, bone, (sx * 2.6, CY + 6.0, 1.0), (sx * 0.4, 1, 0.6), 2.4, 4.0, shader, tip=0.9)
