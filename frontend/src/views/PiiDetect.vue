<template>
  <div class="gpt-root chatgpt-style-bg">
    <aside class="gpt-sidebar">
      <div class="gpt-sidebar-header">
        <img src="../assets/compliance_bot.svg" alt="compliance bot" class="gpt-logo" />
        <span class="gpt-title" style="display: flex; align-items: center; gap: 8px;">
          合规小助手
        </span>
      </div>
      <nav class="gpt-menu">
        <div v-for="item in menuOptions" :key="item.key" :class="['gpt-menu-item', {active: activeMenu === item.key}]"
          @click="handleMenuClick(item)">
          <img :src="item.icon" :alt="item.label + ' icon'" class="gpt-menu-icon" />
          <span>{{ item.label }}</span>
        </div>
      </nav>
    </aside>
    <main class="gpt-main chatgpt-main">
      <header class="gpt-main-header chatgpt-header">
        <span class="gpt-main-title chatgpt-title-main">个人信息检测与风险评估</span>
      </header>
      <section class="gpt-chat-section chatgpt-chat-section">
        <div class="gpt-chat-center chatgpt-chat-center">
          <template v-if="activeMenu === 'pii'">
            <PiiDetectPanel />
          </template>
          <template v-else-if="activeMenu === 'desensitize'">
            <DesensitizePanel />
          </template>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import PiiDetectPanel from './PiiDetectPanel.vue';
import DesensitizePanel from './DesensitizePanel.vue';

const router = useRouter();
const route = useRoute();

const menuOptions = [
  { label: '首页', key: 'home', icon: require('../assets/compliance_bot.svg'), path: '/' },
  { label: 'PII检测', key: 'pii', icon: require('../assets/pii.svg'), path: '/pii' },
  { label: '脱敏处理', key: 'desensitize', icon: require('../assets/desensitize.svg'), path: '/pii?tab=desensitize' },
  { label: '敏感词扫描', key: 'sensitive_words', icon: require('../assets/sensitive_words.svg') },
  { label: '合规风险评估', key: 'risk_assess', icon: require('../assets/risk_assess.svg') },
  { label: '合规知识库问答', key: 'qa', icon: require('../assets/qa.svg') },
  { label: '合规报告生成', key: 'report', icon: require('../assets/report.svg') },
  { label: '数据合规建议', key: 'advice', icon: require('../assets/advice.svg') },
  { label: '日志与历史记录', key: 'history', icon: require('../assets/history.svg') },
  { label: '系统设置', key: 'settings', icon: require('../assets/settings.svg') }
];

const activeMenu = ref('pii');

function handleMenuClick(item) {
  if (item.key === 'home') {
    router.push('/');
    return;
  }
  if (item.path) {
    router.push(item.path);
  }
  // 只在 /pii 路由下切换 tab
  if (route.path === '/pii' && (item.key === 'pii' || item.key === 'desensitize')) {
    activeMenu.value = item.key;
  }
}

// 路由变化时自动联动菜单和tab
watch(
  () => route.fullPath,
  (val) => {
    if (route.path === '/pii') {
      if (route.query.tab === 'desensitize') {
        activeMenu.value = 'desensitize';
      } else {
        activeMenu.value = 'pii';
      }
    } else if (route.path === '/') {
      activeMenu.value = 'home';
    }
  },
  { immediate: true }
);
// ...existing code...
</script>

