"""Stumblepup, the Rescue Pup Pokémon (Normal), a Liquor Meadows Pokémon (the user's design): a scruffy, lovable Saint
Bernard puppy, white with chestnut patches, big eyes, rosy cheeks and droopy ears, a tiny wooden keg on its red collar
and a wagging tail.

Shiny: black and white with a golden keg.

Front is -z, y is up. 13 units tall; baseScale 0.45 (0.45 m).
"""
from __future__ import annotations

from _boxmodel import Model
from _hound import P, SHINY, dog, ramp, solid  # noqa: F401

SCALE = 0.45
HITBOX = [0.7, 0.75]
KIND = "quadruped"
K = 6
HEIGHT = 13
LOOK = "a scruffy Saint Bernard puppy with rosy cheeks, droopy ears and a tiny wooden keg on its collar"


def build() -> Model:
    return dog(Model("stumblepup"), 1.0, False)
