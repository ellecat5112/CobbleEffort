"""Froakie line (Water -> Grass, Greninja Grass/Fairy): plant inspiration, moss and vines. The frubbles are soft moss,
and Greninja's tongue scarf is a vine."""
from __future__ import annotations

from _materials import LEAF_RAMP, MOSS_RAMP, Remap

LINE = ["froakie", "frogadier", "greninja"]
RECOLOUR = {"dst": 108, "dst_shiny": 80, "width": 55}


def build(kit):
    kit.reskin(Remap(*MOSS_RAMP), *kit.named("frubble", "bubble", "back_bubbles", "chest_bubble", "nose_bubble"))
    if kit.model == "greninja":
        kit.reskin(Remap(*LEAF_RAMP), *kit.named("tongue"))
