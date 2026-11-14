{
onResidualOrder: 5,
onResidualSubOrder: 4,
onResidual(pokemon) {
  if (!['sunnyday', 'desolateland', 'raindance', 'primordialsea'].includes(pokemon.effectiveWeather())) return;
  for (const ally of pokemon.alliesAndSelf()) {
    if (ally.hp && ally.hp < ally.maxhp) this.heal(ally.baseMaxhp / 16, ally, pokemon);
  }
},
flags: {},
name: "Aromatic Harvest",
rating: 2.5,
num: -3030
}
