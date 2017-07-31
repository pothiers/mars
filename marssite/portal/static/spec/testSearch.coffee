describe "It should conduct a search", ()->
  it "Does some simple addition", ()->
    expect(3+2).toEqual(5)
  it "Fails when adding a char + num", ()->
    expect(3+'a').toEqual('3a')
