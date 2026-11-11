{
onTryHit(target, source, move) {
      if (target !== source && move.type === "Ground") {
        if (!this.boost({ spe: 1 })) {
          this.add("-immune", target, "[from] ability: Tremor Drive");
        }
        return null;
      }
    },
"flags": {"breakable":1},
"name": "Tremor Drive",
"rating": 3,
"num": -31114
}
