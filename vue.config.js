const devConfig = require('./vue.dev.config')
const devServerAddress = devConfig.devServerAddress

module.exports = {
  publicPath: './',
  transpileDependencies: [
    'vuetify',
  ],
  chainWebpack: config => {
    config.plugin('html').tap(args => {
      args[0].title = 'Paper Retrieval'
      return args
    })
    
  },
  devServer: {
    proxy: {
      '^/api/getPapers': {
        target: devServerAddress,
        changeOrigin: true,
      },
      '^/api/getConfList': {
        target: devServerAddress,
        changeOrigin: true,
      },
      '^/download': {
        target: devServerAddress,
        changeOrigin: true,
      },
      '^/view': {
        target: devServerAddress,
        changeOrigin: true,
      }
    }
  }
}
