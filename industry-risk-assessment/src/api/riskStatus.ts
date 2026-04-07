import request from '@/utils/request'
import type { GraphData } from '@/types/graph'
import type { AxiosRequestConfig } from 'axios'

// 风险概览数据接口
export interface RiskOverview {
  riskCompanyCount: number
  totalCompanyCount: number
  riskCompanies: string[]
  normalCompanies: string[]
  riskLevel: string
  resilienceScore: number
  recoveryScore: number
  integrityScore: number
  nextPeriodLabel: string
  nextPeriodRiskCompanyCount: number
  nextPeriodRiskLevel: string
}

// 获取产业链关系图谱数据
export function getIndustryChainGraph(industryChainId: number, config?: AxiosRequestConfig) {
  return request<GraphData>({
    url: `/api/risk-status/graph/${industryChainId}`,
    method: 'get',
    ...config
  })
}

// 获取产业链风险概览数据
export function getRiskOverview(industryChainId: number, dataPeriod: string, config?: AxiosRequestConfig) {
  return request<RiskOverview>({
    url: `/api/risk-status/overview/${industryChainId}`,
    method: 'get',
    params: { dataPeriod },
    ...config
  })
} 
