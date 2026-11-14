{
onResidualOrder: 28,
onResidualSubOrder: 2,
onResidual(pokemon) {
  if (!pokemon.activeTurns) return;
  const stats = [];
  let s;
  for (s of ['atk', 'def', 'spa', 'spd', 'spe']) {
    if (pokemon.boosts[s] < 6) stats.push(s);
  }
  if (!stats.length) return;
  const boost = {};
  boost[this.sample(stats)] = 1;
  this.boost(boost, pokemon, pokemon);
},
flags: {},
name: "Aged Vintage",
rating: 4,
num: -3033
}
