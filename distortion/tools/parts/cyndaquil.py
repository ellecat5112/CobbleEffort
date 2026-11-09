"""Cyndaquil line (Fire -> Water): sea life, sea anemones. Every flame (the back, the head, Typhlosion's collar,
Hisuian Typhlosion's great mane) becomes anemone tentacles in the flames' own shapes: deep magenta at the base, pink,
teal tips; the glow goes."""
from __future__ import annotations

from _materials import sealife_from_layers

LINE = ["cyndaquil", "quilava", "typhlosion"]
RECOLOUR = {"dst": 205, "dst_shiny": 250, "width": 50}      # cream -> sea-foam blue (the dark back stays)


def build(kit):
    kit.op(sealife_from_layers())
    kit.drop_layers.add("emissive")
