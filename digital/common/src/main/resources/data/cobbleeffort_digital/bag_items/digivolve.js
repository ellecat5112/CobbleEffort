{
    /* digivolve <showdown species id>: the Digivice's warp digivolution, for the rest of the battle (CobbleEffort: Digital) */
    use(battle, pokemon, itemId, data) {
        var species = battle.dex.species.get(data[0]);
        if (!species || !species.exists) return;
        pokemon.setSpecies(species, { effectType: 'BagItem', name: itemId });
        pokemon.baseSpecies = species;
        battle.add('-activate', pokemon, 'warpdigivolution');
    }
}
