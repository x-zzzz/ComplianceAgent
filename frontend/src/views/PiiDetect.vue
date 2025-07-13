<template>
  <div class="gpt-root">
    <aside class="gpt-sidebar">
      <div class="gpt-sidebar-header">
        <img src="../assets/modern_bot.svg" alt="compliance bot" class="gpt-logo" />
        <span class="gpt-title">合规智能体</span>
      </div>
      <nav class="gpt-menu">
        <div v-for="item in menuOptions" 
             :key="item.key" 
             :class="['gpt-menu-item', { active: activeMenu === item.key }]"
             @click="handleMenuClick(item)">
          <img :src="item.icon" :alt="item.label + ' icon'" class="gpt-menu-icon" />
          <span>{{ item.label }}</span>
        </div>
      </nav>
      <div class="gpt-sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">AI</div>
          <span class="user-name">合规助手</span>
        </div>
      </div>
    </aside>
    <main class="gpt-main">
      <!-- 删除header，保留空间 -->
      <div style="height: 1rem;"></div>
      <section class="gpt-chat-section">
        <div class="gpt-chat-center">
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
import { ref, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import PiiDetectPanel from './PiiDetectPanel.vue';
import DesensitizePanel from './DesensitizePanel.vue';

const router = useRouter();
const route = useRoute();
const isDark = ref(false);

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

const getActiveMenuLabel = computed(() => {
  const item = menuOptions.find(item => item.key === activeMenu.value);
  return item ? item.label : '';
});

function toggleTheme() {
  isDark.value = !isDark.value;
  document.documentElement.classList.toggle('dark');
}

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
</script>

<style scoped>
.gpt-root {
  display: flex;
  height: 100vh;
  background-color: var(--gpt-bg);
  color: var(--gpt-text);
}

.gpt-sidebar {
  width: clamp(280px, 15vw, 360px);
  background: var(--gpt-sidebar-bg);
  border-right: 1px solid var(--gpt-border);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.gpt-sidebar-header {
  display: flex;
  align-items: center;
  padding: clamp(1.25rem, 2vw, 2rem);
  height: clamp(76px, 8vh, 96px);
  border-bottom: 1px solid var(--gpt-border);
}

.gpt-logo {
  width: clamp(40px, 2.5vw, 56px);
  height: clamp(40px, 2.5vw, 56px);
  margin-right: clamp(1rem, 1.5vw, 1.5rem);
}

.gpt-title {
  font-size: clamp(1.35rem, 1.5vw, 1.75rem);
  font-weight: 600;
  color: var(--gpt-text);
  letter-spacing: -0.025em;
}

.gpt-menu {
  flex: 1;
  padding: clamp(0.75rem, 1vw, 1.25rem) 0;
  overflow-y: auto;
}

.gpt-menu-item {
  display: flex;
  align-items: center;
  padding: clamp(0.875rem, 1.2vw, 1.25rem) clamp(1.25rem, 1.5vw, 2rem);
  color: var(--gpt-text);
  transition: all 0.3s ease;
  border-radius: 0.75rem;
  margin: 0.25rem clamp(0.75rem, 1vw, 1.25rem);
  font-size: clamp(1.1rem, 1.2vw, 1.4rem);
  font-weight: 500;
  transform-origin: left center;
}

.gpt-menu-item:hover {
  background: var(--gpt-hover-bg);
  transform: scale(1.02);
}

.gpt-menu-item.active {
  background: var(--gpt-active-bg);
  color: var(--gpt-text);
  font-weight: 600;
  transform: scale(1.02);
}

.gpt-menu-icon {
  width: clamp(24px, 1.8vw, 32px);
  height: clamp(24px, 1.8vw, 32px);
  margin-right: clamp(1rem, 1.2vw, 1.5rem);
  transition: transform 0.3s ease;
}

.gpt-menu-item:hover .gpt-menu-icon {
  transform: scale(1.1);
}

.gpt-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--gpt-main-bg);
  min-width: 0; /* 防止内容溢出 */
}

.gpt-main-header {
  height: clamp(76px, 8vh, 96px);
  border-bottom: 1px solid var(--gpt-border);
  background: var(--gpt-header-bg);
}

