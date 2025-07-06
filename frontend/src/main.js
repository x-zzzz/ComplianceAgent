import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import naive from 'naive-ui';

createApp(App).use(router).use(naive).mount('#app');
const observerError = "ResizeObserver loop completed with undelivered notifications";
window.addEventListener("error", (e) => {
  if (e.message === observerError) {
    e.stopImmediatePropagation();
  }
});