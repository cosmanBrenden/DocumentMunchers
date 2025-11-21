import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  root: 'renderer',
  base: './',
  resolve: {
    alias: {
      '@': resolve(__dirname, 'renderer')
    }
  },
  build: {
    outDir: '../../dist/renderer',
    emptyOutDir: true
  }
})
