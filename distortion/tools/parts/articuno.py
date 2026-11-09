"""Articuno (Ice/Flying -> Fire/Electric): a phoenix. Its icy blue turns to flame colours and its long tail and crest
burn."""
from __future__ import annotations

from _materials import Flame

LINE = ["articuno"]
RECOLOUR = {"dst": 18, "dst_shiny": 300, "width": 60}


def build(kit):
    kit.layer("flames", frames=4, fps=8)
    kit.reskin(Flame("flames"), *kit.named("tail"), *kit.named("crown"))
