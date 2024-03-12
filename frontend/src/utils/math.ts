export function roundToDP(value: number, dp: number = 2): number {
  const places = Math.pow(10, dp)
  let rounded = dp > 0 ? Math.round((value + Number.EPSILON) * places) / places : Math.round(value)
  return rounded
}

export function roundToDPFixed(value: number, dp: number = 2): string {
  return roundToDP(value, dp).toFixed(dp)
}

export function toFixed(value: number, dp: number = 2): string {
  return value.toFixed(dp)
}
