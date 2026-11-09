"""Quaxly line (Water -> Grass, Quaquaval Grass/Psychic): plant inspiration, fern fronds. The swept hair, Quaxwell's
hair strings and Quaquaval's head plumes and water feathers are fern fronds."""
from __future__ import annotations

from _materials import LEAF_RAMP, Cutout, Remap, fern

LINE = ["quaxly", "quaxwell", "quaquaval"]
RECOLOUR = {"dst": 110, "dst_shiny": 80, "width": 55}


FROND = Cutout(fern, *LEAF_RAMP)


def build(kit):
    kit.reskin(Remap(*LEAF_RAMP), *kit.named("hair", "feather_head", "water_feather"))
    head = kit.find("head")
    lo, hi = kit.bbox(head)
    h = (hi[1] - lo[1]) * 0.7
    kit.cross(head, ((lo[0] + hi[0]) / 2, hi[1] - 0.3, (lo[2] + hi[2]) / 2), h * 0.6, h, FROND, turn=30)   # a fern frond
