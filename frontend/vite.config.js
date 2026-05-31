import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],

  server: {
    host: '0.0.0.0',

    allowedHosts: [
      '<frontend_domain_name>' //Add domain name or local host in the form of "www.domain.xyz".
    ]
  }
})