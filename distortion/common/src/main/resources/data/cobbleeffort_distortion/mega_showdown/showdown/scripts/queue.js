({
  resolveAction(action, midTurn) {
    const BattleQueue = require("./sim/battle-queue").BattleQueue;
    const battle = this.battle;
    if (!battle.distortHooked) {
      battle.distortHooked = true;
      const runAction = battle.runAction;
      battle.runAction = function (a) {
        if (a.choice === "event" && a.event === "Distort") this.actions.runDistort(a.pokemon);
        // Pokémon distorted outside battle (the interaction wheel) start in their -Distorted forme: give them their twins
        if (a.choice === "start") this.actions.distortedAtStart();
        return runAction.call(this, a);
      };
    }
    const actions = BattleQueue.prototype.resolveAction.call(this, action, midTurn);
    if (!midTurn && action.choice === "move" && action.distort && !action.pokemon.distorted) {
      action.distort = false;
      actions.unshift(...BattleQueue.prototype.resolveAction.call(this,
        {choice: "event", event: "Distort", pokemon: action.pokemon, order: 106}, midTurn));
    }
    return actions;
  },
})
