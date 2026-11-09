"""Zapdos (Electric/Flying -> Ground/Electric): a dust storm. Its yellow turns to desert ochre and its spiky crest and
feathers are sandstone."""
from __future__ import annotations

from _materials import Remap

LINE = ["zapdos"]
RECOLOUR = {"dst": 32, "dst_shiny": 15, "width": 50, "sat": 0.75, "val": 0.85}
SANDSTONE = Remap([(120, 84, 48), (190, 150, 96), (236, 210, 160)], [(110, 70, 60), (180, 120, 100), (230, 190, 170)])


def build(kit):
    kit.reskin(SANDSTONE, *kit.named("hair"))
