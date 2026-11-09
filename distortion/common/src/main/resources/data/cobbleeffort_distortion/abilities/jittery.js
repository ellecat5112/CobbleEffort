{
onDamagingHit(damage, target, source, move) {
      if (["Fairy", "Bug", "Ghost"].includes(move.type)) {
        this.boost({ spe: 1 });
      }
    },
onAfterBoost(boost, target, source, effect) {
      if (effect?.name === "Intimidate") {
        this.boost({ spe: 1 });
      }
    },
"flags": {},
"name": "Jittery",
"rating": 1,
"num": -31118
}
