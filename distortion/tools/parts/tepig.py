"""Tepig line (Fire -> Water, Pignite/Emboar Water/Psychic): sea life, pearls and coral. Tepig's curled tail ball is a
pearl, and Emboar's flaming beard and shoulders are coral; the glow goes."""
from __future__ import annotations

from _materials import CORAL_RAMP, Remap, sealife_from_layers

LINE = ["tepig", "pignite", "emboar"]
RECOLOUR = {"dst": 205, "dst_shiny": 250, "width": 50}
PEARL = Remap([(170, 170, 196), (230, 226, 240), (255, 255, 255)], [(196, 170, 120), (240, 224, 190), (255, 252, 236)])


def build(kit):
    kit.op(sealife_from_layers(names=("emissive", "glow", "fire"), ramp=CORAL_RAMP))
    kit.drop_layers.update({"emissive", "glow"})
    if kit.model == "tepig":
        kit.reskin(PEARL, *kit.named("tail_orb"))
    if kit.model == "emboar":
        kit.reskin(Remap(*CORAL_RAMP, invert=True), *kit.named("fire"))
