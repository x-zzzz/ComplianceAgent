<template>
  <div class="chat-container">
    <!-- Header -->
    <div class="app-header">
      <div class="app-branding">
        <h1 class="app-title">PII检测</h1>
      </div>
      <div class="header-controls">
        <div class="model-select-wrapper">
          <n-select
            class="model-select"
            v-model:value="selectedModel"
            :options="modelOptions"
            placeholder="选择模型"
            size="large"
          />
        </div>
        <div class="header-actions">
          <n-button class="header-button" quaternary circle size="large">
            <template #icon>
              <n-icon size="24"><UserOutlined /></n-icon>
            </template>
          </n-button>
          <n-button class="header-button" quaternary circle size="large">
            <template #icon>
              <n-icon size="24"><SettingOutlined /></n-icon>
            </template>
          </n-button>
          <n-button class="theme-toggle" circle quaternary size="large">
            <template #icon>
              <n-icon size="24">
                <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              </n-icon>
            </template>
          </n-button>
        </div>
      </div>
    </div>

    <!-- Messages Area -->
    <div class="chat-messages" ref="messagesRef">
      <div v-if="piiResult" class="message">
        <div class="message-content">
          <div class="pii-result">
            <!-- 原始文本部分 -->
            <div v-if="piiResult.text" class="result-section text-section">
              <div class="section-header">
                <h3>原始文本</h3>
              </div>
              <p class="text-content">{{ piiResult.text }}</p>
            </div>

            <!-- 风险概览部分 -->
            <div v-if="piiResult?.summary" class="result-section summary-section">
              <div class="risk-overview">
                <div class="risk-badge" :class="piiResult.summary.risk_level">
                  <span class="risk-level">{{ piiResult.summary.risk_level }}风险</span>
                  <span class="entity-count">发现 {{ piiResult.summary.total_entities }} 项敏感信息</span>
                </div>
                <div class="risk-explanation">
                  <p>{{ piiResult.summary.overall_reason }}</p>
                </div>
              </div>
            </div>

            <!-- 详细信息部分 -->
            <div v-if="piiResult.details?.length" class="result-section details-section">
              <div class="section-header">
                <h3>敏感信息详情</h3>
              </div>
              <div class="details-grid">
                <div v-for="(detail, index) in piiResult.details" 
                     :key="index" 
                     class="detail-card"
                     :class="detail.risk_level">
                  <div class="detail-header">
                    <div class="risk-tag" :class="detail.risk_level">{{ detail.risk_level }}风险</div>
                  </div>
                  <div class="detail-content">
                    <div class="entities-list">
                      <div v-for="(entity, entityIndex) in detail.entities" 
                           :key="entityIndex"
                           class="entity-item">
                        {{ entity }}
                      </div>
                    </div>
                    <div class="detail-reason">
                      <p>{{ detail.reason }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="chat-input-container">
      <div class="input-wrapper">
        <n-input
          v-model:value="inputText"
          type="textarea"
          :placeholder="placeholder"
          class="chat-input"
          :autosize="{ minRows: 1, maxRows: 6 }"
          @keydown.enter.prevent="handleEnter"
        />
        <div class="input-buttons">
          <button class="icon-button" :disabled="!inputText" @click="clearInput">
            <n-icon><CloseOutlined /></n-icon>
          </button>
          <button
            class="send-button"
            :disabled="!inputText || loading"
            @click="detectPII"
          >
            <n-icon><SendOutlined /></n-icon>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { NInput, NSelect, NButton, NIcon } from 'naive-ui'
import { UserOutlined, SettingOutlined, SendOutlined, CloseOutlined } from '@vicons/antd'
import { detectPII as apiDetectPII } from '@/api/pii'

const inputText = ref('')
const loading = ref(false)
const piiResult = ref(null)
const messagesRef = ref(null)
const selectedModel = ref('presidio')

const modelOptions = [
  {
    label: 'Presidio',
    value: 'presidio'
  },
  {
    label: 'DeepSeek',
    value: 'deepseek'
  }
]

const placeholder = '请输入需要检测的文本...'

const clearInput = () => {
  inputText.value = ''
}

const handleEnter = (e) => {
  if (!e.shiftKey && !e.isComposing) {
    detectPII()
  }
}

const detectPII = async () => {
  if (!inputText.value || loading.value) return

  loading.value = true
  try {
    const response = await apiDetectPII(inputText.value, selectedModel.value)
    piiResult.value = response.data
    inputText.value = ''
    
    // Scroll to bottom after results are shown
    setTimeout(() => {
      if (messagesRef.value) {
        messagesRef.value.scrollTop = messagesRef.value.scrollHeight
      }
    }, 100)
  } catch (error) {
    console.error('PII detection failed:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  padding: 2rem 0;
}

.app-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2.5rem;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--gpt-border);
  z-index: 10;
}

.app-branding {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.app-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--gpt-text);
  margin: 0;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.model-select-wrapper {
  min-width: 200px;
}

.model-select :deep(.n-base-selection) {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid var(--gpt-border);
  border-radius: 12px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-button,
.theme-toggle {
  width: 44px !important;
  height: 44px !important;
  border-radius: 12px !important;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gpt-text);
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8) !important;
  border: 1px solid var(--gpt-border) !important;
}

