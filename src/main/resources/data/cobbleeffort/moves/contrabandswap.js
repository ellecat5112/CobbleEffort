{
num: -3046,
accuracy: 100,
basePower: 50,
category: "Physical",
name: "Contraband Swap",
pp: 10,
priority: 0,
flags: {contact: 1, protect: 1, mirror: 1, metronome: 1},
onAfterHit(target, source, move) {
  if (source.hp && !source.item && target.item) {
    const item = target.takeItem(source);
    if (item) {
      if (!source.setItem(item)) {
        target.item = item.id;
      } else {
        this.add('-enditem', target, item, '[silent]', '[from] move: Contraband Swap');
        this.add('-item', source, item, '[from] move: Contraband Swap', '[of] ' + target);
      }
    }
  }
  if (target.hp) target.addVolatile('contrabandswap', source);
},
condition: {
  duration: 2,
  onStart(pokemon) {
    this.add('-start', pokemon, 'Contraband Swap');
  },
  onResidualOrder: 13,
  onEnd(pokemon) {
    this.add('-end', pokemon, 'Contraband Swap');
    if (!pokemon.hp) return;
    const mod = Math.pow(2, Math.max(-2, Math.min(2, this.dex.getEffectiveness('Dark', pokemon))));
    this.damage(Math.max(1, Math.floor(pokemon.baseMaxhp / 4 * mod)), pokemon, null, this.dex.conditions.get('contrabandswap'));
  }
},
secondary: null,
target: "normal",
type: "Dark",
desc: "The user steals the target's held item if it has none, and leaves a volatile jug with the target that explodes at the end of the next turn, dealing 1/4 of its maximum HP adjusted by Dark-type effectiveness.",
shortDesc: "Steals item; jug explodes next turn: 1/4 HP x Dark effectiveness.",
contestType: "Clever"
}
