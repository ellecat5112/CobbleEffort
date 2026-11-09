"""Litten line (Fire -> Water, Incineroar Water/Fairy): sea life, a shark. A dorsal fin rises from the back, and
Torracat's bell and Incineroar's flaming belt are coral; the glow goes."""
from __future__ import annotations

from _materials import CORAL_RAMP, Cutout, fin_rays, fin_shape, sealife_from_layers

LINE = ["litten", "torracat", "incineroar"]
RECOLOUR = {"dst": 210, "dst_shiny": 250, "width": 50}
FIN = Cutout(fin_shape, [(30, 50, 80), (70, 104, 140), (150, 190, 220)], [(60, 40, 90), (110, 80, 150), (190, 160, 230)], veins=fin_rays)
BACK = {"litten": ("torso", 6), "torracat": ("torso", 9), "incineroar": ("chest", 13)}


def build(kit):
    kit.op(sealife_from_layers(names=("emissive",), ramp=CORAL_RAMP))
    kit.drop_layers.add("emissive")
    bone, size = BACK[kit.model]
    lo, hi = kit.bbox(bone)
    kit.plane(bone, (0, hi[1] - 0.5, (lo[2] + hi[2]) / 2 + size * 0.15), size, size * 0.8, FIN, facing="x")
