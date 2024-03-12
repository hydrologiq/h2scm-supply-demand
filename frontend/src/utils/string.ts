export const splitHydrogenMethod = (source: string) =>
  source
    .replace("Hydrogen", "")
    .replace(/([A-Z])/g, " $1")
    .trim()
