import { createRouter, createWebHistory } from 'vue-router';

import Home from './views/Home.vue';
import PiiDetect from './views/PiiDetect.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/pii', name: 'PiiDetect', component: PiiDetect },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
