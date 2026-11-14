"""Kegguard, the Cask Dog Pokémon (Normal/Ice), Stumblepup evolved, a Liquor Meadows Pokémon (the user's design): a
sturdy, thick-furred mountain dog, white with chestnut patches and a mask, heavy droopy jowls and sleepy eyes, rosy
cheeks and a reinforced, iron-banded cask strapped under its chin.

Shiny: black and white with a golden keg.

Front is -z, y is up. 26 units tall; baseScale 0.8 (1.4 m).
"""
from __future__ import annotations

from _boxmodel import Model
from _hound import P, SHINY, dog, ramp, solid  # noqa: F401

SCALE = 0.8
HITBOX = [1.3, 1.6]
KIND = "quadruped"
K = 3
HEIGHT = 26
LOOK = "a sturdy thick-furred mountain dog with heavy jowls, sleepy eyes, rosy cheeks and an iron-banded cask under its chin"


def build() -> Model:
    return dog(Model("kegguard"), 2.0, True)
