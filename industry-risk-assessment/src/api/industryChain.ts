import request from '@/utils/request'
import type { IndustryChain } from '@/types/dataset'

// 获取产业链列表
export function getIndustryChainList() {
  return request<IndustryChain[]>({
    url: '/api/industry-chain/list',
    method: 'get'
  })
} 