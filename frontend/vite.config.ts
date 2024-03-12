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
      "@assets": fileURLToPath(new URL("./src/assets/", import.meta.url)),
      "@views": fileURLToPath(new URL("./src/views/", import.meta.url)),
      "@components": fileURLToPath(new URL("./src/components/", import.meta.url)),
      "@api": fileURLToPath(new URL("./src/api/", import.meta.url)),
      "@utils": fileURLToPath(new URL("./src/utils/", import.meta.url)),
      "@custom/types": fileURLToPath(new URL("./src/types/", import.meta.url)),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (
            id.includes("node_modules") &&
            ["@emotion", "react", "framer-motion"].filter((name) => id.includes(name)).length === 0
          ) {
            return id.toString().split("node_modules/")[1].split("/")[0].toString()
          }
        },
      },
    },
  },
})
