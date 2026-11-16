"""Dense non-humanoid bodies for the Digimon (CobbleEffort: Digital detail standard), the beast counterparts of
`_digibody.humanoid`: a theropod (upright or leaning dinosaurs and dragons), a quadruped, round balls, horizontal
slabs, feathered and membrane wings. Each builder places anatomical pieces painted from a `mats` dict (missing keys
fall back to "skin") and returns an anchors dict, so a Digimon module adds only what makes it itself.

theropod mats: skin, belly, neck, head, snout, jaw, mouth, tooth, tongue, arm, hand, claw, thigh, shin, foot, talon,
tail, tail_tip. quadruped mats: skin, belly, neck, head, snout, jaw, mouth, tooth, leg_upper, leg_lower, paw, claw,
tail.
"""
from __future__ import annotations

import math

from _boxmodel import rod, spike


def lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


JAW_SIGN = -1.0


def rot_x(p, pivot, deg):
    """p rotated about the x axis through pivot (y, z) the way a box rotation of `deg` about x turns it."""
    a = math.radians(deg) * JAW_SIGN
    y, z = p[1] - pivot[0], p[2] - pivot[1]
    return (p[0], pivot[0] + y * math.cos(a) - z * math.sin(a), pivot[1] + y * math.sin(a) + z * math.cos(a))


def ball(m, bone, c, r, shader, layers=6, squash=1.0, ry=None):
    """A sphere (or ellipsoid: ry = vertical radius, squash = depth/width) of stacked rounded slices."""
    cx, cy, cz = c
    ry = r if ry is None else ry
    for i in range(layers):
        t0, t1 = -1 + 2 * i / layers, -1 + 2 * (i + 1) / layers
        tm = (t0 + t1) / 2
        rr = r * math.sqrt(max(0.04, 1 - tm * tm))
        m.round_box(bone, cx, cz, rr, rr * squash, cy + ry * t0 - 0.02 * (i % 2), cy + ry * t1, shader,
                    cut=max(1, round(rr * 0.32)))


def slab_z(m, bone, cx, cy, z0, z1, rx, ry, shader, cut=None):
    """A block along z rounded in its xy cross-section: two crossed boxes (a horizontal body slice)."""
    cut = max(1, round(min(rx, ry) * 0.3)) if cut is None else cut
    m.box(bone, cx - rx, cy - ry + cut, z0, cx + rx, cy + ry - cut, z1, shader)
    m.box(bone, cx - rx + cut, cy - ry, z0 - 0.05, cx + rx - cut, cy + ry, z1 - 0.05, shader)


def slab_x(m, bone, cx, cy, cz, x0, x1, ry, rz, shader, cut=None):
    """A block along x rounded in its yz cross-section."""
    cut = max(1, round(min(ry, rz) * 0.3)) if cut is None else cut
    m.box(bone, x0, cy - ry + cut, cz - rz, x1, cy + ry - cut, cz + rz, shader)
    m.box(bone, x0 - 0.05, cy - ry, cz - rz + cut, x1 - 0.05, cy + ry, cz + rz - cut, shader)


def tube(m, bone, pts, radii, shader, step=2.0):
    """Round slices along a path (vertical-ish segments: round_box slices; others: rods), radius per point."""
    for (a, ra), (b, rb) in zip(zip(pts, radii), zip(pts[1:], radii[1:])):
        d = math.dist(a, b)
        n = max(1, round(d / step))
        for i in range(n):
            p0, p1 = lerp(a, b, i / n), lerp(a, b, (i + 1) / n)
            r = ra + (rb - ra) * (i + 0.5) / n
            rod(m, bone, p0, p1, max(1, round(2 * r)), shader, extend=0.6)


