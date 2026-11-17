"""Cannonbeemon (Aircraft Carrier) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard
after the official manga art on wikimon.net): the carrier version of Cannonbeemon, white and grey, with extra
honeycomb pods along a longer flight deck. Perfect stage (floats).

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

from cannonbeemon import HEIGHT, HITBOX, K, KIND, SCALE, make  # noqa: F401

LOOK = ("the white-and-grey carrier version of the hornet fortress, with extra honeycomb pods along a longer flight "
        "deck")

build = make("cannonbeemonaircraftcarrier", carrier=True)
