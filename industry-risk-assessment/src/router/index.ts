import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login/index.vue')
    },
    {
      path: '/',
      redirect: '/dashboard',
      component: () => import('@/views/home/index.vue'),
      children: [
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('@/views/dashboard/index.vue'),
          meta: {
            title: '总览',
            requiresAuth: false
          }
        },
        {
          path: 'data',
          name: 'data',
          meta: {
            title: '数据中心',
            requiresAuth: false
          },
          children: [
            {
              path: 'edit',
              name: 'dataEdit',
              component: () => import('@/views/data/edit.vue'),
              meta: { title: '数据编辑', requiresAuth: false }
            },
            {
              path: 'upload',
              name: 'dataUpload',
              component: () => import('@/views/data/upload.vue'),
              meta: { title: '数据上传', requiresAuth: false }
            }
          ]
        },
        {
          path: 'models',
          name: 'models',
          redirect: '/models/management',
          meta: {
            title: '模型仓库',
            requiresAuth: false
          },
          children: [
            {
              path: 'training',
              name: 'modelTraining',
              component: () => import('@/views/risk/model.vue'),
              meta: { title: '模型训练', requiresAuth: false }
            },
            {
              path: 'management',
              name: 'modelsManagement',
              component: () => import('@/views/models/management.vue'),
              meta: { title: '模型管理', requiresAuth: false }
            },
            {
              path: 'integrity/model1',
              name: 'integrityModel1',
              component: () => import('@/views/models/integrity/model1.vue'),
              meta: { title: '完整性评估 - 模型一', requiresAuth: false }
            },
            {
              path: 'integrity/model2',
              name: 'integrityModel2',
              component: () => import('@/views/models/integrity/model2.vue'),
              meta: { title: '完整性评估 - 模型二', requiresAuth: false }
            },
            {
              path: 'risk-assessment/model1',
              name: 'riskAssessmentModel1',
              component: () => import('@/views/models/risk-assessment/model1.vue'),
              meta: { title: '风险评估 - 模型一', requiresAuth: false }
            },
            {
              path: 'risk-assessment/model2',
              name: 'riskAssessmentModel2',
              component: () => import('@/views/models/risk-assessment/model2.vue'),
              meta: { title: '风险评估 - 模型二', requiresAuth: false }
            },
            {
              path: 'risk-warning/model1',
              name: 'riskWarningModel1',
              component: () => import('@/views/models/risk-warning/model1.vue'),
              meta: { title: '风险预警 - 模型一', requiresAuth: false }
            },
            {
              path: 'risk-warning/model2',
              name: 'riskWarningModel2',
              component: () => import('@/views/models/risk-warning/model2.vue'),
              meta: { title: '风险预警 - 模型二', requiresAuth: false }
            }
          ]
        },
        {
          path: 'risk',
          name: 'risk',
          meta: {
            title: '产业链风险评估',
            requiresAuth: false
          },
          children: [
            {
              path: 'status',
              name: 'riskStatus',
              component: () => import('@/views/risk/status.vue'),
              meta: {
                title: '产业链状态',
                requiresAuth: false
              }
            },
            {
              path: 'node',
              name: 'nodeRiskStatus',
              component: () => import('@/views/risk/node-status.vue'),
              meta: {
                title: '节点风险状态',
                requiresAuth: false
              }
            }
          ]
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()

  const publicPaths = ['/login']

  if (userStore.token && !userStore.hasValidToken) {
    userStore.logout()
    if (!publicPaths.includes(to.path)) {
      next('/login')
      return
    }
  }
  
  // 仅当路由配置 requiresAuth 且不在白名单时才需要校验
  if (to.meta.requiresAuth && !publicPaths.includes(to.path)) {
    if (!userStore.hasValidToken) {
      next('/login')
    } else {
      next()
    }
  } else if (to.path === '/login' && userStore.hasValidToken) {
    next('/risk/status')
  } else {
    next()
  }
})

export default router
