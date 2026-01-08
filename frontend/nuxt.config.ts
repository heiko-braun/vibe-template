// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-01-08',
  devtools: { enabled: true },

  modules: [
    '@nuxt/ui'
  ],

  // API proxy to FastAPI backend (for development)
  nitro: {
    devProxy: {
      '/api': {
        target: 'http://localhost:8081',
        changeOrigin: true,
      }
    }
  },

  // For static generation (SPA mode)
  ssr: false,

  app: {
    head: {
      title: 'App Template',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  }
})