<style scoped>
.gpt-root {
  display: flex;
  height: 100vh;
  background: #f7f7f8;
}
.gpt-sidebar {
  width: 320px;
  background: #fff;
  border-right: 1px solid #ececec;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0 0 0 0;
}
.gpt-sidebar-header {
  display: flex;
  align-items: center;
  height: 64px;
  padding: 0 36px 0 36px;
  border-bottom: 1px solid #ececec;
  width: 100%;
}
.gpt-logo {
  width: 36px;
  height: 36px;
  margin-right: 18px;
}
.gpt-title {
  font-size: 1.3rem;
  font-weight: 600;
  letter-spacing: 1px;
}
.gpt-menu-icon {
  width: 22px;
  height: 22px;
  margin-right: 12px;
  vertical-align: middle;
}
.gpt-menu {
  flex: 1;
  width: 100%;
  padding: 16px 0 0 0;
}
.gpt-menu-item {
  padding: 12px 40px;
  cursor: pointer;
  font-size: 1.08rem;
  color: #222;
  border-left: 3px solid transparent;
  transition: background 0.2s, border-color 0.2s;
}
.gpt-menu-item.active {
  background: #f3f6fa;
  border-left: 3px solid #409eff;
  color: #409eff;
}
.gpt-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}
.gpt-main-header {
  height: 64px;
  display: flex;
  align-items: center;
  padding: 0 32px;
  font-size: 1.2rem;
  font-weight: 500;
  border-bottom: 1px solid #ececec;
  background: #fff;
}
.gpt-main-title {
  margin-left: 0;
}
.gpt-chat-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  overflow: auto;
  background: #f7f7f8;
}
.gpt-chat-center {
  width: 90%;
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 0 0 0;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  min-height: 0;
}
.gpt-feature-title {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 8px;
}
.gpt-feature-title-text {
  vertical-align: middle;
}
.gpt-feature-desc {
  text-align: center;
  color: #888;
  font-size: 1.08rem;
  margin-bottom: 18px;
}
.gpt-input-area-adaptive {
  width: 90%;
  margin: 0 auto 10px auto;
}
.gpt-input {
  font-size: 1.08rem;
}
.gpt-input-rounded {
  border-radius: 24px !important;
  border: 1px solid #e0e0e0 !important;
  background: #fff !important;
  box-shadow: none !important;
  padding: 16px 20px !important;
  font-size: 1.08rem;
  outline: none;
  transition: border-color 0.2s;
}
.gpt-input-rounded:focus {
  border-color: #bdbdbd !important;
}
.gpt-action-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-bottom: 8px;
}
.gpt-detect-btn {
  min-width: 120px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 24px;
  box-shadow: 0 2px 8px #e0e6ed;
}
.gpt-upload-btn {
  background: #f3f6fa;
  border-radius: 50%;
  box-shadow: 0 2px 8px #e0e6ed;
  border: none;
}
.gpt-upload-tip {
  text-align: center;
  color: #aaa;
  font-size: 0.98rem;
  margin-bottom: 8px;
}
.gpt-file-preview {
  margin-bottom: 12px;
}
.gpt-chat-list {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.gpt-chat-bubble {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px #f0f1f3;
  padding: 20px 24px;
  font-size: 1.08rem;
  line-height: 1.7;
  word-break: break-all;
  border: 1px solid #ececec;
}
.risk.高 { color: #e74c3c; font-weight: bold; }
.risk.中 { color: #f39c12; }
.risk.低 { color: #27ae60; }
.gpt-pii-summary {
  background: #f8fafc;
  border-radius: 12px;
  padding: 20px 28px 16px 28px;
  margin: 24px 0 12px 0;
  box-shadow: 0 2px 8px #f0f1f3;
  font-size: 1.08rem;
}
.gpt-pii-summary-unfold {
  margin-top: 24px;
  margin-bottom: 12px;
  background: #fffbe8;
  border: 1px solid #ffe58f;
  box-shadow: 0 2px 8px #f9f6e7;
}
.gpt-summary-title {
  font-size: 1.18rem;
  font-weight: 700;
  margin-bottom: 10px;
}
.gpt-summary-row {
  margin-bottom: 8px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}
.gpt-summary-reason {
  color: #666;
  font-size: 0.98rem;
  line-height: 1.7;
}
.gpt-pii-collapse {
  margin-top: 18px;
}
.gpt-desensitize-section {
  margin-top: 24px;
  padding: 24px;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 8px #f0f1f3;
}
.gpt-desensitize-btn {
  min-width: 120px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 24px;
  box-shadow: 0 2px 8px #e0e6ed;
}
.gpt-desensitize-result {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px 20px;
  margin-top: 12px;
  font-size: 1rem;
  line-height: 1.6;
}
.gpt-desensitized-text {
  word-break: break-all;
  white-space: pre-wrap;
}
/* ChatGPT风格增强 */
.chatgpt-style-bg {
  background: #f7f7f8 !important;
}
.chatgpt-header {
  background: #fff;
  border-bottom: 1px solid #ececec;
  box-shadow: 0 1px 4px #f0f1f3;
}
.chatgpt-title-main {
  font-size: 1.5rem;
  font-weight: 700;
  color: #222;
}
.chatgpt-main {
  background: #f7f7f8;
}
.chatgpt-chat-section {
  background: #f7f7f8;
}
.chatgpt-chat-center {
  max-width: 700px;
  width: 100%;
  margin: 0 auto;
  padding: 32px 0 0 0;
}
.gpt-panel-card, .chatgpt-panel-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 16px 0 rgba(0,0,0,0.04);
  padding: 32px 36px 28px 36px;
  margin-bottom: 32px;
}
.gpt-chat-bubble, .n-input, .n-card, .n-upload, .n-collapse, .n-collapse-item, .gpt-desensitize-result {
  border-radius: 18px !important;
}
.gpt-desensitize-result {
  background: #f8fafc;
  border-radius: 18px !important;
}
.gpt-input-rounded {
  border-radius: 18px !important;
}
</style>

