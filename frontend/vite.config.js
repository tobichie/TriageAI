import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// In production the app is served through nginx, which terminates TLS,
// enforces Basic Auth and proxies /api and /dashboard-api to the
// backend and dashboard containers. These dev-server proxies only take
// effect when the Vite server is reached directly (e.g. on port 5173),
// so they make local testing work without changing production routing.
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    allowedHosts: ['triageai.munichtechexpo.paulmusch.de'],
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/dashboard-api': {
        target: 'http://dashboard:8001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/dashboard-api/, ''),
      },
    },
  },
})
