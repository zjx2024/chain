import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/risk/status',
      component: () => import('@/views/home/index.vue'),
      children: [
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
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/risk/status'
    }
  ]
})

export default router