def fan(m, bone, root, n, length, width, a0, a1, shader, plane="xy", tilt=0.0, curl=0.0, side=1):
    """A fan of flat feathers/fins from `root`: n planes of `length` x `width`, angles a0..a1 (degrees, 0 = straight
    out along +x*side, 90 = up) in the xy plane (plane="xy", seen from the front) or the zy plane ("zy", seen from
    the side); `tilt` turns each about its long axis so its face shows from the front."""
    rx, ry, rz = root
    for i in range(n):
        a = a0 + (a1 - a0) * (i / max(n - 1, 1))
        if plane == "xy":
            x0, x1 = sorted((rx, rx + side * length))
            m.box(bone, x0, ry - width / 2, rz + i * curl * 0.0, x1, ry + width / 2, rz, shader,
                  rotation=(tilt, 0, side * a), pivot=root)
        else:
            m.box(bone, rx, ry - width / 2, rz, rx, ry + width / 2, rz + length, shader,
                  rotation=(-a, 0, 0), pivot=root)


def feather_wing(m, bone, root, span, chord, rows, shader, side=1, sweep=20, droop=0.0, layers=2):
    """A feathered wing: an arm bar out to the side, then rows of long flight feathers hanging back and down from
    it, longest at the tip; `layers` overlapping rows (coverts above the primaries)."""
    rx, ry, rz = root
    tip = (rx + side * span, ry + span * 0.25 - droop, rz + span * math.sin(math.radians(sweep)) * 0.5)
    rod(m, bone, root, lerp(root, tip, 0.5), 3, shader, extend=0.4)
    rod(m, bone, lerp(root, tip, 0.5), tip, 2, shader, extend=0.4)
    for L in range(layers):
        frac = 1.0 - 0.45 * L
        for i in range(rows):
            t = (i + 0.5) / rows
            p = lerp(root, tip, t)
            ln = chord * frac * (0.55 + 0.6 * t)
            w = span / rows + 0.8
            x0, x1 = sorted((p[0] - w / 2, p[0] + w / 2))
            m.box(bone, x0, p[1] - ln, p[2] + 0.3 * L, x1, p[1], p[2] + 0.3 * L, shader,
                  rotation=(-12 - 18 * t, 0, -side * (8 + 25 * t)), pivot=p)
    return tip


def bat_wing(m, bone, root, span, height, fingers, bar, membrane, side=1, sweep=15):
    """A membrane wing: an arm bar, `fingers` finger rods fanning back/down, and cut-out membrane planes between
    them (the membrane shader gets the plane; scallops come from its own cutout)."""
    rx, ry, rz = root
    wrist = (rx + side * span * 0.45, ry + height * 0.35, rz + 2)
    rod(m, bone, root, wrist, 3, bar, extend=0.4)
    tips = []
    for i in range(fingers):
        t = i / max(fingers - 1, 1)
        ang = math.radians(10 + 95 * t)
        tip = (wrist[0] + side * span * 0.55 * math.cos(ang) * (1 - 0.25 * t), wrist[1] + height * (0.5 - 1.1 * t),
               wrist[2] + span * math.sin(math.radians(sweep)) * 0.5 * (1 + t))
        rod(m, bone, wrist, tip, 1, bar, extend=0.3)
        tips.append(tip)
    pts = [root] + tips
    for a, b in zip(tips, tips[1:] + [root]):                      # membrane panels: wrist-a-b triangles as planes
        x0, x1 = sorted((min(wrist[0], a[0], b[0]), max(wrist[0], a[0], b[0])))
        y0, y1 = min(wrist[1], a[1], b[1]), max(wrist[1], a[1], b[1])
        zc = (wrist[2] + a[2] + b[2]) / 3
        m.box(bone, x0, y0, zc, x1, y1, zc, membrane)
    return wrist, tips


