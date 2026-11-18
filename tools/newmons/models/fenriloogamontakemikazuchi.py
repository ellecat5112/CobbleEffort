"""Fenriloogamon: Takemikazuchi (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art
on wikimon.net): Fenriloogamon wreathed in green lightning, carrying a long green-bladed sword in its jaws, with four
silver thruster pods on its back trailing blue flame. 35 blocks tall.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from _digi import sized
from _fenriloogamon import make

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a huge armoured spirit-fire wolf wreathed in green lightning, a green-bladed sword in its jaws and four silver "
        "thruster pods on its back")
build = make("fenriloogamontakemikazuchi", take=True)
