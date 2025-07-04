import { createRouter, createWebHistory } from 'vue-router';
import PiiDetect from './views/PiiDetect.vue';

const routes = [
  { path: '/', name: 'PiiDetect', component: PiiDetect },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
