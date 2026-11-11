{
onTryBoost(boost, target, source, effect) {
      if (source && target === source) return;
      if (boost.accuracy && boost.accuracy < 0) {
        delete boost.accuracy;
        if (!effect.secondaries) {
          this.add(
            "-fail",
            target,
            "unboost",
            "accuracy",
            "[from] ability: Fighting Mind's Eye",
            "[of] " + target,
          );
        }
      }
    },
"onModifyMovePriority": -5,
onModifyMove(move) {
      move.ignoreEvasion = true;
      if (!move.ignoreImmunity) move.ignoreImmunity = {};
      if (move.ignoreImmunity !== true) {
        move.ignoreImmunity["Fighting"] = true;
        move.ignoreImmunity["Fighting"] = true;
      }
    },
"flags": {"breakable":1},
"name": "Fighting Mind's Eye",
"rating": 0,
"num": -31158
}
