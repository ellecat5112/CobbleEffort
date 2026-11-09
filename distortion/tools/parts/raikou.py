"""Raikou (Electric -> Ground): a sandstorm. Its yellow turns desert ochre, the storm-cloud mane is a billowing dust
cloud and the lightning tail is stone."""
from __future__ import annotations

from _materials import Remap

LINE = ["raikou"]
RECOLOUR = {"dst": 30, "dst_shiny": 18, "width": 50, "sat": 0.5, "val": 0.72}
DUST = Remap([(92, 72, 56), (156, 130, 100), (214, 196, 160)], [(80, 70, 90), (140, 128, 150), (206, 196, 214)])
STONE = Remap([(70, 64, 60), (124, 116, 108), (180, 172, 160)], [(64, 60, 80), (116, 110, 140), (176, 170, 200)])


def build(kit):
    if kit.model != "raikou":
        raise KeyError(kit.model)
    kit.reskin(DUST, *kit.named("middle_fur", "left_fur", "right_fur", "outer_left_fur", "outer_right_fur"))
    kit.reskin(STONE, *kit.named("tail"))
