import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import naive from 'naive-ui';

// 抑制 ResizeObserver loop 錯誤
const observerErrMsg = 'ResizeObserver loop completed with undelivered notifications';
const observerErrMsg2 = 'ResizeObserver loop limit exceeded';
const rawError = window.onerror;
window.onerror = function (msg, ...args) {
  if (
    typeof msg === 'string' &&
    (msg.includes(observerErrMsg) || msg.includes(observerErrMsg2))
  ) {
    return true; // 阻止錯誤繼續向上冒泡
  }
  if (rawError) return rawError(msg, ...args);
};
window.addEventListener('error', (e) => {
  if (
    e.message === observerErrMsg ||
    e.message === observerErrMsg2
  ) {
    e.stopImmediatePropagation();
  }
});

createApp(App).use(router).use(naive).mount('#app');

// 彻底抑制 webpack overlay 的 ResizeObserver loop 报错
if (typeof window !== 'undefined') {
  window.addEventListener('error', function (e) {
    if (
      e.message &&
      (e.message.includes('ResizeObserver loop completed with undelivered notifications') ||
        e.message.includes('ResizeObserver loop limit exceeded'))
    ) {
      e.stopImmediatePropagation();
      e.preventDefault();
      return false;
    }
  }, true);

  // 针对 webpack-dev-server 的 overlay
  if (window.__VUE_DEVTOOLS_GLOBAL_HOOK__ && window.__VUE_DEVTOOLS_GLOBAL_HOOK__.emit) {
    const rawEmit = window.__VUE_DEVTOOLS_GLOBAL_HOOK__.emit;
    window.__VUE_DEVTOOLS_GLOBAL_HOOK__.emit = function (...args) {
      if (
        args[0] === 'app:error' &&
        args[1] &&
        typeof args[1].message === 'string' &&
        (args[1].message.includes('ResizeObserver loop completed with undelivered notifications') ||
          args[1].message.includes('ResizeObserver loop limit exceeded'))
      ) {
        return;
      }
      return rawEmit.apply(this, args);
    };
  }
}