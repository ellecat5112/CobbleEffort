{
onDamagingHit(damage, target, source, move) {
  if (move.type === 'Fire') this.boost({spa: 1}, target, target);
},
onStart(pokemon) {
  for (const ally of pokemon.side.pokemon) {
    if (ally.status === 'frz') {
      this.add('-activate', pokemon, 'ability: Warm Infusion');
      ally.cureStatus();
    }
  }
},
onResidualOrder: 5,
onResidualSubOrder: 3,
onResidual(pokemon) {
  for (const ally of pokemon.side.pokemon) {
    if (ally.status === 'frz') {
      this.add('-activate', pokemon, 'ability: Warm Infusion');
      ally.cureStatus();
    }
  }
},
onUpdate(pokemon) {
  if (pokemon.status === 'frz') pokemon.cureStatus();
},
onImmunity(type, pokemon) {
  if (type === 'frz') return false;
},
flags: {},
name: "Warm Infusion",
rating: 2.5,
num: -3031
}
