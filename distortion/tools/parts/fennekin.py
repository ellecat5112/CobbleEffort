"""Fennekin line (Fire -> Water, Delphox Water/Dark): sea life, a nudibranch (sea slug). The ear tufts are frilly
nudibranch cerata, violet tipped with orange, and the flames on Braixen's and Delphox's wands are anemone tentacles."""
from __future__ import annotations

from _materials import ANEMONE, NUDI_RAMP, Remap, sealife_from_layers

LINE = ["fennekin", "braixen", "delphox"]
RECOLOUR = {"dst": 210, "dst_shiny": 250, "width": 50}


def build(kit):
    kit.reskin(Remap(*NUDI_RAMP), *kit.named("ear_ruff", "ear_left_ruff", "ear_right_ruff"))
    if kit.model != "fennekin":
        kit.op(sealife_from_layers(ramp=ANEMONE))
        kit.drop_layers.add("emissive")
        kit.reskin(Remap(*ANEMONE, invert=True), *kit.named("fire"))
