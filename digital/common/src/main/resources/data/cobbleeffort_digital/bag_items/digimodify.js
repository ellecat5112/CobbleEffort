{
    /* digimodify <card>: a Digi-Modify card swiped through the Digivice (CobbleEffort: Digital) */
    use(battle, pokemon, itemId, data) {
        var card = data[0];
        var src = { effectType: 'BagItem', name: itemId };
        if (card === 'high_speed_plugin') {
            battle.boost({ spe: 2 }, pokemon, null, src);
        } else if (card === 'metal_armor') {
            battle.boost({ def: 2, spd: 1 }, pokemon, null, src);
        } else if (card === 'giga_destroyer') {
            battle.boost({ atk: 1, spa: 1 }, pokemon, null, src);
            pokemon.addVolatile('focusenergy');
        } else if (card === 'dot_virus' || card === 'bug_card') {
            var foe = null;
            for (var i = 0; i < pokemon.side.foe.active.length; i++) {
                var f = pokemon.side.foe.active[i];
                if (f && !f.fainted) { foe = f; break; }
            }
            if (foe) foe.addVolatile(card === 'dot_virus' ? 'dotvirus' : 'bugcode', pokemon);
        } else if (card === 'recovery_disk') {
            var amount = pokemon.heal(Math.floor(pokemon.maxhp / 2));
            if (amount) battle.add('-heal', pokemon, pokemon.getHealth, '[from] bagitem: ' + itemId);
            if (pokemon.status) pokemon.cureStatus(true);
        }
    }
}
