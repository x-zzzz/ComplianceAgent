<template>
  <div class="chat-container">
    <div class="chat-messages" v-if="desensitizeResult">
      <div class="gpt-desensitize-result">
        <div class="gpt-summary-title">脱敏处理结果</div>
        <div class="gpt-summary-row">
          <span>脱敏后文本：</span>
          <div class="gpt-desensitized-text">{{ desensitizeResult }}</div>
        </div>
      </div>
    </div>
    
    <div class="chat-input-container">
      <div class="input-wrapper">
        <n-input
          v-model:value="desensitizeText"
          type="textarea"
          :autosize="{ minRows: 3, maxRows: 12 }"
          placeholder="请输入待脱敏文本..."
          :disabled="desensitizeLoading"
          class="gpt-input"
        />
        
        <div class="input-buttons">
          <button 
            class="icon-button" 
            :disabled="!desensitizeText || desensitizeLoading"
            @click="handleDesensitize"
            title="开始脱敏"
          >
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          
          <button 
            v-if="desensitizeDownloadUrl"
            class="icon-button"
            @click="downloadDesensitizedText"
            title="下载脱敏后文本"
          >
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 15V3m0 12l-4-4m4 4l4-4M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { NInput, NButton, NIcon } from 'naive-ui';
import { desensitizePII, detectPII } from '../api/pii';

const props = defineProps({
  modelValue: String,
});
const emit = defineEmits(['update:modelValue', 'update:desensitizeResult']);

const desensitizeText = ref('');
const desensitizeResult = ref('');
const desensitizeLoading = ref(false);
const desensitizeDownloadUrl = ref('');

async function handleDesensitize() {
  desensitizeLoading.value = true;
  try {
    // 自动检测PII实体
    let piiEntities = [];
    const detectRes = await detectPII(desensitizeText.value);
    if (detectRes.data && detectRes.data.details) {
      detectRes.data.details.forEach(item => {
        if (item.entities && Array.isArray(item.entities)) {
          piiEntities.push(...item.entities);
        }
      });
    }
    piiEntities = Array.from(new Set(piiEntities));
    // 脱敏API
    const res = await desensitizePII(desensitizeText.value, piiEntities);
    desensitizeResult.value = res.data && res.data.desensitized_text ? res.data.desensitized_text : '';
    emit('update:desensitizeResult', desensitizeResult.value);
    // 生成下载链接
    if (desensitizeResult.value) {
      const blob = new Blob([desensitizeResult.value], { type: 'text/plain' });
      desensitizeDownloadUrl.value = URL.createObjectURL(blob);
    } else {
      desensitizeDownloadUrl.value = '';
    }
  } finally {
    desensitizeLoading.value = false;
  }
}

function downloadDesensitizedText() {
  if (!desensitizeDownloadUrl.value) return;
  const a = document.createElement('a');
  a.href = desensitizeDownloadUrl.value;
  a.download = 'desensitized_text.txt';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
</script>

<style scoped>
.chatgpt-input-area {
  width: 100%;
  margin: 0 0 18px 0;
}
.chatgpt-title-row {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}
.chatgpt-title-main {
  font-size: 2rem;
  font-weight: 700;
  color: #222;
  text-align: center;
}
.chatgpt-desc {
  color: #888;
  font-size: 1.02rem;
  text-align: center;
  margin-bottom: 18px;
}
.chatgpt-action-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}
.chatgpt-btn {
  border-radius: 50% !important;
  min-width: 48px;
  min-height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  box-shadow: 0 2px 8px #e0e6ed;
}
.chatgpt-tip {
  color: #bbb;
  font-size: 0.95rem;
  text-align: right;
  margin-bottom: 8px;
}
/* 强制 n-input textarea 圆角和背景 */
.n-input__textarea {
  border-radius: 18px !important;
  background: #f7f7f8 !important;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-height: calc(100vh - 76px);
  background: var(--gpt-bg);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 2rem 0;
}

.chat-input-container {
  border-top: 1px solid var(--gpt-border);
  padding: 1.5rem;
  background: var(--gpt-bg);
  position: relative;
}

.input-wrapper {
  position: relative;
  max-width: min(65vw, 60rem);
  margin: 0 auto;
  background: var(--gpt-content-bg);
  border: 1px solid var(--gpt-border);
  border-radius: 1.5rem;
  padding: 1rem;
  box-shadow: var(--gpt-content-shadow);
  transition: all 0.3s ease;
}

.input-wrapper:hover {
  box-shadow: 0 0 20px rgba(0,0,0,0.15);
}

.gpt-input {
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

:deep(.n-input__textarea-mirror) {
  padding: 1rem !important;
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

.gpt-desensitize-result {
  margin: 2rem auto;
  max-width: min(65vw, 60rem);
  padding: 1.5rem;
  background: var(--gpt-content-bg);
  border-radius: 1.25rem;
  border: 1px solid var(--gpt-border);
  box-shadow: var(--gpt-content-shadow);
}

.gpt-summary-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--gpt-text);
}

.gpt-summary-row {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  color: var(--gpt-text);
}

.gpt-desensitized-text {
  background: var(--gpt-hover-bg);
  padding: 1rem;
  border-radius: 0.75rem;
  line-height: 1.6;
}
</style>
