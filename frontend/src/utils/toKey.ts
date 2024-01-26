export function toKey(text: string, char: string = "-") {
  return text.replaceAll(new RegExp("[ |.:]", "g"), char)
}
