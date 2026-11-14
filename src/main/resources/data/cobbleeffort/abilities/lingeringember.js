{
onResidualOrder: 10,
onResidual(pokemon) {
  if (!pokemon.hp) return;
  for (const foe of pokemon.foes()) {
    if (foe.status === 'brn') this.damage(foe.baseMaxhp / 16, foe, pokemon);
  }
},
flags: {},
name: "Lingering Ember",
rating: 3,
num: -3050
}
