{
onTryBoost(boost, target, source, effect) {
  if (effect.name === 'Intimidate' && boost.atk) {
    delete boost.atk;
    this.add('-fail', target, 'unboost', 'Attack', '[from] ability: Liquid Courage', '[of] ' + target);
  }
},
onAfterSetStatus(status, target, source, effect) {
  this.add('-ability', target, 'Liquid Courage');
  this.boost({atk: 1}, target, target);
},
onUpdate(pokemon) {
  if (pokemon.volatiles['confusion'] && !pokemon.abilityState.couraged) {
    pokemon.abilityState.couraged = true;
    this.add('-ability', pokemon, 'Liquid Courage');
    this.boost({atk: 1}, pokemon, pokemon);
  } else if (!pokemon.volatiles['confusion']) {
    pokemon.abilityState.couraged = false;
  }
},
flags: {breakable: 1},
name: "Liquid Courage",
rating: 3,
num: -3036
}
