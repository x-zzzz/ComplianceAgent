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
          <n-button type="primary" strong block :loading="loading" :disabled="!text" @click="detectPII">
            检测
          </n-button>
        </n-form-item>
      </n-form>
      <n-divider v-if="result" />
      <n-alert v-if="result" type="info" show-icon class="pii-naive-result">
        <template #header>
          检测结果
        </template>
        <div class="risk">风险等级：<b :class="result.risk_level.toLowerCase()">{{ result.risk_level }}</b></div>
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
import { NCard, NSpace, NInput, NButton, NForm, NFormItem, NAlert, NDivider, NList, NListItem, NTag } from 'naive-ui';
import { detectPII } from '../api/pii';

const text = ref('');
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
</script>

<style scoped>
.pii-naive-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #ece9fc 0%, #f7fafd 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.pii-naive-card {
  max-width: 520px;
  width: 100%;
  margin: 48px 0;
  border-radius: 18px;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.12);
}
.pii-naive-subtitle {
  color: #6c757d;
  font-size: 1.05rem;
  margin: 0 0 8px 0;
}
.pii-naive-input {
  font-size: 1.08rem;
}
.pii-naive-result {
  margin-top: 18px;
}
.risk {
  font-size: 1.1rem;
  margin-bottom: 10px;
}
.risk b.low {
  color: #22c55e;
}
.risk b.medium {
  color: #f59e42;
}
.risk b.high {
  color: #ef4444;
}
</style>
