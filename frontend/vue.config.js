module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://backend:8000', // Django 后端服务地址
        changeOrigin: true,
      },
    },
  },
};