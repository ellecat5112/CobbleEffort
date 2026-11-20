"""A Mewtwo-shaped body for the Gen 1 paradox Mewtwos (Iron Blast, Feral Mind): the humanoid builder with Mewtwo's
proportions (slim waist and arms, great round thighs, digitigrade legs, three bulbous fingers), a small head with a
short muzzle and two swept-back horns, the tube from the back of its skull, and its long thick tail curling round
on the ground. Materials by key (missing ones fall back to "skin"): skin, chest, abs, pelvis, neck, deltoid,
upper_arm, forearm, hand, finger, thigh, knee, shin, foot, toe, head, muzzle, horn, tube, tail, tail_tip, hip.
Returns the humanoid's anchors plus head, head_c, tail (bone), tail_pts.
"""
from __future__ import annotations

from _boxmodel import rod, spike
from _digibody import humanoid
from _pgen1 import smooth_path
from _regi import ellipsoid


def mewtwo(m, mats, name, horns=True, tail_ctrl=None, tail_w=(4.6, 1.4), tip_from=0.55):
    def M(k):
        return mats.get(k) or mats["skin"]

    a = humanoid(m, mats, bulk=0.82, arm_bulk=0.72, leg_bulk=1.05, digitigrade=True, claws=False, talons=False,
                 toes=2, fingers=3, hand_pose="relaxed", name=name, chest_depth=0.9)
    bd = a["body"]
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):                       # the great round thighs
        lg = a[nm]["bone"]
        ellipsoid(m, lg, sx * 3.4, 25.5, -0.4, 3.4, 5.6, 3.6, M("hip"), step=1)
    ellipsoid(m, bd, 0, 33.0, 0.4, 4.4, 2.6, 3.4, M("hip"), step=1)            # the round belly/hips
    hd = m.bone("head", bd, (0, 55.0, 0))
    ellipsoid(m, hd, 0, 58.6, -0.2, 3.1, 3.4, 3.4, M("head"), step=1)          # small round head
    m.round_box(hd, 0, -3.6, 1.6, 1.2, 55.6, 58.0, M("muzzle"), cut=0.5)       # short muzzle
    if horns:
        for sx in (-1, 1):                                                   # swept-back horns
            rod(m, hd, (sx * 1.8, 60.6, 0.4), (sx * 2.6, 64.0, 2.6), 1.6, M("horn"), extend=0.4)
            spike(m, hd, (sx * 2.6, 63.8, 2.4), (sx * 0.2, 0.6, 1), 1.2, 2.2, M("horn"), tip=0.6)
    rod(m, hd, (0, 58.6, 2.8), (0, 54.0, 4.6), 1.6, M("tube"), extend=0.4)     # the tube from its skull
    rod(m, bd, (0, 54.2, 4.4), (0, 50.0, 3.6), 1.6, M("tube"), extend=0.4)
    tl = m.bone("tail", bd, (0, 31.0, 3.4))
    ctrl = tail_ctrl or [(0, 31.0, 3.4), (0, 27.0, 9.0), (0, 20.0, 14.0), (0, 12.0, 16.5), (2.0, 5.0, 16.0),
                         (4.0, 2.0, 11.0), (3.0, 1.6, 6.0)]
    pts = smooth_path(ctrl, 16)
    w0, w1 = tail_w
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        f = i / (len(pts) - 2)
        rod(m, tl, p0, p1, max(1.0, round((w0 + (w1 - w0) * f) * 2) / 2), M("tail" if f < tip_from else "tail_tip"),
            extend=0.8)
    a.update({"head": hd, "head_c": (0, 58.6, -0.2), "tail": tl, "tail_pts": pts})
    return a
