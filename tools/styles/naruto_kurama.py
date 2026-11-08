"""Naruto collection, 'Kurama' (the Nine-Tails, for the Vulpix line): orange fox fur, black eye markings and ear tips, red slit eyes, and a flickering orange chakra glow on every edge. Shiny: gold Kurama Link Mode with black seal lines."""
from ._shinobi import CHAKRA, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso/ear face positions
EXTRA_LAYERS = [CHAKRA]
retexture, extra_layer = make("kurama")
