"""Bulbasaur line (Grass/Poison -> Fire/Ground): natural disaster, a wildfire. The bulb is gone, raging animated flames
burst from a charred stump in its place; the leaves are charred and burning at the edges; Venusaur's flower is an
inferno on a cracked, smouldering trunk."""
from __future__ import annotations

from _materials import Charred, Flame, LavaRock

LINE = ["bulbasaur", "ivysaur", "venusaur"]
RECOLOUR = {"dst": 14, "dst_shiny": 40, "width": 60, "near": 165}   # teal skin -> ember red-orange


def flames(kit, bone, base, size, layer="flames"):
    """A blaze: one big crossed flame and two smaller ones leaning out."""
    x, y, z = base
    kit.cross(bone, (x, y, z), size * 0.7, size, Flame(layer))
    kit.cross(bone, (x - size * 0.22, y, z + size * 0.12), size * 0.4, size * 0.62, Flame(layer, tongues=1.1), turn=35)
    kit.cross(bone, (x + size * 0.2, y, z - size * 0.1), size * 0.4, size * 0.7, Flame(layer, tongues=1.2), turn=-30)


def build(kit):
    kit.layer("flames", frames=4, fps=8)
    burn = Charred("flames")
    if kit.model.startswith("bulbasaur"):
        lo, hi = kit.bbox("bulb")
        kit.hide("bulb")
        cx, cz = (lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2
        kit.box("bulb", [cx - 3, lo[1] + 0.5, cz - 3], [6, 2, 6], LavaRock("flames"))
        flames(kit, "bulb", (cx, lo[1] + 2.0, cz), 13)
    elif kit.model.startswith("ivysaur"):
        lo, hi = kit.bbox("bulb")
        kit.hide("bulb")
        cx, cz = (lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2
        kit.box("bulb", [cx - 3.5, lo[1], cz - 3.5], [7, 3, 7], LavaRock("flames"))
        flames(kit, "bulb", (cx, lo[1] + 2.5, cz), 17)
        kit.reskin(burn, *[b["name"] for b in kit.bones if b["name"].startswith("leaf_")])
    else:
        kit.reskin(LavaRock("flames"), "tree", "tree2", "tree3")
        lo, hi = kit.bbox("tree3")
        kit.hide("tree_crown")
        kit.reskin(burn, *[b["name"] for b in kit.bones if b["name"].startswith("leaf_")])
        kit.reskin(Flame("flames"), *[b["name"] for b in kit.bones if b["name"].startswith("petal_")])   # petals of fire
        cx, cz = (lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2
        flames(kit, "flower_top", (cx, hi[1] - 1, cz), 30)
