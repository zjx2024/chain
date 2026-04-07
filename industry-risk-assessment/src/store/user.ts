import { defineStore } from 'pinia'
import type { UserInfo } from '@/types/user'
import { BusinessError, ErrorCode } from '@/types/error'
import { login, getUserInfo } from '@/api/user'

const TOKEN_EXPIRES_AT_KEY = 'tokenExpiresAt'

function getTokenExpireTime(token: string): number | null {
  try {
    const parts = token.split('.')
    if (parts.length < 2) {
      return null
    }
    const payload = JSON.parse(atob(parts[1]))
    if (!payload.exp) {
      return null
    }
    return payload.exp * 1000
  } catch (error) {
    console.error('解析token失败', error)
    return null
  }
}

interface UserState {
  token: string
  userInfo: UserInfo | null
  tokenExpiresAt: number | null
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || 'null'),
    tokenExpiresAt: (() => {
      const stored = localStorage.getItem(TOKEN_EXPIRES_AT_KEY)
      return stored ? Number(stored) : null
    })()
  }),

  getters: {
    // Token 是否有效
    hasValidToken(): boolean {
      return !!this.token && !!this.tokenExpiresAt && Date.now() < this.tokenExpiresAt
    },
    // 是否已登录
    isLogin(): boolean {
      return this.hasValidToken && !!this.userInfo
    },
    // 获取用户角色
    userRole(): string | undefined {
      return this.userInfo?.role
    },
    // 判断是否有某个角色
    hasRole(): (role: string) => boolean {
      return (role: string) => this.userInfo?.role === role
    }
  },

  actions: {
    // 设置 Token
    setToken(token: string) {
      try {
        const expiresAt = getTokenExpireTime(token)
        if (!expiresAt) {
          throw new BusinessError(ErrorCode.TOKEN_INVALID, '无法解析token')
        }
        this.token = token
        this.tokenExpiresAt = expiresAt
        localStorage.setItem('token', token)
        localStorage.setItem(TOKEN_EXPIRES_AT_KEY, expiresAt.toString())
      } catch (error) {
        console.error('Token存储失败:', error)
        throw new BusinessError(ErrorCode.INTERNAL_ERROR, 'Token存储失败')
      }
    },

    // 设置用户信息
    setUserInfo(userInfo: UserInfo) {
      this.userInfo = userInfo
      // 保存到localStorage
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    },

    // 登录
    async login(username: string, password: string) {
      try {
        const { data } = await login({ username, password })
        this.setToken(data.token)
        this.setUserInfo(data.userInfo)
        return data
      } catch (error) {
        this.logout()  // 登录失败时清除状态
        return Promise.reject(error)
      }
    },

    // 登出
    logout() {
      this.token = ''
      this.userInfo = null
      this.tokenExpiresAt = null
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      localStorage.removeItem(TOKEN_EXPIRES_AT_KEY)
    },

    // 判断token是否过期
    isTokenExpired(): boolean {
      if (!this.token || !this.tokenExpiresAt) {
        return true
      }
      return Date.now() >= this.tokenExpiresAt
    },

    // 获取用户信息
    async getUserInfo() {
      try {
        // TODO: 调用获取用户信息 API
        // const { data } = await getUserInfoApi()
        // this.setUserInfo(data)
        return Promise.resolve(this.userInfo)
      } catch (error) {
        return Promise.reject(error)
      }
    },

    // 初始化用户信息
    async initUserInfo() {
      if (this.token && !this.userInfo) {
        if (this.isTokenExpired()) {
          this.logout()
          return
        }
        try {
          const { data } = await getUserInfo()
          this.setUserInfo(data)
        } catch (error) {
          this.logout()
          throw error
        }
      }
    }
  }
}) 