.header-button:hover,
.theme-toggle:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.9) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  margin-top: 4rem;
}

.message {
  display: flex;
  justify-content: center;
  padding: 1.5rem 1rem;
}

.message-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.pii-result {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.result-section {
  background: var(--gpt-content-bg);
  border-radius: 1rem;
  margin-bottom: 2rem;
  border: 1px solid var(--gpt-border);
  overflow: hidden;
}

.section-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--gpt-border);
  background: rgba(0, 0, 0, 0.02);
}

.section-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--gpt-text);
  margin: 0;
}

.result-section p,
.result-section ul {
  margin: 0;
  line-height: 1.6;
}

.result-section ul {
  padding-left: 1.5rem;
}

/* 风险概览样式 */
.risk-overview {
  padding: 1.5rem;
}

.risk-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  border-radius: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.risk-badge.高 {
  background-color: #fef2f2;
  color: #dc2626;
}

.risk-badge.中 {
  background-color: #fff7ed;
  color: #ea580c;
}

.risk-badge.低 {
  background-color: #f0fdf4;
  color: #16a34a;
}

.risk-level {
  font-size: 1.25rem;
  margin-right: 1rem;
}

.entity-count {
  font-size: 1rem;
  opacity: 0.8;
}

.risk-explanation {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--gpt-text);
}

/* 详细信息网格布局 */
.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  padding: 1.5rem;
}

.detail-card {
  background: var(--gpt-content-bg);
  border-radius: 0.75rem;
  border: 1px solid var(--gpt-border);
  overflow: hidden;
  transition: all 0.3s ease;
}

.detail-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.detail-card.高 {
  border-left: 4px solid #dc2626;
}

.detail-card.中 {
  border-left: 4px solid #ea580c;
}

.detail-card.低 {
  border-left: 4px solid #16a34a;
}

.detail-header {
  padding: 1rem;
  border-bottom: 1px solid var(--gpt-border);
  background: rgba(0, 0, 0, 0.02);
}

.risk-tag {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 600;
}

.risk-tag.高 {
  background-color: #fef2f2;
  color: #dc2626;
}

.risk-tag.中 {
  background-color: #fff7ed;
  color: #ea580c;
}

.risk-tag.低 {
  background-color: #f0fdf4;
  color: #16a34a;
}

.detail-content {
  padding: 1rem;
}

.entities-list {
  margin-bottom: 1rem;
}

.entity-item {
  font-size: 1.1rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.03);
  margin-bottom: 0.5rem;
}

.detail-reason {
  font-size: 0.95rem;
  color: var(--gpt-text-secondary);
  line-height: 1.5;
}

/* 文本内容样式 */
.text-content {
  padding: 1.5rem;
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--gpt-text);
}

/* 动画效果 */
.message-enter-active,
.message-leave-active {
  transition: all 0.3s ease;
}

.message-enter-from,
.message-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

@media (max-width: 768px) {
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .message-content {
    padding: 1rem;
  }
}

.chat-input-container {
  position: relative;
  padding: 1.5rem 1rem;
  border-top: 1px solid var(--gpt-border);
}

.input-wrapper {
  position: relative;
  max-width: min(65vw, 60rem);
  margin: 0 auto;
  background: var(--gpt-content-bg);
  border: 1px solid var(--gpt-border);
  border-radius: 1.5rem;
  padding: 1rem;
  box-shadow: 0 0 15px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.input-wrapper:hover {
  box-shadow: 0 0 20px rgba(0,0,0,0.15);
}

.chat-input {
  width: 100%;
  padding-right: 6rem;
}

:deep(.n-input) {
  background: transparent !important;
}

:deep(.n-input__textarea) {
  min-height: 4.5rem !important;
  padding: 1rem !important;
  border-radius: 1.25rem !important;
  font-size: 1rem !important;
  line-height: 1.5 !important;
  background: transparent !important;
}

.input-buttons {
  position: absolute;
  right: 1rem;
  bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.icon-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border: none;
  background: var(--gpt-button-bg);
  color: var(--gpt-text);
  cursor: pointer;
  border-radius: 0.75rem;
  transition: all 0.3s ease;
  border: 1px solid var(--gpt-border);
}

.icon-button:hover {
  background: var(--gpt-hover-bg);
  transform: scale(1.05);
}

.icon-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.send-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border: none;
  background: var(--gpt-text);
  color: var(--gpt-bg);
  cursor: pointer;
  border-radius: 0.75rem;
  transition: all 0.3s ease;
}

.send-button:hover:not(:disabled) {
  transform: scale(1.05);
  opacity: 0.9;
}

.send-button:disabled {
  background: var(--gpt-border);
  cursor: not-allowed;
  transform: none;
}
</style>
