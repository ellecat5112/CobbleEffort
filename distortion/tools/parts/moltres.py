"""Moltres (Fire/Flying -> Water/Electric): a tidal wave. Its flames are water in their own shapes, deep blue cresting
to white foam, and its orange turns ocean blue; the glow goes."""
from __future__ import annotations

from _materials import sealife_from_layers

LINE = ["moltres"]
RECOLOUR = {"dst": 210, "dst_shiny": 250, "width": 55}
WAVE = ([(20, 60, 150), (60, 150, 230), (236, 250, 255)], [(70, 30, 140), (150, 110, 230), (246, 236, 255)])


def build(kit):
    kit.op(sealife_from_layers(ramp=WAVE))
    kit.drop_layers.add("emissive")
