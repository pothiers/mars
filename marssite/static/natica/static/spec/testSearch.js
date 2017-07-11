describe("It should conduct a search", function() {
  it("Does some simple addition", function() {
    return expect(3 + 2).toEqual(5);
  });
  return it("Fails when adding a char + num", function() {
    return expect(3 + 'a').toEqual('3a');
  });
});
