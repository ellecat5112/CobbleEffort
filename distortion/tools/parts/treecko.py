"""Treecko line (Grass -> Fire): natural disaster, a firestorm. The leafy tail is a sheet of flame, the crest and
Grovyle's great head leaf burn, Sceptile's seeds are molten and its arm blades are flame."""
from __future__ import annotations

from _materials import Flame, Glow, LavaRock

LINE = ["treecko", "grovyle", "sceptile"]
RECOLOUR = {"dst": 18, "dst_shiny": 45, "width": 60}        # green -> ember red-orange


def build(kit):
    kit.layer("flames", frames=4, fps=8)
    fire = Flame("flames")
    if kit.model == "treecko":
        # the tail is magma, cracked and glowing, with flames licking up from it; the crest smoulders
        kit.reskin(LavaRock("flames", crack=0.2), *kit.named("tail_left", "tail_right"), "bone", "bone2", "bone3")
        for side in ("tail_left2", "tail_right2"):
            lo, hi = kit.bbox(side)
            kit.cross(side, ((lo[0] + hi[0]) / 2, hi[1] - 0.5, (lo[2] + hi[2]) / 2), 4, 6, fire)
    elif kit.model == "grovyle":
        kit.reskin(fire, *kit.named("leaf", "arm_leaf", "tail_left", "tail_right"))
    else:
        kit.reskin(Glow("flames"), *kit.named("bud_"))
        kit.reskin(fire, *kit.named("arm_leaf", "tail_leaves"))
