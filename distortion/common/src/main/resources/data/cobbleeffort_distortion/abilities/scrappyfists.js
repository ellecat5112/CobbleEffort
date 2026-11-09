{
"onModifyMovePriority": -5,
onModifyMove(move) {
      if (!move.ignoreImmunity) move.ignoreImmunity = {};
      if (move.ignoreImmunity !== true) {
        move.ignoreImmunity["Fighting"] = true;
        move.ignoreImmunity["Fighting"] = true;
      }
    },
onTryBoost(boost, target, source, effect) {
      if (effect.name === "Intimidate" && boost.atk) {
        delete boost.atk;
        this.add(
          "-fail",
          target,
          "unboost",
          "Attack",
          "[from] ability: Scrappy Fists",
          "[of] " + target,
        );
      }
    },
"flags": {},
"name": "Scrappy Fists",
"rating": 3,
"num": -31115
}
