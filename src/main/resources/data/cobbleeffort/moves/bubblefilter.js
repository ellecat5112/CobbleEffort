{
num: -3021,
accuracy: 100,
basePower: 70,
category: "Special",
name: "Bubble Filter",
pp: 15,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
onAfterHit(target, pokemon, move) {
  if (!pokemon.hp) return;
  for (const c of ['spikes', 'toxicspikes', 'stealthrock', 'stickyweb', 'gmaxsteelsurge']) {
    if (pokemon.side.removeSideCondition(c)) {
      this.add('-sideend', pokemon.side, this.dex.conditions.get(c).name, '[from] move: Bubble Filter', '[of] ' + pokemon);
    }
  }
  for (const ally of pokemon.side.pokemon) ally.cureStatus();
},
onAfterSubDamage(damage, target, pokemon, move) {
  if (!pokemon.hp) return;
  for (const c of ['spikes', 'toxicspikes', 'stealthrock', 'stickyweb', 'gmaxsteelsurge']) {
    if (pokemon.side.removeSideCondition(c)) {
      this.add('-sideend', pokemon.side, this.dex.conditions.get(c).name, '[from] move: Bubble Filter', '[of] ' + pokemon);
    }
  }
  for (const ally of pokemon.side.pokemon) ally.cureStatus();
},
secondary: {chance: 30, status: 'brn'},
target: "normal",
type: "Water",
desc: "Clears hazards from the user's side and cures the status of every Pokemon in its party. 30% chance to burn the target.",
shortDesc: "Clears own hazards, cures party status. 30% burn.",
contestType: "Beautiful"
}
