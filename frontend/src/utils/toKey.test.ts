import { toKey } from "./toKey"

describe("toKey", () => {
  it("replaces space", () => {
    const val = toKey("test value")
    expect(val).toEqual("test-value")
  })

  it("replaces .", () => {
    const val = toKey("test.value")
    expect(val).toEqual("test-value")
  })

  it("replaces with _", () => {
    const val = toKey("test.value", "_")
    expect(val).toEqual("test_value")
  })

  it("replaces space multiple times", () => {
    const val = toKey("test value (100)")
    expect(val).toEqual("test-value-(100)")
  })
})
