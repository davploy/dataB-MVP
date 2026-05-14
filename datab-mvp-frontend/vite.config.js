import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// https://vite.dev/config/
export default defineConfig({
  // Load `.env` from monorepo root (shared with backend).
  envDir: path.resolve(__dirname, '..'),
  plugins: [vue()],
  envDir: '..',
})
