{
num: -3060,
accuracy: 90,
basePower: 35,
category: "Special",
name: "Yeast Bubble",
pp: 15,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
volatileStatus: 'partiallytrapped',
onHit(target, source) {
  source.addVolatile('yeastbubble');
},
condition: {
  duration: 5,
  onStart(pokemon) {
    this.add('-start', pokemon, 'Yeast Bubble');
  },
  onResidualOrder: 6,
  onResidual(pokemon) {
    this.heal(pokemon.baseMaxhp / 16);
  },
  onEnd(pokemon) {
    this.add('-end', pokemon, 'Yeast Bubble', '[silent]');
  }
},
secondary: null,
target: "normal",
type: "Fairy",
desc: "Traps and damages the target for 4-5 turns. The user restores 1/16 of its maximum HP at the end of each turn for 5 turns.",
shortDesc: "Traps/damages for 4-5 turns; user heals 1/16 each turn.",
contestType: "Cute"
}
