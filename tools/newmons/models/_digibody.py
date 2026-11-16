"""A dense humanoid body for the Digimon (CobbleEffort: Digital detail standard): 64 units tall to the top of the head,
built from anatomical pieces (pelvis, abdomen, ribcage, separate pectorals, neck, deltoids, biceps/triceps, forearms,
hands with jointed fingers and a thumb, thighs, knees, calves, shins and toed feet), each painted by its own shader
from a `mats` dict, so a Digimon module adds only what makes it itself (armour, head, hair, wings, weapons, tail).

humanoid(m, mats, **proportions) -> anchors: bone names and key points for attaching parts.

mats keys (any missing key falls back to "skin"): skin, chest, abs, pelvis, neck, deltoid, upper_arm, forearm, hand,
finger, thigh, knee, shin, calf, foot, toe.
Proportions: bulk (overall width), arm_bulk, leg_bulk, digitigrade (bird/goat legs bent back), claws (finger tips
become claws, `claw` shader key), talons (toes become talons, `talon` key), toes (count), fingers (count).
"""
from __future__ import annotations

import math

from _boxmodel import rod, spike


def shell(m, bone, c, r, y0, y1, a0, a1, n, t, shader, tilt=0.0):
    """A curved plate round a vertical axis through c: n boxes along the arc from angle a0 to a1 (degrees, 0 = front
    -z, positive toward +x), radius r, height y0..y1, thickness t; `tilt` leans the whole shell's top outward."""
    cx, cz = c[0], c[2]
    da = (a1 - a0) / n
    w = 2 * r * math.sin(math.radians(abs(da)) / 2) + 0.6
    for i in range(n):
        th = math.radians(a0 + da * (i + 0.5))
        px, pz = cx + r * math.sin(th), cz - r * math.cos(th)
        m.box(bone, px - w / 2, y0, pz - t / 2, px + w / 2, y1, pz + t / 2, shader,
              rotation=(tilt, -math.degrees(th), 0), pivot=(px, (y0 + y1) / 2, pz))


def dome(m, bone, c, r, h, shader, layers=4, squash=1.0):
    """A rounded cap: stacked round slices narrowing toward the top (for pauldrons, helmets, knee caps)."""
    cx, cy, cz = c
    for i in range(layers):
        f0 = i / layers
        rr = r * math.sqrt(max(0.05, 1 - f0 * f0))
        m.round_box(bone, cx, cz, rr, rr * squash, cy + h * f0 - 0.02 * i, cy + h * (f0 + 1 / layers), shader,
                    cut=max(1, round(rr * 0.35)))


def humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.0, digitigrade=False, claws=False, talons=False, toes=3, fingers=4,
             hand_pose="relaxed", name=None, chest_depth=1.0):
    def M(k):
        return mats.get(k) or mats["skin"]

    b, ab, lb = bulk, arm_bulk * bulk, leg_bulk * bulk
    top = m.bone(name or m.name, None, (0, 0, 0))
    bd = m.bone("body", top, (0, 34, 0))
    # pelvis, abdomen, ribcage: each rounded; pectorals as their own slabs on the front of the ribcage
    m.round_box(bd, 0, 0.4, 4.6 * b, 3.4 * b, 30.5, 35.5, M("pelvis"), cut=1)
    m.round_box(bd, 0, 0.2, 3.8 * b, 3.0 * b * chest_depth, 35.0, 42.0, M("abs"), cut=1)
    m.round_box(bd, 0, 0.0, 5.4 * b, 3.6 * b * chest_depth, 41.5, 51.0, M("chest"), cut=1)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 0.4, sx * 5.0 * b))
        m.box(bd, x0, 44.0, -3.6 * b * chest_depth - 1.0, x1, 50.0, -3.6 * b * chest_depth + 0.5, M("chest"))
    m.round_box(bd, 0, 0.6, 2.0 * b, 2.0 * b, 50.5, 55.0, M("neck"), cut=1)          # neck
    for sx in (-1, 1):                                                               # trapezius slopes
        x0, x1 = sorted((sx * 1.8 * b, sx * 5.2 * b))
        m.box(bd, x0, 50.0, -1.2, x1, 52.5, 2.8, M("chest"), rotation=(0, 0, -sx * 14), pivot=(sx * 1.8 * b, 50, 0))
    anchors = {"top": top, "body": bd, "chest_top": 51.0, "chest_front": -3.6 * b * chest_depth - 1.0,
               "neck_top": 55.0, "shoulder_x": 6.8 * b}
    # arms: deltoid, upper arm (biceps front, triceps back), elbow, forearm (tapering), hand
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        sh = (sx * 6.6 * b, 49.5, 0.3)
        a = m.bone(nm, bd, sh)
        m.round_box(a, sx * 7.0 * b, 0.3, 2.6 * ab, 2.6 * ab, 46.0, 52.0, M("deltoid"), cut=1)
        el = (sx * 8.9 * b, 38.0, -0.2)
        rod(m, a, (sh[0] + sx * 0.6, 47.0, 0.3), el, round(3.4 * ab), M("upper_arm"), extend=0.4)
        rod(m, a, (sh[0] + sx * 0.9, 45.5, -0.9), (el[0], 40.0, -0.4), round(2.2 * ab), M("upper_arm"), extend=0.2)
        wr = (sx * 10.2 * b, 28.5, -2.6)
        rod(m, a, el, wr, round(3.0 * ab), M("forearm"), extend=0.5)
        rod(m, a, (el[0], 36.0, -0.6), (wr[0], 31.0, -0.9), round(2.2 * ab), M("forearm"), extend=0.2)
        hx, hy, hz = wr[0], 26.6, wr[2]
        m.box(a, hx - 1.2 * ab, hy - 3.6, hz - 1.6 * ab, hx + 1.2 * ab, hy + 0.4, hz + 1.4 * ab, M("hand"))
        for f in range(fingers):                                              # fingers: two segments each
            fz = hz - 1.2 * ab + f * (2.6 * ab / max(fingers - 1, 1))
            curl = 0.5 if hand_pose == "relaxed" else 0.95 if hand_pose == "fist" else 0.15
            p0 = (hx, hy - 3.6, fz)
            p1 = (hx + sx * 0.2, hy - 5.4, fz - curl * 0.8)
            p2 = (hx + sx * 0.3, hy - 6.6 + curl * 1.4, fz - curl * 1.8)
            rod(m, a, p0, p1, 1, M("finger"), extend=0.3)
            if claws:
                spike(m, a, p1, (sx * 0.05, -1, -curl), 0.9, 1.8, M("claw"), tip=0.25)
            else:
                rod(m, a, p1, p2, 1, M("finger"), extend=0.25)
        rod(m, a, (hx - sx * 0.3, hy - 1.5, hz - 1.5 * ab), (hx - sx * 0.6, hy - 3.6, hz - 2.6 * ab), 1, M("finger"),
            extend=0.3)                                                       # thumb
        anchors[nm] = {"bone": a, "shoulder": sh, "elbow": el, "wrist": wr, "hand": (hx, hy - 2, hz)}
    # legs: thigh (quads), knee, calf + shin, foot with toes
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        hip = (sx * 2.7 * b, 31.5, 0.4)
        lg = m.bone(nm, top, hip)
        kn = (sx * 3.1 * b, 18.5, -0.6 if not digitigrade else -2.4)
        rod(m, lg, hip, kn, round(4.6 * lb), M("thigh"), extend=0.8)
        rod(m, lg, (hip[0], 29.0, -1.6), (kn[0], 21.5, kn[2] - 1.2), round(2.6 * lb), M("thigh"), extend=0.3)
        m.round_box(lg, kn[0], kn[2] - 0.4, 1.8 * lb, 1.6 * lb, 16.5, 20.5, M("knee"), cut=1)
        if digitigrade:
            hock = (kn[0], 8.0, 3.6)
            rod(m, lg, kn, hock, round(3.4 * lb), M("shin"), extend=0.5)
            ank = (kn[0], 2.4, 0.6)
            rod(m, lg, hock, ank, round(2.4 * lb), M("shin"), extend=0.4)
        else:
            ank = (kn[0], 3.0, 0.0)
            rod(m, lg, kn, ank, round(3.6 * lb), M("shin"), extend=0.5)
            rod(m, lg, (kn[0], 15.5, 1.4), (kn[0], 7.5, 1.0), round(2.6 * lb), M("calf"), extend=0.3)
        fx, fz = ank[0], ank[2]
        m.box(lg, fx - 1.8 * lb, 0.0, fz - 3.2 * lb, fx + 1.8 * lb, 2.6, fz + 1.8 * lb, M("foot"))
        for t in range(toes):
            tx = fx - 1.3 * lb + t * (2.6 * lb / max(toes - 1, 1))
            if talons:
                spike(m, lg, (tx, 0.9, fz - 3.2 * lb), (0, -0.25, -1), 1.2, 3.4, M("talon"), tip=0.3)
            else:
                m.box(lg, tx - 0.5, 0.0, fz - 4.4 * lb, tx + 0.5, 1.4, fz - 3.0 * lb, M("toe"))
        anchors[nm] = {"bone": lg, "hip": hip, "knee": kn, "ankle": ank}
    return anchors


def cape(m, bone, top, width, length, shader, z=3.0, flare=0.6, panels=6, sweep=(0.0, 0.0), seed=1):
    """A cape hanging from the shoulders: `panels` vertical planes side by side, each hanging back at an angle that
    grows outward (flare) and swept by `sweep` (x, z offset of the hem), with a ragged hem cut out (tattered cloth)."""
    from _digidetail import cutout, local, noise2
    top_y = top
    pw = width / panels

    def torn(x, y, z_, face, box):
        u, v, W, H = local(x, y, z_, face, box)
        f = (box.lo[0] + u) * 0.9
        rag = 0.12 + 0.18 * noise2(f, seed) + 0.1 * abs(math.sin(f * 2.3 + seed))
        hole = noise2(f * 1.7, (box.lo[1] + v) * 0.6 + seed * 3) > 0.86 and v / max(H, 1e-6) < 0.4
        return v / max(H, 1e-6) > rag and not hole

    sh = cutout(torn, shader)
    for i in range(panels):
        x0 = -width / 2 + i * pw
        t = (i + 0.5) / panels - 0.5
        zz = z + abs(t) * 3.0 * flare
        m.box(bone, x0 - 0.2, top_y - length, zz, x0 + pw + 0.2, top_y, zz, sh,
              rotation=(8 + 14 * abs(t) * flare * 2 + sweep[1], 0, t * 10 * flare + sweep[0]),
              pivot=(x0 + pw / 2, top_y, zz))
