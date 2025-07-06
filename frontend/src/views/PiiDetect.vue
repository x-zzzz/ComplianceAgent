<template>
  <div class="gpt-root">
    <aside class="gpt-sidebar">
      <div class="gpt-sidebar-header">
        <img src="../assets/lock.svg" alt="lock" class="gpt-logo" />
        <span class="gpt-title">医疗数据合规智能体</span>
      </div>
      <nav class="gpt-menu">
        <div v-for="item in menuOptions" :key="item.key" :class="['gpt-menu-item', {active: activeMenu === item.key}]" @click="activeMenu = item.key">
          {{ item.label }}
        </div>
      </nav>
    </aside>
    <main class="gpt-main">
      <header class="gpt-main-header">
        <span class="gpt-main-title">个人信息检测与风险评估</span>
      </header>
      <section class="gpt-chat-section">
        <div class="gpt-chat-center">
          <div class="gpt-feature-title">
            <n-icon size="40" color="#409eff" style="vertical-align: middle; margin-right: 10px;">
              <svg viewBox="0 0 24 24" fill="none"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" fill="#409eff"/></svg>
            </n-icon>
            <span class="gpt-feature-title-text">智能检测医疗文本中的敏感信息与风险</span>
          </div>
          <div class="gpt-feature-desc">本功能可自动识别医疗文本中的敏感个人信息，并评估其风险等级，助力数据合规。</div>
          <div class="gpt-input-area-adaptive">
            <n-input
              v-model:value="text"
              type="textarea"
              :autosize="{ minRows: 4, maxRows: 8 }"
              placeholder="请输入待检测文本..."
              :disabled="loading"
              class="gpt-input gpt-input-rounded"
            />
          </div>
          <div class="gpt-action-bar">
            <n-upload
              :custom-request="handleFileUpload"
              :show-file-list="false"
              accept=".txt,.pdf,.doc,.docx"
              :disabled="loading"
            >
              <n-button quaternary circle size="large" class="gpt-upload-btn" :loading="loading">
                <n-icon size="24"><svg viewBox="0 0 24 24" fill="none"><path d="M12 16V4m0 0l-4 4m4-4l4 4" stroke="#409eff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="4" y="16" width="16" height="4" rx="2" fill="#409eff"/></svg></n-icon>
              </n-button>
            </n-upload>
            <n-button type="primary" size="large" class="gpt-detect-btn" :loading="loading" :disabled="!text && !fileContent" @click="detectPIIHandler">
              <n-icon size="24" style="margin-right: 4px;"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="#fff" stroke-width="2"/><path d="M8 12l2 2 4-4" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></n-icon>
              检测
            </n-button>
          </div>
          <div class="gpt-upload-tip">支持上传 .txt/.pdf/.doc/.docx 文件，或直接粘贴文本</div>
          <div v-if="fileContent" class="gpt-file-preview">
            <n-input
              v-model:value="fileContent"
              type="textarea"
              :autosize="{ minRows: 2, maxRows: 6 }"
              placeholder="文件内容将显示在此处"
              :disabled="true"
              class="gpt-input"
            />
          </div>

          <!-- 检测结果总览，直接展开显示 -->
          <div v-if="result && result.total_entities !== undefined" class="gpt-pii-summary gpt-pii-summary-unfold">
            <div class="gpt-summary-row">
              <span>发现敏感个人信息总数：</span>
              <b>{{ result.total_entities }}</b>
            </div>
            <div class="gpt-summary-row">
              <span>整体风险等级：</span>
              <b :class="['risk', result.risk_level]">{{ result.risk_level }}</b>
            </div>
            <div class="gpt-summary-row">
              <span>合规风险说明：</span>
              <span class="gpt-summary-reason">{{ result.overall_reason }}</span>
            </div>
          </div>

          <n-collapse v-if="result && result.details && result.details.length" class="gpt-pii-collapse" accordion>
            <n-collapse-item v-for="(item, idx) in result.details" :key="idx" :title="'敏感信息 ' + (idx+1)">
              <div class="entities">
                <b>敏感信息内容：</b>
                <ul>
                  <li v-for="(e, i) in item.entities" :key="i">{{ e }}</li>
                </ul>
              </div>
              <div>
                <b>风险等级：</b>
                <span :class="['risk', item.risk_level]">{{ item.risk_level }}</span>
              </div>
              <div>
                <b>合规说明：</b>
                <span class="gpt-summary-reason">{{ item.reason }}</span>
              </div>
            </n-collapse-item>
          </n-collapse>

          <div v-if="result && result.details && !result.details.length" style="text-align:center;color:#aaa;margin-top:32px;">
            未检测到敏感个人信息。
          </div>

          <!-- 原始内容调试展示（可選） -->
          <n-collapse v-if="result && result.raw_response && result.raw_response.content" class="gpt-pii-collapse" style="margin-top:18px;">
            <n-collapse-item title="原始检测内容（调试用）">
              <pre style="white-space:pre-wrap;word-break:break-all;font-size:0.98rem;color:#888;background:#f8fafc;padding:12px 16px;border-radius:8px;">{{ result.raw_response.content }}</pre>
            </n-collapse-item>
          </n-collapse>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { NCard, NSpace, NInput, NButton, NForm, NFormItem, NAlert, NDivider, NList, NListItem, NTag, NUpload, NTabs, NTabPane, NMenu, NIcon, NCollapse, NCollapseItem } from 'naive-ui';
import { detectPII } from '../api/pii';

const text = ref('');
const fileContent = ref('');
const result = ref(null);
const loading = ref(false);
const activeMenu = ref('pii');
const menuOptions = [
  { label: 'PII检测', key: 'pii' },
  { label: '脱敏处理', key: 'desensitize' },
  { label: '敏感词扫描', key: 'sensitive_words' },
  { label: '合规风险评估', key: 'risk_assess' },
  { label: '合规知识库问答', key: 'qa' },
  { label: '合规报告生成', key: 'report' },
  { label: '数据合规建议', key: 'advice' },
  { label: '日志与历史记录', key: 'history' },
  { label: '系统设置', key: 'settings' }
];

async function detectPIIHandler() {
  if (!text.value) return;
  loading.value = true;
  try {
    const res = await detectPII(text.value);
    result.value = res.data;
  } finally {
    loading.value = false;
  }
}

async function handleFileUpload({ file }) {
  loading.value = true;
  fileContent.value = '';
  result.value = null;
  try {
    const reader = new FileReader();
    reader.onload = async e => {
      const content = e.target.result;
      fileContent.value = content;
      const res = await detectPII(content);
      result.value = res.data;
    };
    reader.readAsText(file.file);
  } finally {
    loading.value = false;
  }
}

async function detectFileContent() {
  if (!fileContent.value) return;
  loading.value = true;
  try {
    const res = await detectPII(fileContent.value);
    result.value = res.data;
  } finally {
    loading.value = false;
  }
}
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
</style>

