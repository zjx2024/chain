import request from '@/utils/request'
import type { NodeRiskAlert, NodeRiskDetail } from '@/types/risk'

export function getNodeRiskCompanies(industryChainId: number) {
  return request<string[]>({
    url: '/api/node-risk/companies',
    method: 'get',
    params: { industryChainId }
  })
}

export function getNodeRiskStatus(params: {
  industryChainId: number
  dataPeriod: string
  companyName: string
}) {
  return request<NodeRiskDetail>({
    url: '/api/node-risk/status',
    method: 'get',
    params
  })
}

export function getNodeRiskAlert(params: {
  industryChainId: number
  dataPeriod: string
  companyName: string
}) {
  return request<NodeRiskAlert>({
    url: '/api/node-risk/alerts',
    method: 'get',
    params
  })
}
