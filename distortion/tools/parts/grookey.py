"""Grookey line (Grass -> Fire): natural disaster, a wildfire. The sticks are burning torches, the head leaves and
Rillaboom's leafy hair are flame, and Rillaboom's stump drum is magma."""
from __future__ import annotations

from _materials import Flame, LavaRock

LINE = ["grookey", "thwackey", "rillaboom"]
RECOLOUR = {"dst": 20, "dst_shiny": 46, "width": 55}


def build(kit):
    kit.layer("flames", frames=4, fps=8)
    fire = Flame("flames")
    for stick in kit.named("stick"):
        lo, hi = kit.bbox(stick)
        # a flame at the stick's far end (sticks are held along different axes)
        ext = [hi[i] - lo[i] for i in range(3)]
        axis = ext.index(max(ext))
        tip = [(lo[i] + hi[i]) / 2 for i in range(3)]
        tip[axis] = hi[axis] if axis == 1 else lo[axis]
        kit.cross(stick, tuple(tip), 3, 5, fire)
    kit.reskin(fire, *kit.named("leaf", "mohawk", "hair_spike"))
    if kit.model == "rillaboom":
        kit.reskin(LavaRock("flames", crack=0.2), "drum")
