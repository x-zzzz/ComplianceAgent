<template>
  <div class="gpt-desensitize-section gpt-panel-card chatgpt-panel-card">
    <div class="chatgpt-title-row">
      <n-icon size="48" color="#409eff" style="vertical-align: middle; margin-right: 12px;">
        <svg viewBox="0 0 24 24" fill="none"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" fill="#409eff"/></svg>
      </n-icon>
      <span class="chatgpt-title-main">脱敏处理</span>
    </div>
    <div class="chatgpt-desc">对检测到的敏感信息进行脱敏处理，保护个人隐私。</div>
    <div class="gpt-input-area-adaptive chatgpt-input-area">
      <n-input
        v-model:value="desensitizeText"
        type="textarea"
        :autosize="{ minRows: 6, maxRows: 12 }"
        placeholder="请输入待脱敏文本..."
        :disabled="desensitizeLoading"
        class="gpt-input chatgpt-input-rounded"
        style="border-radius:18px;background:#f7f7f8;border:1.5px solid #e0e0e0;"
      />
    </div>
    <div class="gpt-action-bar chatgpt-action-bar">
      <n-button type="primary" size="large" class="gpt-desensitize-btn chatgpt-btn" :loading="desensitizeLoading" :disabled="!desensitizeText" @click="handleDesensitize">
        <n-icon size="24"><svg viewBox="0 0 24 24" fill="none"><path d="M5 13l4 4L19 7" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></n-icon>
      </n-button>
      <n-button v-if="desensitizeDownloadUrl" type="default" size="large" class="chatgpt-btn" :disabled="desensitizeLoading" @click="downloadDesensitizedText">
        <n-icon size="22"><svg viewBox="0 0 24 24" fill="none"><path d="M12 16V4m0 0l-4 4m4-4l4 4" stroke="#409eff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="4" y="16" width="16" height="4" rx="2" fill="#409eff"/></svg></n-icon>
      </n-button>
    </div>
    <div class="chatgpt-tip">点击右侧按钮可下载脱敏文本</div>
    <div v-if="desensitizeResult" class="gpt-desensitize-result" style="margin-top: 16px;">
      <div class="gpt-summary-title">脱敏处理结果</div>
      <div class="gpt-summary-row">
        <span>脱敏后文本：</span>
        <div class="gpt-desensitized-text">{{ desensitizeResult }}</div>
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
</style>
