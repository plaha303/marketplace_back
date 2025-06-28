import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import path from 'path';
import svgr from "vite-plugin-svgr";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    svgr({
      svgrOptions: {
        replaceAttrValues: {
          '#000': 'currentColor',
          '#000000': 'currentColor',
          '#A0864D': 'currentColor',
          '#fff': 'currentColor',
          '#ffffff': 'currentColor'
        },
      },
    
    })
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    }
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
  },
})
