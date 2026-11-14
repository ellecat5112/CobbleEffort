{
num: -3045,
accuracy: true,
basePower: 0,
category: "Status",
name: "Distill",
pp: 10,
priority: 0,
flags: {snatch: 1, metronome: 1},
onHit(pokemon) {
  let purified = 0;
  if (pokemon.status) {
    pokemon.cureStatus();
    purified++;
  }
  let s;
  for (s in pokemon.boosts) {
    if (pokemon.boosts[s] < 0) {
      pokemon.boosts[s] = 0;
      purified++;
    }
  }
  if (purified) this.add('-clearnegativeboost', pokemon, '[silent]');
  return this.boost({spa: purified ? 2 : 1}, pokemon, pokemon) !== false;
},
secondary: null,
target: "self",
type: "Steel",
desc: "The user is cured of its non-volatile status condition and loses its negative stat stages, then raises its Special Attack by 2 stages if anything was removed, otherwise by 1 stage.",
shortDesc: "Cures status and stat drops; +2 SpA if any were cleared, else +1.",
contestType: "Clever"
}