def jaws(m, hd, jaw_bone, x_half, y_mouth, z_back, z_front, M, open_deg=18, teeth=6, upper_h=3.0, lower_h=2.0):
    """Upper snout + hinged lower jaw with teeth rows and a tongue. The jaw bone pivots at the back of the mouth."""
    m.box(hd, -x_half, y_mouth, z_front, x_half, y_mouth + upper_h, z_back, M("snout"))
    m.box(hd, -x_half + 0.4, y_mouth - 0.4, z_front + 0.4, x_half - 0.4, y_mouth, z_back, M("mouth"))
    jw = m.bone(jaw_bone, hd, (0, y_mouth, z_back))
    m.box(jw, -x_half + 0.3, y_mouth - lower_h, z_front + 0.5, x_half - 0.3, y_mouth - 0.6, z_back, M("jaw"),
          rotation=(open_deg, 0, 0), pivot=(0, y_mouth, z_back))
    m.box(jw, -x_half + 0.8, y_mouth - 0.8, z_front + 1.2, x_half - 0.8, y_mouth - 0.6, z_back - 0.4, M("tongue"),
          rotation=(open_deg, 0, 0), pivot=(0, y_mouth, z_back))
    L = z_back - z_front
    for i in range(teeth):
        f = (i + 0.5) / teeth
        z = z_front + 0.5 + f * (L * 0.75)
        for sx in (-1, 1):
            x = sx * (x_half - 0.6) * (0.55 + 0.45 * f) if i == 0 else sx * (x_half - 0.6)
            spike(m, hd, (x, y_mouth + 0.2, z), (0, -1, 0), 1.0, 1.6 if i < 2 else 1.2, M("tooth"))
            q = rot_x((x, y_mouth - 0.7, z), (y_mouth, z_back), open_deg)
            spike(m, jw, q, rot_x((0, 1, 0), (0, 0), open_deg), 1.0, 1.2, M("tooth"))
    return jw


