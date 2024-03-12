import { roundToDP, roundToDPFixed, toFixed } from "./math"

describe("roundToDP", () => {
  it("two decimal places", () => {
    const val = roundToDP(2.234567)
    expect(val).toEqual(2.23)
  })

  it("one decimal place", () => {
    const val = roundToDP(2.5, 1)
    expect(val).toEqual(2.5)
  })

  it("four decimal places", () => {
    const val = roundToDP(2.234567, 4)
    expect(val).toEqual(2.2346)
  })

  it("zero decimal places", () => {
    const val = roundToDP(2.234567, 0)
    expect(val).toEqual(2)
  })

  it("no float value", () => {
    const val = roundToDP(2)
    expect(val).toEqual(2)
  })

  it("no float and no decimal places value", () => {
    const val = roundToDP(2, 0)
    expect(val).toEqual(2)
  })

  it("zero value", () => {
    const val = roundToDP(0)
    expect(val).toEqual(0)
  })

  it("zero value zero decimal places", () => {
    const val = roundToDP(0, 0)
    expect(val).toEqual(0)
  })
})

describe("roundToDPFixed", () => {
  it("pad zeros", () => {
    const val = roundToDPFixed(1, 2)
    expect(val).toEqual("1.00")
  })
})

describe("toFixed", () => {
  it("pad zeros", () => {
    const val = toFixed(1)
    expect(val).toEqual("1.00")
  })
})
