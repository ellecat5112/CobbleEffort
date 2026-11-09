{
onFoeTrapPokemon(pokemon) {
      if (
        pokemon.hasType("Ground") &&
        pokemon.isAdjacent(this.effectState.target)
      ) {
        pokemon.tryTrap(true);
      }
    },
onFoeMaybeTrapPokemon(pokemon, source) {
      if (!source) source = this.effectState.target;
      if (!source || !pokemon.isAdjacent(source)) return;
      if (!pokemon.knownType || pokemon.hasType("Ground")) {
        pokemon.maybeTrapped = true;
      }
    },
"flags": {},
"name": "Quagmire",
"rating": 4,
"num": -31117
}
