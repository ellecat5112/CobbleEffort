{
onDamagingHit(damage, target, source, move) {
  if (source && source !== target && source.hp && this.checkMoveMakesContact(move, source, target)) {
    source.addVolatile('hooked', target);
  }
},
condition: {
  duration: 2,
  onStart(pokemon) {
    this.add('-start', pokemon, 'ability: Hooked');
  },
  onTrapPokemon(pokemon) {
    pokemon.tryTrap();
  },
  onEnd(pokemon) {
    this.add('-end', pokemon, 'ability: Hooked', '[silent]');
  }
},
flags: {},
name: "Hooked",
rating: 3,
num: -3019
}
