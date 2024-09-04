import { createRouter, createWebHistory } from 'vue-router';
import StartPage from '@/components/StartPage.vue';
import Dashboard from '@/components/DashboardPage.vue';

const routes = [
  {
    path: '/',
    name: 'StartPage',
    component: StartPage
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

