({
  name: "Miraidonite",
  spritenum: 0,
  megaStone: { "Miraidon": "Miraidon-Mega" },
  itemUser: ["Miraidon"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9118,
  gen: 9,
  isNonstandard: "Past",
})
