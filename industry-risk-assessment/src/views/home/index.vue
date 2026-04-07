<template>
  <div class="layout-container">
    <!-- 左侧导航栏 -->
    <el-menu
      class="sidebar-menu"
      :default-active="route.path"
      router
      :collapse="false"
    >
      <el-menu-item index="/dashboard">
        <el-icon><Odometer /></el-icon>
        <template #title>总览</template>
      </el-menu-item>

      <el-sub-menu index="/data">
        <template #title>
          <el-icon><DataLine /></el-icon>
          <span>数据中心</span>
        </template>
        <el-menu-item index="/data/edit">数据编辑</el-menu-item>
        <el-menu-item index="/data/upload">数据上传</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="/risk">
        <template #title>
          <el-icon><Warning /></el-icon>
          <span>产业链风险评估</span>
        </template>
        <el-menu-item index="/risk/status">产业链状态</el-menu-item>
        <el-menu-item index="/risk/node">节点风险状态</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="/models">
        <template #title>
          <el-icon><Box /></el-icon>
          <span>模型仓库</span>
        </template>
        <el-sub-menu index="/models/integrity">
          <template #title>完整性评估</template>
          <el-menu-item index="/models/integrity/model1">模型一：LPME</el-menu-item>
          <el-menu-item index="/models/integrity/model2">模型二：LPAPE</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="/models/risk-assessment">
          <template #title>风险评估</template>
          <el-menu-item index="/models/risk-assessment/model1">模型一：GANS</el-menu-item>
          <el-menu-item index="/models/risk-assessment/model2">模型二：HKTGNN</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="/models/risk-warning">
          <template #title>风险预警</template>
          <el-menu-item index="/models/risk-warning/model1">模型一：PCA-CNN</el-menu-item>
          <el-menu-item index="/models/risk-warning/model2">模型二：HiGNN</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/models/training">模型训练</el-menu-item>
        <el-menu-item index="/models/management">模型管理</el-menu-item>
      </el-sub-menu>
    </el-menu>

    <!-- 右侧内容区 -->
    <div class="content-container">

      <!-- 主要内容区 -->
      <div class="main-content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import {
  Odometer,
  DataLine,
  Warning,
  Box
} from '@element-plus/icons-vue'

const route = useRoute()
</script>

<style scoped lang="scss">
.layout-container {
  height: 100vh;
  display: flex;

  .sidebar-menu {
    height: 100%;
    border-right: 1px solid #e6e6e6;
    flex-shrink: 0;
    background-color: #fff;
    position: relative;
    z-index: 1;
    
    // 展开时的宽度
    &:not(.el-menu--collapse) {
      width: 240px;
    }
    
    // 折叠时的宽度
    &.el-menu--collapse {
      width: 64px;
    }
    
    // 确保过渡效果平滑
    transition: width 0.3s;
  }

  .content-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    background-color: #f5f7f9;

    .header {
      height: 60px;
      border-bottom: 1px solid #e6e6e6;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;

      .header-left {
        display: flex;
        align-items: center;
        gap: 20px;

        .collapse-btn {
          font-size: 20px;
          cursor: pointer;
          &:hover {
            color: #409eff;
          }
        }
      }

      .header-right {
        .user-info {
          display: flex;
          align-items: center;
          gap: 4px;
          cursor: pointer;
          
          &:hover {
            color: #409eff;
          }
        }
      }
    }

    .main-content {
      flex: 1;
      padding: 20px;
      overflow: auto;
    }
  }
}
</style> 
