<template>
  <div class="login-container">
    <!-- 左侧装饰区域 -->
    <div class="login-left">
      <div class="left-content">
        <h2>产业链风险评估分析系统</h2>
        <p>Industry Risk Assessment System</p>
      </div>
    </div>

    <!-- 右侧登录表单区域 -->
    <div class="login-right">
      <div class="login-form">
        <h2>欢迎登录</h2>
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          size="large"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              show-password
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              :loading="loading"
              class="login-button"
              @click="handleLogin"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import { useUserStore } from '@/store/user'
import type { LoginForm } from '@/types/user'
import { BusinessError } from '@/types/error'

const router = useRouter()
const userStore = useUserStore()
const loginFormRef = ref<FormInstance | null>(null)

// 登录表单数据
const loginForm = reactive<LoginForm>({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在 3 到 20 个字符之间', trigger: 'blur' },
    { 
      validator: (_rule: any, value: string, callback: Function) => {
        if (value && /[<>]/.test(value)) {
          callback(new Error('用户名包含非法字符'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在 6 到 20 个字符之间', trigger: 'blur' },
    {
      validator: (_rule: any, value: string, callback: Function) => {
        if (value && !/^[a-zA-Z0-9_]+$/.test(value)) {
          callback(new Error('密码只能包含字母、数字和下划线'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 加载状态
const loading = ref(false)

// 登录处理
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    loading.value = true
    await loginFormRef.value.validate()
    await userStore.login(loginForm.username, loginForm.password)
    ElMessage.success('登录成功')
    router.push('/')  // 登录成功后跳转到首页
  } catch (error) {
    console.error('登录失败:', error)
    if (error instanceof BusinessError) {
      ElMessage.error(error.message)
    } else {
      ElMessage.error('登录失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  position: fixed;  // 使用fixed定位
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  overflow: hidden;

  .login-left {
    flex: 1.2;  // 左侧占比稍大
    background: linear-gradient(135deg, #1890ff, #1d39c4);
    display: flex;
    align-items: center;
    justify-content: center;
    
    .left-content {
      color: white;
      text-align: center;
      padding: 0 20px; // 添加一些内边距
      
      h2 {
        font-size: 2.5rem; // 使用相对单位
        margin-bottom: 20px;
        font-weight: 600;
      }
      
      p {
        font-size: 1.2rem;
        opacity: 0.8;
      }
    }
  }

  .login-right {
    flex: 0.8;  // 右侧占比稍小
    background-color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;

    .login-form {
      width: min(400px, 90%); // 响应式宽度
      max-width: 100%;
      
      h2 {
        text-align: center;
        margin-bottom: 40px;
        color: #333;
        font-size: 1.8rem;
        font-weight: 500;
      }

      :deep(.el-input) {
        .el-input__wrapper {
          padding-left: 11px;
          box-shadow: 0 0 0 1px #dcdfe6 inset;
          
          &:hover {
            box-shadow: 0 0 0 1px #c0c4cc inset;
          }
          
          &.is-focus {
            box-shadow: 0 0 0 1px #409eff inset;
          }
          
          .el-input__prefix {
            font-size: 16px;
            color: #909399;
          }
        }
      }

      .login-button {
        width: 100%;
        height: 40px;
        font-size: 16px;
        border-radius: 4px;
        margin-top: 10px;
      }
    }
  }
}

// 响应式设计
@media screen and (max-width: 768px) {
  .login-container {
    flex-direction: column;
    
    .login-left {
      flex: none;
      height: 30vh;
      
      .left-content {
        h2 {
          font-size: 2rem;
        }
        
        p {
          font-size: 1rem;
        }
      }
    }
    
    .login-right {
      flex: none;
      height: 70vh;
      padding: 20px;
    }
  }
}
</style>
