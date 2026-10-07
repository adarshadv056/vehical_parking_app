const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
        '@/components': path.resolve(__dirname, 'src/components'),
        '@/components/ui': path.resolve(__dirname, 'src/components/ui'),
        '@/components/layout': path.resolve(__dirname, 'src/components/layout'),
        '@/components/feedback': path.resolve(__dirname, 'src/components/feedback'),
        '@/components/icons': path.resolve(__dirname, 'src/components/icons'),
        '@/api': path.resolve(__dirname, 'src/api'),
        '@/store': path.resolve(__dirname, 'src/store'),
        '@/composables': path.resolve(__dirname, 'src/composables'),
        '@/styles': path.resolve(__dirname, 'src/styles'),
        '@/assets': path.resolve(__dirname, 'src/assets')
      }
    }
  },
  chainWebpack: config => {
    config.resolve.alias
      .set('@', path.resolve(__dirname, 'src'))
      .set('@/components', path.resolve(__dirname, 'src/components'))
      .set('@/components/ui', path.resolve(__dirname, 'src/components/ui'))
      .set('@/components/layout', path.resolve(__dirname, 'src/components/layout'))
      .set('@/components/feedback', path.resolve(__dirname, 'src/components/feedback'))
      .set('@/components/icons', path.resolve(__dirname, 'src/components/icons'))
      .set('@/api', path.resolve(__dirname, 'src/api'))
      .set('@/store', path.resolve(__dirname, 'src/store'))
      .set('@/composables', path.resolve(__dirname, 'src/composables'))
      .set('@/styles', path.resolve(__dirname, 'src/styles'))
      .set('@/assets', path.resolve(__dirname, 'src/assets'))
  }
})