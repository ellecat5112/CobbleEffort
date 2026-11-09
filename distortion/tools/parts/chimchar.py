"""Chimchar line (Fire -> Water, Monferno/Infernape Water/Psychic): sea life, jellyfish. The flames on the tail and
Infernape's crown are jellyfish tendrils, violet fading to pale tips; the glow goes."""
from __future__ import annotations

from _materials import JELLY_RAMP, sealife_from_layers

LINE = ["chimchar", "monferno", "infernape"]
RECOLOUR = {"dst": 205, "dst_shiny": 250, "width": 50}


def build(kit):
    kit.op(sealife_from_layers(ramp=JELLY_RAMP))
    kit.drop_layers.add("emissive")
