{
onDamagingHit(damage, target, source, move) {
      if (["Dark", "Flying", "Ghost"].includes(move.type)) {
        this.boost({ spe: 1 });
      }
    },
onAfterBoost(boost, target, source, effect) {
      if (effect?.name === "Intimidate") {
        this.boost({ spe: 1 });
      }
    },
"flags": {},
"name": "Flying Rattled",
"rating": 1,
"num": -31147
}