.header-content {
  max-width: min(90vw, 120rem);
  width: 100%;
  margin: 0 auto;
  padding: 0 clamp(1.5rem, 2vw, 3rem);
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.gpt-main-title {
  font-size: clamp(1.5rem, 1.8vw, 2.25rem);
  font-weight: 600;
  color: var(--gpt-text);
  letter-spacing: -0.025em;
}

.gpt-chat-section {
  flex: 1;
  overflow-y: hidden;
  background: var(--gpt-bg);
  padding: clamp(1.5rem, 2vw, 2.5rem);
}

.gpt-chat-center {
  height: 100%;
  width: 100%;
  margin: 0;
  background: var(--gpt-content-bg);
  border-radius: clamp(1rem, 1.5vw, 2rem);
  box-shadow: var(--gpt-content-shadow);
  overflow: hidden;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: clamp(1rem, 1.5vw, 2rem);
}

.theme-toggle {
  padding: clamp(0.75rem, 1vw, 1rem);
  border-radius: clamp(0.5rem, 0.75vw, 0.75rem);
  color: var(--gpt-text);
  background: var(--gpt-button-bg);
  border: 2px solid var(--gpt-border);
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-toggle:hover {
  background: var(--gpt-button-hover-bg);
  border-color: var(--gpt-text);
}

.theme-toggle svg {
  width: clamp(20px, 1.5vw, 28px);
  height: clamp(20px, 1.5vw, 28px);
}

.user-info {
  display: flex;
  align-items: center;
  padding: clamp(1.25rem, 1.5vw, 2rem);
  border-top: 1px solid var(--gpt-border);
  gap: clamp(1rem, 1.2vw, 1.5rem);
}

.user-avatar {
  width: clamp(40px, 2.5vw, 56px);
  height: clamp(40px, 2.5vw, 56px);
  border-radius: 50%;
  background: var(--gpt-text);
  color: var(--gpt-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: clamp(1.1rem, 1.2vw, 1.4rem);
}

.user-name {
  font-size: clamp(1.1rem, 1.2vw, 1.4rem);
  color: var(--gpt-text);
  font-weight: 500;
}

/* Update color variables for black and white theme */
:root {
  --gpt-bg: #ffffff;
  --gpt-text: #202123;
  --gpt-text-secondary: #6b7280;
  --gpt-sidebar-bg: #f0f0f0;
  --gpt-main-bg: #ffffff;
  --gpt-header-bg: #ffffff;
  --gpt-content-bg: #ffffff;
  --gpt-border: #e5e7eb;
  --gpt-hover-bg: #e7e7e8;
  --gpt-active-bg: #ddddde;
  --gpt-active-text: #202123;
  --gpt-button-bg: #ffffff;
  --gpt-button-hover-bg: #f3f4f6;
  --gpt-content-shadow: 0 0 15px rgba(0,0,0,0.1);
  --gpt-accent: #202123;
  --gpt-icon-filter: none;
}

:root.dark {
  --gpt-bg: #343541;
  --gpt-text: #ffffff;
  --gpt-text-secondary: #9ca3af;
  --gpt-sidebar-bg: #202123;
  --gpt-main-bg: #343541;
  --gpt-header-bg: #343541;
  --gpt-content-bg: #444654;
  --gpt-border: #4b5563;
  --gpt-hover-bg: #2a2b32;
  --gpt-active-bg: #343541;
  --gpt-active-text: #ffffff;
  --gpt-button-bg: #40414f;
  --gpt-button-hover-bg: #4b5563;
  --gpt-content-shadow: 0 0 15px rgba(0,0,0,0.2);
  --gpt-accent: #ffffff;
  --gpt-icon-filter: brightness(1);
}

/* Transitions */
* {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* 媒体查询用于超大屏幕 */
@media (min-width: 2560px) {
  .gpt-menu-item {
    padding: 1.5rem 2.5rem;
  }
  
  .gpt-chat-section {
    padding: 3rem;
  }
  
  .gpt-chat-center {
    border-radius: 2rem;
  }
}
</style>

