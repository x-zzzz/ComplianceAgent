<template>
  <div class="gpt-panel-card chatgpt-panel-card">
    <div class="chatgpt-title-row">
      <n-icon size="48" color="#409eff" style="vertical-align: middle; margin-right: 12px;">
        <svg viewBox="0 0 24 24" fill="none"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" fill="#409eff"/></svg>
      </n-icon>
      <span class="chatgpt-title-main">智能检测医疗文本中的敏感信息与风险</span>
    </div>
    <div class="chatgpt-desc">本功能可自动识别医疗文本中的敏感个人信息，并评估其风险等级，助力数据合规。</div>
    <div class="gpt-input-area-adaptive chatgpt-input-area">
      <n-input
        v-model:value="text"
        type="textarea"
        :autosize="{ minRows: 6, maxRows: 12 }"
        placeholder="请输入待检测文本..."
        :disabled="loading"
        class="gpt-input chatgpt-input-rounded"
      />
    </div>
    <div class="gpt-action-bar chatgpt-action-bar">
      <n-upload
        :custom-request="handleFileUpload"
        :show-file-list="false"
        accept=".txt,.pdf,.doc,.docx"
        :disabled="loading"
      >
        <n-button quaternary circle size="large" class="gpt-upload-btn chatgpt-btn" :loading="loading">
          <n-icon size="24"><svg viewBox="0 0 24 24" fill="none"><path d="M12 16V4m0 0l-4 4m4-4l4 4" stroke="#409eff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="4" y="16" width="16" height="4" rx="2" fill="#409eff"/></svg></n-icon>
        </n-button>
      </n-upload>
      <n-button type="primary" size="large" class="gpt-detect-btn chatgpt-btn" :loading="loading" :disabled="!text && !fileContent" @click="detectPIIHandler">
        <n-icon size="24"><svg viewBox="0 0 24 24" fill="none"><path d="M5 13l4 4L19 7" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></n-icon>
      </n-button>
    </div>
    <div class="gpt-upload-tip chatgpt-tip">支持上传 .txt/.pdf/.doc/.docx 文件，或直接粘贴文本</div>
    <div v-if="fileContent" class="gpt-file-preview chatgpt-input-area">
      <n-input
        v-model:value="fileContent"
        type="textarea"
        :autosize="{ minRows: 3, maxRows: 8 }"
        placeholder="文件内容将显示在此处"
        :disabled="true"
        class="gpt-input chatgpt-input-rounded"
      />
    </div>
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
        <span class="gpt-summary-reason chatgpt-desc">{{ result.overall_reason }}</span>
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
          <span class="gpt-summary-reason chatgpt-desc">{{ item.reason }}</span>
        </div>
      </n-collapse-item>
    </n-collapse>
    <div v-if="result && result.details && !result.details.length" style="text-align:center;color:#aaa;margin-top:32px;">
      未检测到敏感个人信息。
    </div>
    <n-collapse v-if="result && result.raw_response && result.raw_response.content" class="gpt-pii-collapse" style="margin-top:18px;">
      <n-collapse-item title="原始检测内容（调试用）">
        <pre style="white-space:pre-wrap;word-break:break-all;font-size:0.98rem;color:#888;background:#f8fafc;padding:12px 16px;border-radius:8px;">{{ result.raw_response.content }}</pre>
      </n-collapse-item>
    </n-collapse>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { NInput, NButton, NUpload, NIcon, NCollapse, NCollapseItem } from 'naive-ui';
import { detectPII } from '../api/pii';

const props = defineProps({
  modelValue: String,
});
const emit = defineEmits(['update:modelValue', 'update:result']);

const text = ref('');
const fileContent = ref('');
const result = ref(null);
const loading = ref(false);

async function detectPIIHandler() {
  if (!text.value) return;
  loading.value = true;
  try {
    const res = await detectPII(text.value);
    result.value = res.data;
    emit('update:result', res.data);
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
      emit('update:result', res.data);
    };
    reader.readAsText(file.file);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.chatgpt-input-area {
  width: 100%;
  margin: 0 0 18px 0;
}
.chatgpt-input-rounded {
  border-radius: 18px !important;
}
.n-input__textarea {
  border-radius: 18px !important;
  background: #f7f7f8 !important;
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
</style>
