<template>
  <n-space vertical size="large" class="pii-naive-bg">
    <n-card class="pii-naive-card" :bordered="false" hoverable>
      <template #header>
        <n-space align="center">
          <img src="../assets/lock.svg" alt="lock" style="width:36px;height:36px;" />
          <span style="font-size:1.3rem;font-weight:600;">医疗数据合规智能体</span>
        </n-space>
        <div class="pii-naive-subtitle">个人信息检测与风险评估</div>
      </template>
      <n-tabs type="line" animated>
        <n-tab-pane name="text" tab="文本输入">
          <n-form>
            <n-form-item>
              <n-input
                v-model:value="text"
                type="textarea"
                :autosize="{ minRows: 4, maxRows: 8 }"
                placeholder="请输入待检测文本..."
                :disabled="loading"
                class="pii-naive-input"
              />
            </n-form-item>
            <n-form-item>
              <n-button type="primary" strong block :loading="loading" :disabled="!text" @click="detectPIIHandler">
                检测
              </n-button>
            </n-form-item>
          </n-form>
        </n-tab-pane>
        <n-tab-pane name="file" tab="文件上传">
          <n-upload
            :custom-request="handleFileUpload"
            :show-file-list="false"
            accept=".txt,.pdf,.doc,.docx"
            :disabled="loading"
          >
            <n-button type="primary" :loading="loading">选择文件</n-button>
          </n-upload>
          <n-input
            v-model:value="fileContent"
            type="textarea"
            :autosize="{ minRows: 4, maxRows: 8 }"
            placeholder="文件内容将显示在此处"
            :disabled="true"
            class="pii-naive-input"
            style="margin-top: 12px;"
          />
          <n-form-item>
            <n-button type="primary" strong block :loading="loading" :disabled="!fileContent" @click="detectFileContent">
              检测
            </n-button>
          </n-form-item>
        </n-tab-pane>
      </n-tabs>
      <n-divider v-if="result" />
      <n-alert v-if="result" type="info" show-icon class="pii-naive-result">
        <template #header>
          检测结果
        </template>
        <div class="risk">风险等级：<b :class="result.risk_level?.toLowerCase()">{{ result.risk_level }}</b></div>
        <n-list>
          <n-list-item v-for="(entity, idx) in result.entities" :key="idx">
            <n-space>
              <n-tag type="info">类型: {{ entity.type }}</n-tag>
              <n-tag>位置: {{ entity.start }}-{{ entity.end }}</n-tag>
              <n-tag type="success">置信度: {{ entity.score }}</n-tag>
            </n-space>
          </n-list-item>
        </n-list>
      </n-alert>
    </n-card>
  </n-space>
</template>

<script setup>
import { ref } from 'vue';
import { NCard, NSpace, NInput, NButton, NForm, NFormItem, NAlert, NDivider, NList, NListItem, NTag, NUpload, NTabs, NTabPane } from 'naive-ui';
import { detectPII } from '../api/pii';

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
      const res = await detectPII(content);  // 这里和文本一致，发送 JSON
      result.value = res.data;
    };
    reader.readAsText(file.file);  // 不区分 txt 或 docx 等，只读文本
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

