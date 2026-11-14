{
onStart(pokemon) {
  if (pokemon.baseSpecies.baseSpecies !== 'cobbleeffort:Sparkling' || pokemon.level < 20 || pokemon.transformed) return;
  if (pokemon.hp > pokemon.maxhp / 4) {
    if (pokemon.species.id === 'cobbleeffortsparkling') pokemon.formeChange('cobbleeffort:Sparkling-Swarm');
  } else if (pokemon.species.id === 'cobbleeffortsparklingswarm') {
    pokemon.formeChange('cobbleeffort:Sparkling');
  }
},
onResidualOrder: 29,
onResidual(pokemon) {
  if (pokemon.baseSpecies.baseSpecies !== 'cobbleeffort:Sparkling' || pokemon.level < 20 || pokemon.transformed || !pokemon.hp) return;
  if (pokemon.hp > pokemon.maxhp / 4) {
    if (pokemon.species.id === 'cobbleeffortsparkling') pokemon.formeChange('cobbleeffort:Sparkling-Swarm');
  } else if (pokemon.species.id === 'cobbleeffortsparklingswarm') {
    pokemon.formeChange('cobbleeffort:Sparkling');
  }
},
flags: {failroleplay: 1, noreceiver: 1, noentrain: 1, notrace: 1, failskillswap: 1, cantsuppress: 1, notransform: 1},
name: "Murmuration",
rating: 3,
num: -3021
}
