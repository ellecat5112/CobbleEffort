{
"onTryHitPriority": 1,
onTryHit(target, source, move) {
      if (target !== source && move.type === "Fire") {
        if (!this.boost({ atk: 1 })) {
          this.add("-immune", target, "[from] ability: Ember Sipper");
        }
        return null;
      }
    },
onAllyTryHitSide(target, source, move) {
      if (source === this.effectState.target || !target.isAlly(source)) return;
      if (move.type === "Fire") {
        this.boost({ atk: 1 }, this.effectState.target);
      }
    },
"flags": {"breakable":1},
"name": "Ember Sipper",
"rating": 3,
"num": -31131
}
