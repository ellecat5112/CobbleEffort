"""Mudkip line (Water -> Grass, Marshtomp/Swampert Grass/Water): plant inspiration, a lotus pond. The fins are lily
pads, the orange gills are lotus petals, and a lotus flower blooms on Mudkip's head."""
from __future__ import annotations

from _materials import Cutout, Remap, petal

LINE = ["mudkip", "marshtomp", "swampert"]
RECOLOUR = {"dst": 105, "dst_shiny": 75, "width": 55}       # blue -> pond green
PAD = Remap([(36, 92, 40), (84, 162, 66), (168, 226, 128)], [(40, 96, 100), (90, 166, 150), (176, 232, 214)])
LOTUS = Remap([(170, 56, 118), (240, 140, 190), (255, 226, 240)], [(150, 110, 40), (240, 200, 90), (255, 246, 200)])
BLOOM = Cutout(petal, [(200, 70, 140), (246, 150, 200), (255, 232, 244)], [(200, 150, 50), (246, 210, 100), (255, 248, 210)])


def build(kit):
    kit.reskin(PAD, *kit.named("fin", "tail", "head_fin", "tail_fin"))
    kit.reskin(LOTUS, *kit.named("cheek", "check"))
    if kit.model == "mudkip":
        lo, hi = kit.bbox("head")
        for turn in (0, 45):
            kit.cross("head", (0, hi[1] - 0.2, (lo[2] + hi[2]) / 2 + 1), 3, 3, BLOOM, turn=turn)
