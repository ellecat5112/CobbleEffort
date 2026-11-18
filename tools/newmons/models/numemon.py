"""Numemon (a Digimon of the CobbleEffort: Digital crossover; after the official art on wikimon.net): the sewer slug: a
glossy lime-green blob of slime with blue patches pooling at its base, two bloodshot eyes on long stalks, a huge
gaping mouth of big square teeth and a long lolling pink tongue. 15 blocks tall.

Front is -z, y is up. 30 units tall; Adult stage. Built by _numemon.make(look="numemon").
"""
from _digi import sized
from _numemon import make

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "a glossy lime-green slime blob with blue patches, eyes on stalks, a huge gaping mouth of square teeth and a lolling tongue"
build = make("numemon", "numemon")
