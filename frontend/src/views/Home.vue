<template>
  <div class="bg-white text-gray-900">
    <!-- Hero Section -->
    <section class="min-h-screen flex flex-col items-center justify-center text-center px-6">
      <img src="../assets/compliance_bot.svg" alt="合规智能体" class="w-20 h-20 mb-6" />
      <h1 class="text-4xl md:text-5xl font-bold mb-4">合规智能体平台</h1>
      <p class="text-lg md:text-xl text-gray-600 mb-8">
        让数据合规更智能 · 更高效 · 更安全
      </p>
      <div class="flex flex-col sm:flex-row gap-4">
        <router-link to="/pii">
          <button class="bg-black text-white px-6 py-3 rounded-full text-sm hover:bg-gray-800 transition">
            立即体验
          </button>
        </router-link>
        <a href="#features" class="text-black px-6 py-3 border border-black rounded-full text-sm hover:bg-gray-100 transition">
          了解更多
        </a>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-24 bg-gray-50 px-6">
      <h2 class="text-3xl font-semibold text-center mb-16">平台核心能力</h2>
      <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
        <div>
          <img src="../assets/pii.svg" class="w-16 h-16 mx-auto mb-4" />
          <h3 class="text-xl font-semibold mb-2">PII智能检测</h3>
          <p class="text-gray-600">自动识别文本中的敏感个人信息，精准标注风险点。</p>
        </div>
        <div>
          <img src="../assets/desensitize.svg" class="w-16 h-16 mx-auto mb-4" />
          <h3 class="text-xl font-semibold mb-2">智能脱敏处理</h3>
          <p class="text-gray-600">对敏感信息进行智能脱敏，保护隐私安全。</p>
        </div>
        <div>
          <img src="../assets/risk_assess.svg" class="w-16 h-16 mx-auto mb-4" />
          <h3 class="text-xl font-semibold mb-2">风险评估与建议</h3>
          <p class="text-gray-600">多维度评估数据合规风险，输出专业建议。</p>
        </div>
      </div>
    </section>

    <!-- Why Us Section -->
    <section class="py-24 px-6">
      <h2 class="text-3xl font-semibold text-center mb-16">为什么选择我们？</h2>
      <div class="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
        <div>
          <h3 class="text-xl font-semibold mb-2 text-blue-600">AI驱动</h3>
          <p class="text-gray-600">融合大模型与知识库，合规更智能。</p>
        </div>
        <div>
          <h3 class="text-xl font-semibold mb-2 text-blue-600">极致体验</h3>
          <p class="text-gray-600">极简交互，秒级响应，支持多端访问。</p>
        </div>
        <div>
          <h3 class="text-xl font-semibold mb-2 text-blue-600">安全可信</h3>
          <p class="text-gray-600">全流程留痕，数据不出本地，合规可追溯。</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-100 py-8 text-center text-sm text-gray-500">
      © 2025 合规智能体平台 | 智能合规 · 安全可信 · 高效便捷
    </footer>
  </div>
</template>

<script setup>
// 无逻辑，仅展示页面
</script>

/* Apple-like smooth scroll 样式已移至全局 index.css */
