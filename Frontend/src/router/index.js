import { createRouter, createWebHistory } from 'vue-router'
import StartPage from '@/components/StartPage.vue'
import Dashboard from '@/components/DashboardPage.vue'
import ForgotPassword from '@/components/ForgotPassword.vue'
import ResetPassword from '@/components/ResetPassword.vue'
import HomePage from '@/components/HomePage.vue'
import AboutPage from '@/components/AboutPage.vue'
import ForecastPage from '@/components/ForecastPage.vue'
import ProfilePage from '@/components/ProfilePage.vue'

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
  },
  {
    path: '/home',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/about',
    name: 'About',
    component: AboutPage
  },
  {
    path: '/forecast',
    name: 'Forecast',
    component: ForecastPage
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword
  },
  {
    path: '/reset-password/:uidb64/:token',
    name: 'ResetPassword',
    component: ResetPassword,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
