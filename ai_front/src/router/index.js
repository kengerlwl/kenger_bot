import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/User/login.vue'
import Register from '@/components/User/Register.vue'
import ChatContainer from '@/components/Chat/ChatContainer.vue'

// 定义路由
const routes = [
  {
    path: '/',
    component: ChatContainer,
    meta: { requiresAuth: true }  // 需要登录才能访问
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/register',
    component: Register
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：检查是否登录，未登录则跳转到登录页面
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')  // 从localStorage读取token
  if (to.meta.requiresAuth && !token) {
    next('/login')  // 未登录，跳转到登录页面
    // next()
  } else {
    next()  // 否则继续访问
  }
})

export default router