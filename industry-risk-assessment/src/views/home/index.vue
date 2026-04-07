<template>
  <div class="layout-container">
    <el-menu
      class="sidebar-menu"
      :default-active="route.path"
      router
      :collapse="false"
    >
      <div class="brand-block">
        <div class="brand-title">产业链风险评估</div>
      </div>

      <el-menu-item index="/risk/status">
        <el-icon><DataAnalysis /></el-icon>
        <template #title>产业链状态</template>
      </el-menu-item>

      <el-menu-item index="/risk/node">
        <el-icon><Warning /></el-icon>
        <template #title>节点风险状态</template>
      </el-menu-item>
    </el-menu>

    <div class="content-container">
      <div class="content-header">
        <div class="content-title">
          {{ route.path === '/risk/node' ? '节点风险状态' : '产业链状态' }}
        </div>
      </div>

      <div class="main-content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { DataAnalysis, Warning } from '@element-plus/icons-vue'

const route = useRoute()
</script>

<style scoped lang="scss">
.layout-container {
  min-height: 100vh;
  display: flex;
  background:
    radial-gradient(circle at top left, rgba(41, 128, 185, 0.18), transparent 30%),
    linear-gradient(135deg, #f4f7fb 0%, #eef3f8 100%);

  .sidebar-menu {
    height: 100vh;
    width: 240px;
    flex-shrink: 0;
    border-right: 1px solid rgba(15, 23, 42, 0.08);
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(12px);
    padding-top: 24px;

    :deep(.el-menu-item) {
      margin: 8px 12px;
      border-radius: 12px;
    }

    :deep(.el-menu-item.is-active) {
      background: #dceeff;
      color: #0f5ba7;
    }

    .brand-block {
      padding: 0 20px 20px;

      .brand-title {
        font-size: 18px;
        font-weight: 700;
        color: #10233f;
      }
    }
  }

  .content-container {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;

    .content-header {
      padding: 32px 32px 0;

      .content-title {
        font-size: 28px;
        font-weight: 700;
        color: #10233f;
      }
    }

    .main-content {
      flex: 1;
      padding: 24px 32px 32px;
      overflow: auto;
    }
  }
}

@media (max-width: 960px) {
  .layout-container {
    flex-direction: column;

    .sidebar-menu {
      width: 100%;
      height: auto;
      padding-top: 16px;
      border-right: none;
      border-bottom: 1px solid rgba(15, 23, 42, 0.08);
    }

    .content-container {
      .content-header {
        padding: 24px 20px 0;
      }

      .main-content {
        padding: 20px;
      }
    }
  }
}
</style>
