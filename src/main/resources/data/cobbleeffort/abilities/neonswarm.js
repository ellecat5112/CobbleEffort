{
onStart(pokemon) {
  if (pokemon.baseSpecies.baseSpecies !== 'cobbleeffort:Ufly' || pokemon.level < 20 || pokemon.transformed) return;
  if (pokemon.hp > pokemon.maxhp / 4) {
    if (pokemon.species.id === 'cobbleeffortufly') pokemon.formeChange('cobbleeffort:Ufly-Swarm');
  } else if (pokemon.species.id === 'cobbleeffortuflyswarm') {
    pokemon.formeChange('cobbleeffort:Ufly');
  }
},
onResidualOrder: 29,
onResidual(pokemon) {
  if (pokemon.baseSpecies.baseSpecies !== 'cobbleeffort:Ufly' || pokemon.level < 20 || pokemon.transformed || !pokemon.hp) return;
  if (pokemon.hp > pokemon.maxhp / 4) {
    if (pokemon.species.id === 'cobbleeffortufly') pokemon.formeChange('cobbleeffort:Ufly-Swarm');
  } else if (pokemon.species.id === 'cobbleeffortuflyswarm') {
    pokemon.formeChange('cobbleeffort:Ufly');
  }
},
flags: {failroleplay: 1, noreceiver: 1, noentrain: 1, notrace: 1, failskillswap: 1, cantsuppress: 1, notransform: 1},
name: "Neon Swarm",
rating: 3,
num: -3070
}
