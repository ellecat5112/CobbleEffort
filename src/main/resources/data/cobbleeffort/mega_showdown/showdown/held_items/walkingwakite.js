({
  name: "Walking Wakite",
  spritenum: 0,
  megaStone: { "Walking Wake": "Walking Wake-Mega" },
  itemUser: ["Walking Wake"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9108,
  gen: 9,
  isNonstandard: "Past",
})
