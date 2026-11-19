{
    num: -3202, name: "Bug Code", type: "Dark", category: "Status", basePower: 0, accuracy: 90, pp: 10, priority: 0,
    flags: {protect: 1, reflectable: 1, mirror: 1, metronome: 1}, volatileStatus: 'bugcode', target: "normal",
    desc: "Writes a bug into the target's data for 3 turns: the Vaccine > Virus > Data > Vaccine triangle is inverted for it.",
    shortDesc: "3 turns: inverts the target's attribute triangle.",
    condition: {
        duration: 3,
        onStart(pokemon) {
            this.add('-start', pokemon, 'bugcode');
        },
        onEnd(pokemon) {
            this.add('-end', pokemon, 'bugcode');
        }
    },
    secondary: null, isNonstandard: null, contestType: "Clever"
}