def theropod(m, mats, name, hip_y=20.0, hip_z=2.0, chest=(0, 32.0, -2.0), body_r=6.0, chest_r=5.4, belly_r=None,
             neck_top=(0, 40.0, -5.0), head_len=11.0, head_w=4.0, head_h=4.4, mouth_open=20, teeth=6,
             arm_len=8.0, arm_bulk=1.0, fingers=3, leg_bulk=1.0, toes=3, tail=((0, 18, 8), (0, 13, 16), (0, 9, 24),
                                                                                   (0, 6, 31)),
             tail_r=(4.6, 3.6, 2.4, 1.4), stance=4.2, digitigrade=True, head_tilt=0.0):
    """An upright or leaning dinosaur: rounded torso slices from pelvis to chest with a belly plate, a thick neck,
    a long head with a hinged jaw full of teeth, short clawed arms, powerful digitigrade legs with talons and a long
    tapering tail. Returns anchors: top, body, head, jaw, head_c (skull centre), eye (side-of-skull point),
    mouth_y, snout_front, arm_left/arm_right {bone, shoulder, elbow, hand}, leg_left/leg_right {bone, hip, knee,
    ankle}, tail (bone), tail_pts."""
    def M(k):
        return mats.get(k) or mats["skin"]

    top = m.bone(name, None, (0, 0, 0))
    bd = m.bone("body", top, (0, hip_y, hip_z))
    belly_r = body_r * 0.8 if belly_r is None else belly_r
    pelvis = (0, hip_y, hip_z)
    n = 7
    for i in range(n):                                              # torso: rounded slices along pelvis -> chest
        t0, t1 = i / n, (i + 1) / n
        c0, c1 = lerp(pelvis, chest, t0), lerp(pelvis, chest, t1)
        tm = (t0 + t1) / 2
        r = body_r + (chest_r - body_r) * tm + 0.8 * math.sin(tm * math.pi)
        cz = (c0[2] + c1[2]) / 2
        m.round_box(bd, 0, cz, r, r * 0.86, c0[1] - 0.6, c1[1] + 0.6, M("skin"), cut=max(1, round(r * 0.3)))
        br = belly_r * (0.75 + 0.35 * math.sin(tm * math.pi))
        m.box(bd, -br * 0.72, c0[1] - 0.4, cz - r * 0.86 - 0.9, br * 0.72, c1[1] + 0.4, cz - r * 0.86 + 1.0,
              M("belly"))
    nk = m.bone("neck", bd, chest)
    nc = (0, chest[1] + chest_r * 0.4, chest[2])
    for i in range(3):                                              # neck slices
        a, b = lerp(nc, neck_top, i / 3), lerp(nc, neck_top, (i + 1) / 3)
        r = chest_r * (0.78 - 0.1 * i)
        m.round_box(nk, 0, (a[2] + b[2]) / 2, r, r * 0.9, a[1] - 0.6, b[1] + 0.8, M("neck"), cut=max(1, round(r * .3)))
        m.box(nk, -r * 0.55, a[1] - 0.4, (a[2] + b[2]) / 2 - r * 0.9 - 0.8, r * 0.55, b[1] + 0.4,
              (a[2] + b[2]) / 2 - r * 0.9 + 0.8, M("belly"))
    hd = m.bone("head", nk, neck_top)
    hx, hy, hz = neck_top
    skull_z0, skull_z1 = hz - head_len * 0.45, hz + head_len * 0.15
    m.round_box(hd, 0, (skull_z0 + skull_z1) / 2, head_w, (skull_z1 - skull_z0) / 2, hy - head_h * 0.3,
                hy + head_h, M("head"), cut=max(1, round(head_w * 0.35)))
    mouth_y = hy - head_h * 0.1
    sf = hz - head_len
    jw = jaws(m, hd, "jaw", head_w * 0.8, mouth_y, skull_z0 + 1.0, sf, M, open_deg=mouth_open, teeth=teeth,
              upper_h=head_h * 0.62, lower_h=head_h * 0.5)
    for sx in (-1, 1):                                              # brow ridges over the eyes
        x0, x1 = sorted((sx * (head_w - 1.4), sx * (head_w + 0.3)))
        m.box(hd, x0, hy + head_h - 1.2, skull_z0 - 0.6, x1, hy + head_h + 0.2, skull_z0 + 3.4, M("head"),
              rotation=(0, sx * 8, 0), pivot=(sx * head_w, hy + head_h, skull_z0))
    anchors = {"top": top, "body": bd, "neck": nk, "head": hd, "jaw": jw, "head_c": (0, hy + head_h * 0.4, hz),
               "eye": (head_w, hy + head_h * 0.62, skull_z0 + 1.6), "mouth_y": mouth_y, "snout_front": sf,
               "skull_top": hy + head_h, "skull_z": (skull_z0, skull_z1)}
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):             # short clawed arms
        sh = (sx * chest_r * 0.85, chest[1] - 1.0, chest[2] - chest_r * 0.3)
        a = m.bone(nm, bd, sh)
        el = (sh[0] + sx * 1.6, sh[1] - arm_len * 0.5, sh[2] - 1.4)
        hand = (el[0] + sx * 0.4, el[1] - 0.6, el[2] - arm_len * 0.48)
        rod(m, a, sh, el, max(2, round(3.2 * arm_bulk)), M("arm"), extend=0.6)
        rod(m, a, el, hand, max(2, round(2.6 * arm_bulk)), M("arm"), extend=0.6)
        m.box(a, hand[0] - 1.2 * arm_bulk, hand[1] - 1.4, hand[2] - 1.4, hand[0] + 1.2 * arm_bulk, hand[1] + 1.0,
              hand[2] + 0.8, M("hand"))
        for f in range(fingers):
            fx = hand[0] + (f - (fingers - 1) / 2) * 0.9 * arm_bulk
            spike(m, a, (fx, hand[1] - 0.4, hand[2] - 1.2), (sx * 0.05, -0.55, -1), 0.9, 2.2, M("claw"), tip=0.4)
        anchors[nm] = {"bone": a, "shoulder": sh, "elbow": el, "hand": hand}
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):             # digitigrade legs
        hip = (sx * body_r * 0.62, hip_y + 0.5, hip_z)
        lg = m.bone(nm, top, hip)
        lb = leg_bulk
        kn = (sx * (stance + 0.4), hip_y * 0.55, hip_z - 4.0 * lb)
        m.round_box(lg, hip[0] + sx * 0.4, hip_z - 1.0, 3.6 * lb, 4.0 * lb, hip_y * 0.5, hip_y + 3.0, M("thigh"),
                    cut=max(1, round(1.2 * lb)))                    # the great drumstick thigh
        rod(m, lg, (hip[0], hip_y * 0.75, hip_z - 1.0), kn, max(3, round(4.4 * lb)), M("thigh"), extend=0.8)
        if digitigrade:
            hock = (kn[0], hip_y * 0.2, hip_z + 1.6)
            rod(m, lg, kn, hock, max(2, round(3.2 * lb)), M("shin"), extend=0.6)
            ank = (kn[0], 1.6, hip_z - 1.0)
            rod(m, lg, hock, ank, max(2, round(2.6 * lb)), M("shin"), extend=0.5)
        else:
            ank = (kn[0], 1.6, kn[2] + 0.6)
            rod(m, lg, kn, ank, max(3, round(3.8 * lb)), M("shin"), extend=0.6)
        fx, fz = ank[0], ank[2]
        m.box(lg, fx - 2.2 * lb, 0, fz - 3.6 * lb, fx + 2.2 * lb, 2.4, fz + 1.4, M("foot"))
        for t in range(toes):
            tx = fx + (t - (toes - 1) / 2) * 1.5 * lb
            m.box(lg, tx - 0.7 * lb, 0, fz - 5.0 * lb, tx + 0.7 * lb, 1.8, fz - 3.2 * lb, M("foot"))
            spike(m, lg, (tx, 1.0, fz - 5.0 * lb), (0, -0.35, -1), 1.2 * lb, 2.6 * lb, M("talon"), tip=0.5)
        spike(m, lg, (fx, 1.6, fz + 1.0), (sx * 0.2, -0.3, 1), 1.0, 1.6, M("talon"))   # dew claw
        anchors[nm] = {"bone": lg, "hip": hip, "knee": kn, "ankle": ank}
    tl = m.bone("tail", bd, (0, hip_y, hip_z + body_r * 0.6))
    pts = [(0, hip_y, hip_z + body_r * 0.4)] + list(tail)
    radii = [body_r * 0.8] + list(tail_r)
    half = len(pts) // 2
    tip_bone = m.bone("tail_tip", tl, pts[half])
    for j, (a, b) in enumerate(zip(pts, pts[1:])):
        bn = tl if j < half else tip_bone
        n_s = max(1, round(math.dist(a, b) / 3.0))
        for i in range(n_s):
            p0, p1 = lerp(a, b, i / n_s), lerp(a, b, (i + 1) / n_s)
            r = radii[j] + (radii[j + 1] - radii[j]) * (i + 0.5) / n_s
            rod(m, bn, p0, p1, max(1, round(2 * r)), M("tail" if j < len(pts) - 2 else "tail_tip"), extend=0.8)
    anchors["tail"] = tl
    anchors["tail_tip"] = tip_bone
    anchors["tail_pts"] = pts
    return anchors


