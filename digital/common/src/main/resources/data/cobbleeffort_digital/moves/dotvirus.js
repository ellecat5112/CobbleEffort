{
    num: -3201, name: "Dot Virus", type: "Dark", category: "Status", basePower: 0, accuracy: 90, pp: 10, priority: 0,
    flags: {protect: 1, reflectable: 1, mirror: 1, metronome: 1}, volatileStatus: 'dotvirus', target: "normal",
    desc: "Compresses the target into 8-bit dot data for 3 turns: its Attack is halved and it can't use special moves.",
    shortDesc: "3 turns: target's Atk halved, no special moves.",
    condition: {
        duration: 3,
        onStart(pokemon) {
            this.add('-formechange', pokemon, pokemon.species.name + '-Pixelated');
        },
        onModifyAtkPriority: 5,
        onModifyAtk(atk, pokemon) {
            return this.chainModify(0.5);
        },
        onDisableMove(pokemon) {
            for (const slot of pokemon.moveSlots) {
                if (this.dex.moves.get(slot.id).category === 'Special') pokemon.disableMove(slot.id);
            }
        },
        onEnd(pokemon) {
            this.add('-formechange', pokemon, pokemon.species.name + '-Restored');
        }
    },
    secondary: null, isNonstandard: null, contestType: "Clever"
}
