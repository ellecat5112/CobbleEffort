{
onStart(pokemon) {
  let activated = false;
  for (const target of pokemon.adjacentFoes()) {
    if (!target.hasType('Bug')) continue;
    if (!activated) {
      this.add('-ability', pokemon, 'Pest Deterrent', 'boost');
      activated = true;
    }
    if (target.volatiles['substitute']) this.add('-immune', target);
    else this.boost({atk: -1}, target, pokemon, null, true);
  }
},
flags: {},
name: "Pest Deterrent",
rating: 2,
num: -3012
}
