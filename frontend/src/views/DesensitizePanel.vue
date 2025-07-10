<template>
  <div class="gpt-desensitize-section gpt-panel-card chatgpt-panel-card">
    <div class="gpt-feature-title" style="margin-bottom: 16px;">
      <n-icon size="40" color="#409eff" style="vertical-align: middle; margin-right: 10px;">
        <svg viewBox="0 0 24 24" fill="none"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" fill="#409eff"/></svg>
      </n-icon>
      <span class="gpt-feature-title-text">脱敏处理</span>
    </div>
    <div class="gpt-feature-desc" style="margin-bottom: 24px;">对检测到的敏感信息进行脱敏处理，保护个人隐私。</div>
    <div class="gpt-input-area-adaptive">
      <n-input
        v-model:value="desensitizeText"
        type="textarea"
        :autosize="{ minRows: 4, maxRows: 8 }"
        placeholder="请输入待脱敏文本..."
        :disabled="desensitizeLoading"
        class="gpt-input gpt-input-rounded"
      />
    </div>
    <div class="gpt-action-bar">
      <n-button type="primary" size="large" class="gpt-desensitize-btn" :loading="desensitizeLoading" :disabled="!desensitizeText" @click="handleDesensitize">
        <n-icon size="24" style="margin-right: 4px;"><svg viewBox="0 0 24 24" fill="none"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" fill="#fff"/></svg></n-icon>
        脱敏处理
      </n-button>
    </div>
    <div v-if="desensitizeResult" class="gpt-desensitize-result" style="margin-top: 16px;">
      <div class="gpt-summary-title">脱敏处理结果</div>
      <div class="gpt-summary-row">
        <span>脱敏后文本：</span>
        <div class="gpt-desensitized-text">{{ desensitizeResult }}</div>
      </div>
      <div v-if="desensitizeDownloadUrl" class="gpt-summary-row">
        <n-button type="default" size="small" :disabled="desensitizeLoading" @click="downloadDesensitizedText">
          <n-icon size="16" style="margin-right: 4px;"><svg viewBox="0 0 24 24" fill="none"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" fill="#409eff"/></svg></n-icon>
          下载脱敏文本
        </n-button>
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
/* 复用主样式，圆角由主文件控制 */
</style>
