"""Chespin line (Grass -> Fire, Chesnaught Fire/Psychic): natural disaster, a meteor strike. The spiky hood is a meteor
cracked with glowing lava, Chesnaught's shell and shields are meteorite plating and its spikes burn."""
from __future__ import annotations

from _materials import Flame, LavaRock

LINE = ["chespin", "quilladin", "chesnaught"]
RECOLOUR = {"dst": 18, "dst_shiny": 44, "width": 55}


def build(kit):
    kit.layer("flames", frames=4, fps=8)
    rock = LavaRock("flames", crack=0.18)
    if kit.model == "chespin":
        kit.reskin(rock, *kit.named("head_spike"))
    elif kit.model == "quilladin":
        kit.reskin(rock, "hair", "spike_left", "spike_right")
    else:
        kit.reskin(rock, *kit.named("shell", "shield"))
        kit.reskin(Flame("flames"), *kit.named("spike"))
