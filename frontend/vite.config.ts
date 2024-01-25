import { defineConfig } from "vitest/config"
import react from "@vitejs/plugin-react-swc"
import { fileURLToPath } from "node:url"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./vitest.setup.ts"],
  },
  resolve: {
    alias: {
      "@views": fileURLToPath(new URL("./src/views/", import.meta.url)),
      "@components": fileURLToPath(new URL("./src/components/", import.meta.url)),
      "@api": fileURLToPath(new URL("./src/api/", import.meta.url)),
    },
  },
})
