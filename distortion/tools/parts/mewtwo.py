"""Mewtwo (Psychic -> Normal/Fighting, a specialised distortion by the user's design): the heavyweight bodybuilder.
Its slender arms are replaced by Conkeldurr's (Cobblemon's Conkeldurr model's arm geometry, fitted to Mewtwo's
joints), translucent pink for its Fighting typing, and its chest, waist, neck and thighs are bulked up."""
from __future__ import annotations

from _materials import Muscle

LINE = ["mewtwo"]
RECOLOUR = "keep"

# Conkeldurr's left arm (from Cobblemon's conkeldurr.geo.json): per Mewtwo bone, Conkeldurr's x span along the arm and
# its cubes (origin, size); its shoulder joint is at y 24.5, z -1.5
CONK_SHOULDER = (24.5, -1.5)
CONK = {
    "arm_left": ((7, 22), [([7, 17, -9], [6, 15, 15]), ([13, 20, -6.5], [9, 9, 10])]),          # deltoid, upper arm
    "arm_left2": ((22, 33), [([22, 20.5, -5.5], [7, 8, 8]), ([28, 22, -5], [5, 6, 7])]),       # forearm, wrist
    "hand_left": ((33, 45), [([33, 24, -5.5], [6, 4, 8]), ([39, 25, -0.5], [5, 3, 3]), ([41, 23, -0.5], [3, 5, 3]),
                             ([39, 25, -5.5], [6, 3, 3]), ([42, 23, -5.5], [3, 5, 3]), ([34, 23, -7], [4, 3, 3]),
                             ([38, 23, -7], [4, 3, 3])]),                                       # fist, fingers, thumb
}
THICK = 0.7          # Conkeldurr's arm girth, scaled to Mewtwo


def build(kit):
    if kit.model != "mewtwo":
        raise KeyError(kit.model)
    kit.layer("muscle", emissive=False, translucent=True, frames=1, fps=1)
    muscle = Muscle("muscle")
    # Mewtwo's joints along the arm (x), and its shoulder (y, z)
    joints = {"arm_left": (3.5, kit.bone("arm_left2")["pivot"][0]),
              "arm_left2": (kit.bone("arm_left2")["pivot"][0], kit.bone("hand_left")["pivot"][0]),
              "hand_left": (kit.bone("hand_left")["pivot"][0], kit.bone("hand_left")["pivot"][0] + 7)}
    sy, sz = kit.bone("arm_left")["pivot"][1], kit.bone("arm_left")["pivot"][2]
    for side in ("left", "right"):
        sign = 1 if side == "left" else -1
        kit.hide(f"arm_{side}", f"arm_{side}2", f"hand_{side}", deep=False)
        kit.hide(*[b for b in kit.descendants(f"hand_{side}")])
        for bone, ((c0, c1), cubes) in CONK.items():
            m0, m1 = joints[bone]
            k = (m1 - m0) / (c1 - c0)
            for (o, size) in cubes:
                x0 = m0 + (o[0] - c0) * k
                w = size[0] * k
                y0 = sy + (o[1] - CONK_SHOULDER[0]) * THICK
                z0 = sz + (o[2] - CONK_SHOULDER[1]) * THICK
                x = x0 if sign > 0 else -(x0 + w)
                kit.box(bone.replace("left", side), [x, y0, z0], [w, size[1] * THICK, size[2] * THICK], muscle)
    # the bodybuilder's bulk
    kit.bulk(1.8, "torso3")
    kit.bulk(1.0, "torso", "torso2")
    kit.bulk(0.6, "neck")
    kit.bulk(1.2, "leg_left", "leg_right")
