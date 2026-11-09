"""Entei (Fire -> Water): sea life, a lionfish. Its fiery brown turns sea blue, its mane and fluff are a lionfish's
striped venomous spines, and its golden crest and mask are pearl."""
from __future__ import annotations

from _materials import Remap, Stripes

LINE = ["entei"]
RECOLOUR = {"dst": 212, "dst_shiny": 250, "width": 55}
SPINES = Stripes([(196, 60, 52), (246, 228, 210)], [(70, 60, 170), (226, 220, 250)], width=2)
PEARL = Remap([(170, 170, 196), (230, 226, 240), (255, 255, 255)], [(196, 170, 120), (240, 224, 190), (255, 252, 236)])


def build(kit):
    if kit.model != "entei":
        raise KeyError(kit.model)
    kit.reskin(SPINES, *kit.named("middle_mane", "left_mane", "right_mane", "left_fluff", "right_fluff", "top_fluff",
                                  "left_spike", "right_spike", "left_bottom_spike", "right_bottom_spike", "cloud"))
    kit.reskin(PEARL, *kit.named("crest", "mask", "forehead"))
