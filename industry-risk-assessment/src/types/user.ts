// 用户信息接口
export interface UserInfo {
  id: number
  username: string
  realName?: string
  email?: string
  role?: string
}

// 登录表单接口
export interface LoginForm {
  username: string
  password: string
}

// 登录响应接口
export interface LoginResponse {
  token: string
  userInfo: UserInfo
} 