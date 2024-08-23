import { createRouter, createWebHistory } from 'vue-router';
import StartPage from '@/components/StartPage.vue';
// Add other components as needed

const routes = [
  {
    path: '/',
    name: 'StartPage',
    component: StartPage
  },
  // Add more routes here
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

