import request from '@/utils/request'
import type { LoginForm } from '@/types/user'

export function login(data: LoginForm) {
  return request({
    url: '/api/user/login',
    method: 'post',
    data
  })
}

export function getUserInfo() {
  return request({
    url: '/api/user/info',
    method: 'get'
  })
} 