"""Suicune (Water -> Grass): a weeping willow. Its blue turns green, its long ribbons are trailing willow vines, its
purple mane is wisteria blossom and its crystal crest is a leaf."""
from __future__ import annotations

from _materials import LEAF_RAMP, Remap

LINE = ["suicune"]
RECOLOUR = {"dst": 110, "dst_shiny": 80, "width": 40, "src": 192}
WISTERIA = Remap([(110, 70, 160), (186, 150, 230), (240, 226, 255)], [(170, 70, 120), (236, 150, 190), (255, 230, 240)])
WILLOW = Remap([(52, 96, 40), (120, 170, 80), (200, 230, 150)], [(60, 100, 100), (120, 176, 160), (200, 236, 220)])


def build(kit):
    if kit.model != "suicune":
        raise KeyError(kit.model)
    kit.reskin(WILLOW, *kit.named("left_tail", "right_tail"))
    kit.reskin(WISTERIA, *kit.named("hair"))
    kit.reskin(Remap(*LEAF_RAMP), *kit.named("crest"))
