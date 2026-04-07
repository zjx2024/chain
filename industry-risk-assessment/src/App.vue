<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

onMounted(async () => {
  // 如果有token但没有用户信息，才需要重新获取
  if (userStore.token && !userStore.userInfo) {
    try {
      await userStore.initUserInfo()
    } catch (error) {
      console.error('获取用户信息失败:', error)
      userStore.logout()
      router.push('/login')
    }
  }
})
</script>

<template>
  <router-view></router-view>
</template>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

#app {
  height: 100%;
}
</style>
