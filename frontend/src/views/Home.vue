<template>
  <div class="overflow-hidden">
    <!-- Hero Section -->
    <section class="min-h-screen relative flex flex-col items-center justify-center text-center px-6 bg-gradient-to-b from-gray-900 to-black text-white overflow-hidden">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-500/20 via-transparent to-transparent animate-pulse"></div>
      <div class="relative z-10 transform transition-all" :class="{ 'translate-y-0 opacity-100': isVisible, 'translate-y-12 opacity-0': !isVisible }">
        <img src="../assets/compliance_bot.svg" alt="合规智能体" class="w-32 h-32 mb-8 animate-float" />
        <h1 class="text-6xl md:text-7xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-300">
          合规智能体平台
        </h1>
        <p class="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto leading-relaxed">
          让数据合规更智能 · 更高效 · 更安全
        </p>
        <div class="flex flex-col sm:flex-row gap-6 justify-center">
          <router-link to="/pii">
            <button class="group relative px-8 py-4 bg-white text-black rounded-full text-lg font-medium overflow-hidden transition-all hover:scale-105">
              <span class="relative z-10">立即体验</span>
              <div class="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></div>
            </button>
          </router-link>
          <a href="#features" class="group px-8 py-4 border border-white/30 backdrop-blur-sm rounded-full text-lg font-medium transition-all hover:bg-white/10">
            了解更多
          </a>
        </div>
      </div>
      <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <svg class="w-6 h-6 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
        </svg>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-32 bg-black text-white overflow-hidden">
      <div class="max-w-7xl mx-auto px-6">
        <h2 class="text-4xl md:text-5xl font-bold text-center mb-24 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          平台核心能力
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-16">
          <div v-for="(feature, index) in features" :key="index" 
               class="feature-card group"
               :class="{ 'fade-up-1': index === 0, 'fade-up-2': index === 1, 'fade-up-3': index === 2 }">
            <div class="relative bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-8 transition-all duration-500 group-hover:transform group-hover:scale-105">
              <div class="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl"></div>
              <img :src="feature.icon" class="w-20 h-20 mb-6 transition-transform group-hover:scale-110" />
              <h3 class="text-2xl font-semibold mb-4">{{ feature.title }}</h3>
              <p class="text-gray-400 text-lg">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Why Us Section -->
    <section class="py-32 bg-gradient-to-b from-black to-gray-900 text-white">
      <div class="max-w-7xl mx-auto px-6">
        <h2 class="text-4xl md:text-5xl font-bold text-center mb-24 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          为什么选择我们？
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-16">
          <div v-for="(reason, index) in reasons" :key="index" 
               class="reason-card backdrop-blur-lg bg-white/5 rounded-2xl p-8 transform transition-all hover:scale-105"
               :class="{ 'fade-up-1': index === 0, 'fade-up-2': index === 1, 'fade-up-3': index === 2 }">
            <h3 class="text-2xl font-semibold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              {{ reason.title }}
            </h3>
            <p class="text-gray-400 text-lg">{{ reason.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-black py-12 text-center text-gray-400">
      <div class="max-w-7xl mx-auto px-6">
        <p class="text-sm">© 2025 合规智能体平台 | 智能合规 · 安全可信 · 高效便捷</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useIntersectionObserver } from '@vueuse/core';

const isVisible = ref(false);

const features = [
  {
    icon: new URL('../assets/pii.svg', import.meta.url).href,
    title: 'PII智能检测',
    description: '自动识别文本中的敏感个人信息，精准标注风险点。'
  },
  {
    icon: new URL('../assets/desensitize.svg', import.meta.url).href,
    title: '智能脱敏处理',
    description: '对敏感信息进行智能脱敏，保护隐私安全。'
  },
  {
    icon: new URL('../assets/risk_assess.svg', import.meta.url).href,
    title: '风险评估与建议',
    description: '多维度评估数据合规风险，输出专业建议。'
  }
];

const reasons = [
  {
    title: 'AI驱动',
    description: '融合大模型与知识库，合规更智能。'
  },
  {
    title: '极致体验',
    description: '极简交互，秒级响应，支持多端访问。'
  },
  {
    title: '安全可信',
    description: '全流程留痕，数据不出本地，合规可追溯。'
  }
];

onMounted(() => {
  isVisible.value = true;
  setupScrollAnimations();
});

const setupScrollAnimations = () => {
  const animateOnScroll = () => {
    document.querySelectorAll('.feature-card, .reason-card').forEach((card) => {
      const rect = card.getBoundingClientRect();
      const isVisible = rect.top <= window.innerHeight * 0.85;
      if (isVisible) {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }
    });
  };

  window.addEventListener('scroll', animateOnScroll);
  animateOnScroll(); // Initial check
};

onUnmounted(() => {
  window.removeEventListener('scroll', setupScrollAnimations);
});
</script>

<style scoped>
.animate-float {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.feature-card, .reason-card {
  opacity: 0;
  transform: translateY(50px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-up-1 { transition-delay: 0.2s; }
.fade-up-2 { transition-delay: 0.4s; }
.fade-up-3 { transition-delay: 0.6s; }

/* Smooth scrolling for anchor links */
html {
  scroll-behavior: smooth;
}
</style>
