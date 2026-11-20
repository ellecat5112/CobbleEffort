"""A Dialga-shaped body for the Gen 4 paradox Dialgas (Proto-Dialga, Iron Epoch): a deep-chested four-legged dragon
with a chest gem in an armour frame, a long neck rising steeply to a long head with a crest blade, armoured legs
with three claws and a spiked tail. Materials by key (missing ones fall back to "skin"): skin, belly, neck, head,
crest, armour, leg_upper, leg_lower, foot, claw, tail, core, plate.

Front is -z. Returns anchors: top, body, neck, head, jaw, head_c (skull centre), eye (side point), core (chest gem
centre), shoulder (back point between the shoulders), legs {name: {bone, hip, knee, foot}}, tail, tail_pts.
"""
from __future__ import annotations

from _boxmodel import rod, spike
from _digibeast import slab_z
from _pgen1 import smooth_path
from _regi import ellipsoid

BODY_Y = 24.0


def dialga(m, mats, name, neck_w=4.4):
    def M(k):
        return mats.get(k) or mats["skin"]

    top = m.bone(name, None, (0, 0, 0))
    bd = m.bone("body", top, (0, BODY_Y, 0))
    for z0, z1, rx, ry, dy in ((-13, -9, 6.2, 6.8, 0.6), (-9, -4, 7.0, 7.2, 0.4), (-4, 1, 6.8, 6.6, 0.0),
                               (1, 6, 6.2, 6.0, 0.2), (6, 11, 5.8, 5.4, 0.6), (11, 14, 4.6, 4.2, 1.2)):
        slab_z(m, bd, 0, BODY_Y + dy, z0, z1, rx, ry, M("skin"))                    # the body, deep at the chest
    m.box(bd, -3.2, BODY_Y - 7.2, -10.0, 3.2, BODY_Y - 5.6, 8.0, M("belly"))
    core = (0, BODY_Y + 0.4, -14.4)
    ellipsoid(m, bd, core[0], core[1], core[2], 2.6, 3.4, 1.4, M("core"), step=1)   # the chest gem
    for sx in (-1, 1):                                                           # its armour frame
        rod(m, bd, (0, BODY_Y + 5.4, -13.6), (sx * 4.2, BODY_Y + 1.0, -13.4), 1.6, M("plate"), extend=0.6)
        rod(m, bd, (sx * 4.2, BODY_Y + 1.0, -13.4), (0, BODY_Y - 4.8, -13.6), 1.6, M("plate"), extend=0.6)
        rod(m, bd, (sx * 4.6, BODY_Y + 1.0, -13.0), (sx * 7.8, BODY_Y + 0.4, -12.0), 1.4, M("plate"), extend=0.4)
        x0, x1 = sorted((sx * 4.4, sx * 8.0))                                    # shoulder plates
        m.box(bd, x0, BODY_Y + 2.0, -11.0, x1, BODY_Y + 6.4, -3.0, M("armour"), rotation=(0, 0, sx * 18),
              pivot=(sx * 6.0, BODY_Y + 4.0, -7.0))
    nk = m.bone("neck", bd, (0, BODY_Y + 4.0, -10.0))
    npts = smooth_path([(0, BODY_Y + 3.0, -9.0), (0, BODY_Y + 10.0, -13.0), (0, BODY_Y + 17.0, -15.0),
                        (0, BODY_Y + 23.0, -15.5)], 8)
    for i, (a, b) in enumerate(zip(npts, npts[1:])):
        w = neck_w * (1.25 - 0.35 * i / (len(npts) - 2))
        rod(m, nk, a, b, round(w * 2) / 2, M("neck"), extend=0.8)
        m.box(nk, -1.0, a[1] - 0.6, a[2] - w / 2 - 0.6, 1.0, b[1] + 0.6, a[2] - w / 2 + 0.4, M("plate"))
    hy, hz = BODY_Y + 25.0, -16.0
    hd = m.bone("head", nk, (0, hy, hz))
    m.round_box(hd, 0, hz - 1.0, 3.6, 3.4, hy - 2.0, hy + 3.0, M("head"), cut=1)   # skull
    m.round_box(hd, 0, hz - 7.0, 2.6, 3.4, hy - 1.8, hy + 1.4, M("head"), cut=0.6)  # snout
    jw = m.bone("jaw", hd, (0, hy - 1.4, hz))
    m.box(jw, -1.8, hy - 2.8, hz - 8.6, 1.8, hy - 1.4, hz + 0.4, M("head"), rotation=(8, 0, 0), pivot=(0, hy - 1.4, hz))
    spike(m, hd, (0, hy + 2.2, hz - 1.0), (0, 0.9, 0.5), 2.0, 7.0, M("crest"), tip=1.0)   # the crest blade
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, hy + 1.6, hz + 0.6), (sx * 0.5, 0.35, 1), 1.4, 4.4, M("crest"), tip=0.6)
        spike(m, hd, (sx * 1.8, hy - 1.6, hz - 6.0), (sx * 0.2, -1, -0.2), 1.0, 2.4, M("claw"))   # fangs at its jaw
    a = {"top": top, "body": bd, "neck": nk, "head": hd, "jaw": jw, "head_c": (0, hy + 0.4, hz - 1.0),
         "eye": (3.0, hy + 1.0, hz - 2.6), "core": core, "shoulder": (0, BODY_Y + 6.0, -4.0), "legs": {}}
    for nm, sx, z, front in (("leg_front_left", 1, -8.0, True), ("leg_front_right", -1, -8.0, True),
                             ("leg_back_left", 1, 8.0, False), ("leg_back_right", -1, 8.0, False)):
        hip = (sx * 6.2, BODY_Y - 1.0, z)
        lg = m.bone(nm, top, hip)
        ellipsoid(m, lg, hip[0] + sx * 0.6, hip[1] - 1.6, z, 3.2, 5.0, 3.6, M("leg_upper"), step=1)
        if front:
            kn = (sx * 7.0, 12.0, z - 0.6)
            ft = (sx * 7.4, 2.0, z - 1.6)
            rod(m, lg, (hip[0] + sx * 0.6, hip[1] - 3.0, z), kn, 4.6, M("leg_upper"), extend=0.8)
            rod(m, lg, kn, ft, 4.2, M("leg_lower"), extend=0.6)
        else:
            kn = (sx * 7.0, 13.0, z - 2.4)
            hock = (sx * 7.2, 6.6, z + 2.2)
            ft = (sx * 7.4, 2.0, z + 0.6)
            rod(m, lg, (hip[0] + sx * 0.6, hip[1] - 3.0, z), kn, 5.0, M("leg_upper"), extend=0.8)
            rod(m, lg, kn, hock, 4.0, M("leg_lower"), extend=0.6)
            rod(m, lg, hock, ft, 3.6, M("leg_lower"), extend=0.5)
        m.box(lg, ft[0] - 2.6, 0, ft[2] - 3.8, ft[0] + 2.6, 2.8, ft[2] + 1.8, M("foot"))
        for c in (-1, 0, 1):
            spike(m, lg, (ft[0] + c * 1.6, 1.0, ft[2] - 3.6), (c * 0.25, -0.25, -1), 1.4, 3.0, M("claw"), tip=0.7)
        a["legs"][nm] = {"bone": lg, "hip": hip, "knee": kn, "foot": ft}
    tl = m.bone("tail", bd, (0, BODY_Y + 1.0, 13.0))
    tpts = smooth_path([(0, BODY_Y + 1.0, 12.0), (0, BODY_Y - 1.0, 19.0), (0, BODY_Y - 5.0, 25.0),
                        (0, BODY_Y - 10.0, 29.0), (0, BODY_Y - 14.0, 31.0)], 10)
    for i, (p0, p1) in enumerate(zip(tpts, tpts[1:])):
        rod(m, tl, p0, p1, max(1.5, round((4.4 - 3.0 * i / (len(tpts) - 2)) * 2) / 2), M("tail"), extend=0.8)
    a.update({"tail": tl, "tail_pts": tpts})
    return a
