"""Duftmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Duftmon awakened by the X-Antibody, bulkier in brown armour with teal studs and purple spikes, a violet-lined cape, a blade of pink light and the gold-tipped tail.
35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from _digi import sized
from _duftmon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a bulky brown-armoured leopard knight with teal studs, purple spikes, a violet cape, a pink light blade and a blonde mane"
build = make("duftmonxantibody", "x")
