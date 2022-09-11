export function SeedRandom(seed: number) {
  const mod1 = 4294967087;
  const mul1 = 65539;
  const mod2 = 4294965887;
  const mul2 = 65537;
  const limit = 4e9;

  let state1 = (seed % (mod1 - 1)) + 1;
  let state2 = (seed % (mod2 - 1)) + 1;

  function random(): number {
    state1 = (state1 * mul1) % mod1;
    state2 = (state2 * mul2) % mod2;
    if (
      state1 < limit &&
      state2 < limit &&
      state1 < mod1 % limit &&
      state2 < mod2 % limit
    ) {
      return random();
    }
    return ((state1 + state2) % limit) / limit;
  }
  return random;
}
