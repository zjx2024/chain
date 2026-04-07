import axios from 'axios'
import type { AxiosInstance } from 'axios'
import { ElMessage } from 'element-plus'
import { BusinessError, ErrorCode } from '@/types/error'

const service: AxiosInstance = axios.create({
  baseURL: '',  // 使用空字符串，让vite代理处理路径
  timeout: 300000
})

// 请求拦截器
service.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
)

service.interceptors.response.use(
  (response) => {
    // 对于blob类型的响应，直接返回response
    if (response.config.responseType === 'blob') {
      return response
    }
    
    const res = response.data
    if (res.code !== ErrorCode.SUCCESS) {
      switch (res.code) {
        case ErrorCode.UNAUTHORIZED:
        case ErrorCode.TOKEN_EXPIRED:
        case ErrorCode.TOKEN_INVALID:
          ElMessage.warning(res.message || '当前接口未开放访问')
          break
        case ErrorCode.FORBIDDEN:
          ElMessage.error(res.message || '当前接口不允许访问')
          break
        case ErrorCode.REQUEST_FREQUENT:
          ElMessage.warning('请求过于频繁，请稍后再试')
          break
        case ErrorCode.PASSWORD_ERROR:
          ElMessage.error('密码错误')
          break
        default:
          ElMessage.error(res.message || '请求错误')
      }
      return Promise.reject(new BusinessError(res.code, res.message))
    }
    return res
  },
  (error) => {
    // 对于blob类型的请求，不显示错误消息
    if (error.config?.responseType === 'blob') {
      return Promise.reject(error)
    }
    
    if (error.response) {
      switch (error.response.status) {
        case 401:
          ElMessage.warning('当前接口未开放访问')
          break
        case 403:
          ElMessage.error('当前接口不允许访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器错误，请稍后重试')
          break
        default:
          ElMessage.error('网络错误，请稍后重试')
      }
    } else if (error.request) {
      ElMessage.error('网络连接失败，请检查网络')
    } else {
      ElMessage.error('请求配置错误')
    }
    return Promise.reject(error)
  }
)

export default service
