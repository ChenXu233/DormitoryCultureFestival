// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    // ⚠️ 不要引入 @nuxt/fonts 或 @nuxtjs/google-fonts
  ],
  css: ['~/assets/css/main.css'],

  // 完全禁用字体处理
  icon: {
    provider: 'local'
  },

  vite: {
    server: {
      fs: {
        allow: ['..'] // 或明确包含你的项目路径
      },
      proxy: {
      '/api': {
        target: 'http://101.126.35.203:8000',
        changeOrigin: true
      }
    }
    }
  },
})
