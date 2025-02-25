import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      // Any call to /api/* will be forwarded to your Flask backend
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
        // Remove the '/api' prefix before forwarding the request
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
