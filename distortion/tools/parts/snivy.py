"""Snivy line (Grass -> Fire): natural disaster, a lava flow. The tail leaves are flame, the neck leaves a collar of
glowing magma, and Serperior's long tail is molten rock cracked with lava."""
from __future__ import annotations

from _materials import Flame, Glow, LavaRock

LINE = ["snivy", "servine", "serperior"]
RECOLOUR = {"dst": 20, "dst_shiny": 44, "width": 55}


def build(kit):
    kit.layer("flames", frames=4, fps=8)
    fire = Flame("flames")
    kit.reskin(fire, *kit.named("tail_leaf", "back_leaf", "head_leaf"))
    kit.reskin(Glow("flames"), *kit.named("neck_leaf", "neck_leave"))
    if kit.model == "serperior":
        kit.reskin(LavaRock("flames", crack=0.2), *[f"segment{i}" for i in range(5, 10) if kit.has(f"segment{i}")])
