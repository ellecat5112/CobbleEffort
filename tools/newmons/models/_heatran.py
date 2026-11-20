"""A Heatran-shaped body for the Gen 4 paradox Heatrans (Burning Verdure, Iron Forge): a broad domed shell over a
great round ribbed chest, a low hooded head at the front of the chest, and four legs splayed out to the sides with
their knees high. Materials by key (missing ones fall back to "shell"): shell, chest, head, leg_upper, leg_lower,
foot, toe.

Front is -z. Returns anchors: top, body, head, head_c, face_z (the face's front), legs {name: {bone, knee, foot}}.
"""
from __future__ import annotations

from _boxmodel import rod, spike
from _regi import ellipsoid

BY = 13.0


def heatran(m, mats, name, lower=True):
    def M(k):
        return mats.get(k) or mats["shell"]

    top = m.bone(name, None, (0, 0, 0))
    bd = m.bone("body", top, (0, BY, 2.0))
    ellipsoid(m, bd, 0, BY + 3.0, 4.0, 10.6, 6.6, 10.6, M("shell"), step=1)          # the domed shell
    ellipsoid(m, bd, 0, BY - 0.4, -2.6, 8.4, 7.4, 7.0, M("chest"), step=1)           # the round ribbed chest
    hd = m.bone("head", bd, (0, BY + 3.4, -8.0))
    ellipsoid(m, hd, 0, BY + 3.6, -9.6, 4.0, 3.8, 3.4, M("head"), step=1)            # the hooded head
    m.round_box(hd, 0, -12.6, 1.2, 1.4, BY + 0.4, BY + 3.6, M("head"), cut=0.5)      # its beak
    a = {"top": top, "body": bd, "head": hd, "head_c": (0, BY + 3.6, -9.6), "face_z": -13.0, "legs": {}}
    for nm, sx, z in (("leg_front_left", 1, -5.0), ("leg_front_right", -1, -5.0), ("leg_back_left", 1, 9.0),
                      ("leg_back_right", -1, 9.0)):
        dz = -1 if z < 0 else 1
        hip = (sx * 7.6, BY, z)
        lg = m.bone(nm, top, hip)
        kn = (sx * 13.0, BY + 1.4, z + dz * 3.0)
        ft = (sx * 14.4, 0.0, z + dz * 4.6)
        rod(m, lg, hip, kn, 5.0, M("leg_upper"), extend=1.0)
        ellipsoid(m, lg, kn[0], kn[1], kn[2], 3.0, 3.0, 3.0, M("leg_upper"), step=1)
        if lower:
            rod(m, lg, kn, (ft[0], 2.4, ft[2]), 4.6, M("leg_lower"), extend=0.8)
            m.box(lg, ft[0] - 3.0, 0, ft[2] - 3.4, ft[0] + 3.0, 2.6, ft[2] + 2.6, M("foot"))
            for c in (-1, 0, 1):
                spike(m, lg, (ft[0] + c * 1.8, 1.0, ft[2] - 3.2), (c * 0.3, -0.2, -1), 1.6, 2.4, M("toe"), tip=0.8)
        a["legs"][nm] = {"bone": lg, "knee": kn, "foot": ft, "side": sx}
    return a
