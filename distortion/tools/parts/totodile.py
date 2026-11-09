"""Totodile line (Water -> Grass): plant inspiration, the Venus flytrap. Snapping traps sprout along the back; Feraligatr's
red spines turn to leaves."""
from __future__ import annotations

from _materials import Cutout, Flytrap, leaf, midrib

LINE = ["totodile", "croconaw", "feraligatr"]
RECOLOUR = {"dst": 100, "dst_shiny": 70, "width": 55}       # blue -> leaf green
LEAF = Cutout(leaf, [(40, 100, 38), (84, 160, 60), (160, 220, 120)], [(50, 110, 110), (100, 170, 160), (180, 230, 220)], veins=midrib)


def trap(kit, bone, base, size):
    """Two lobes opening upwards in a V."""
    kit.plane(bone, base, size * 0.8, size, Flytrap(), facing="x", rotation=[0, 0, 28])
    kit.plane(bone, base, size * 0.8, size, Flytrap(), facing="x", rotation=[0, 0, -28])


# where the traps grow (bone, then (x, y, z, size) on its back)
TRAPS = {"totodile": ("torso2", [(0, 14, 8.5, 7), (-3, 11, 8.3, 5), (3, 10.5, 8.3, 5)]),
         "croconaw": ("torso", [(0, 12, 5.3, 9), (-4.5, 8.5, 5.1, 6), (4.5, 8, 5.1, 6)]),
         "feraligatr": ("torso2", None)}


def build(kit):
    bone, spots = TRAPS[kit.model]
    if spots is None:
        lo, hi = kit.bbox(bone)
        spots = [(0, hi[1] - 2, hi[2] + 0.4, 12), (-6, hi[1] - 6, hi[2] + 0.3, 8), (6, hi[1] - 7, hi[2] + 0.3, 8)]
    for x, y, z, size in spots:
        trap(kit, bone, (x, y, z), size)
    if kit.model == "feraligatr":
        kit.reskin(LEAF, *kit.named("spike"))
