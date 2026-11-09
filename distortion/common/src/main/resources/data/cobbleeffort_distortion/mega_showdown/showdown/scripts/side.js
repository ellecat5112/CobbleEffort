({
  chooseMove(moveText, targetLoc, event) {
    const Side = require("./sim/side").Side;
    if (typeof moveText === "string" && / distort$/.test(moveText.trim())) {
      let text = moveText.trim().replace(/ distort$/, "").trim();
      if (targetLoc === undefined && /\s(?:-|\+)?[1-3]$/.test(text)) {
        targetLoc = parseInt(text.slice(-2));
        text = text.slice(0, -2).trim();
      }
      const index = this.getChoiceIndex();
      const pokemon = this.active[index];
      // can't distort (already did, or no crystal): the plain move, never an error (an AI's choice must not fail)
      if (!pokemon || this.distortUsed || this.choice.distort || !this.battle.actions.canDistort(pokemon)) {
        return Side.prototype.chooseMove.call(this, text, targetLoc, event);
      }
      const ok = Side.prototype.chooseMove.call(this, text, targetLoc, event);
      if (ok) {
        // the queue turns this into a distort action before the move (see queue.js)
        this.choice.actions[this.choice.actions.length - 1].distort = true;
        this.choice.distort = true;
      }
      return ok;
    }
    return Side.prototype.chooseMove.call(this, moveText, targetLoc, event);
  },
})
