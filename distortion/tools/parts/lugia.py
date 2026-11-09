"""Lugia (Psychic/Flying -> Dark/Electric): a storm at night. A photographic negative of itself (its white turns
black, its blue amber), with lightning crackling along its dorsal plates."""
from __future__ import annotations

from _materials import ELECTRIC, Glow

LINE = ["lugia"]
RECOLOUR = "negative"


def build(kit):
    if kit.model != "lugia":
        raise KeyError(kit.model)
    kit.layer("storm", frames=4, fps=10)
    kit.reskin(Glow("storm", ELECTRIC), *kit.named("plate"))