def quadruped(m, mats, name, length=30.0, body_y=16.0, body_rx=6.0, body_ry=6.0, chest_bulk=1.1, neck=((0, 22, -14),
              (0, 27, -19)), head_len=9.0, head_w=4.0, head_h=4.4, snout=0.5, mouth_open=8, teeth=0, leg_len=None,
              leg_bulk=1.0, paw="paw", tail=((0, 18, 16), (0, 16, 22), (0, 12, 27)), tail_r=(2.4, 1.8, 1.2),
              toes=3, claws=True):
    """A four-legged beast: horizontal body slices (deeper chest, tucked waist), a neck, a head with a snout and
    hinged jaw, four jointed legs (front legs straight, hind legs with a hock) ending in toed paws, and a tail.
    Legs are named leg_front_left/right and leg_back_left/right (the rig walks them in pairs)."""
    def M(k):
        return mats.get(k) or mats["skin"]

    top = m.bone(name, None, (0, 0, 0))
    bd = m.bone("body", top, (0, body_y, 0))
    z0 = -length / 2
    n = 8
    for i in range(n):
        t = (i + 0.5) / n
        prof = 1.0 + (chest_bulk - 1.0) * max(0.0, 1 - t * 2.2) - 0.14 * math.sin(t * math.pi * 1.6) ** 4
        rx, ry = body_rx * prof, body_ry * prof
        cy = body_y + 0.8 * (1 - t)
        slab_z(m, bd, 0, cy, z0 + i * length / n - 0.3, z0 + (i + 1) * length / n + 0.3, rx, ry, M("skin"))
        m.box(bd, -rx * 0.55, cy - ry - 0.8, z0 + i * length / n, rx * 0.55, cy - ry + 1.0, z0 + (i + 1) * length / n,
              M("belly"))
    nk = m.bone("neck", bd, (0, body_y + body_ry * 0.4, z0 + 2))
    pts = [(0, body_y + body_ry * 0.3, z0 + 3)] + list(neck)
    for a, b in zip(pts, pts[1:]):
        rod(m, nk, a, b, max(3, round(body_rx * 1.1)), M("neck"), extend=1.0)
    hx, hy, hz = neck[-1]
    hd = m.bone("head", nk, neck[-1])
    m.round_box(hd, 0, hz - head_len * 0.15, head_w, head_len * 0.32, hy - head_h * 0.4, hy + head_h * 0.7, M("head"),
                cut=max(1, round(head_w * 0.35)))
    mouth_y = hy - head_h * 0.35
    sf = hz - head_len * 0.15 - head_len * 0.32 - head_len * snout
    jw = jaws(m, hd, "jaw", head_w * 0.62, mouth_y, hz - head_len * 0.25, sf, M, open_deg=mouth_open, teeth=teeth,
              upper_h=head_h * 0.5, lower_h=head_h * 0.35)
    anchors = {"top": top, "body": bd, "neck": nk, "head": hd, "jaw": jw, "head_c": (0, hy, hz - head_len * 0.15),
               "eye": (head_w, hy + head_h * 0.25, hz - head_len * 0.35), "mouth_y": mouth_y, "snout_front": sf,
               "skull_top": hy + head_h * 0.7}
    L = body_y - body_ry * 0.4 if leg_len is None else leg_len
    for front, zz in ((True, z0 + length * 0.16), (False, -z0 - length * 0.16)):
        for sx in (1, -1):
            nm = f"leg_{'front' if front else 'back'}_{'left' if sx > 0 else 'right'}"
            hip = (sx * body_rx * 0.72, body_y - body_ry * 0.2, zz)
            lg = m.bone(nm, top, hip)
            lb = leg_bulk * (1.08 if not front else 1.0)
            m.round_box(lg, hip[0], zz, 2.6 * lb, 3.2 * lb, hip[1] - L * 0.45, hip[1] + body_ry * 0.6,
                        M("leg_upper"), cut=1)
            if front:
                el = (hip[0], hip[1] - L * 0.5, zz + 0.8)
                wr = (hip[0], 2.2, zz - 0.4)
            else:
                el = (hip[0], hip[1] - L * 0.42, zz + 2.6)
                wr = (hip[0], 2.2, zz + 0.4)
            rod(m, lg, (hip[0], hip[1] - L * 0.3, zz), el, max(2, round(3.4 * lb)), M("leg_upper"), extend=0.8)
            rod(m, lg, el, wr, max(2, round(2.6 * lb)), M("leg_lower"), extend=0.6)
            m.box(lg, wr[0] - 1.8 * lb, 0, wr[2] - 2.6 * lb, wr[0] + 1.8 * lb, 2.4, wr[2] + 1.4 * lb, M(paw))
            for t in range(toes):
                tx = wr[0] + (t - (toes - 1) / 2) * 1.2 * lb
                if claws:
                    spike(m, lg, (tx, 0.8, wr[2] - 2.6 * lb), (0, -0.3, -1), 0.9, 1.6 * lb, M("claw"))
            anchors[nm] = {"bone": lg, "hip": hip, "elbow": el, "wrist": wr}
    tl = m.bone("tail", bd, (0, body_y + body_ry * 0.3, -z0))
    tpts = [(0, body_y + body_ry * 0.3, -z0 - 1)] + list(tail)
    trad = [tail_r[0] * 1.2] + list(tail_r)
    for j, (a, b) in enumerate(zip(tpts, tpts[1:])):
        rod(m, tl, a, b, max(1, round(2 * (trad[j] + trad[j + 1]) / 2)), M("tail"), extend=0.8)
    anchors["tail"] = tl
    anchors["tail_pts"] = tpts
    anchors["length"] = length
    return anchors
