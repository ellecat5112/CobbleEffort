{
onStart(pokemon) {
  let activated = false;
  for (const target of pokemon.adjacentFoes()) {
    if (!activated) {
      this.add('-ability', pokemon, 'Secondhand Haze', 'boost');
      activated = true;
    }
    if (target.volatiles['substitute']) this.add('-immune', target);
    else this.boost({accuracy: -1}, target, pokemon, null, true);
  }
},
flags: {},
name: "Secondhand Haze",
rating: 3,
num: -3049
}
