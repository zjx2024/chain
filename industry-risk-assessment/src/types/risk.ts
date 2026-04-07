export interface RiskFactor {
  index: number
  name: string
  value: number | null
}

export type RiskAlertLevel = 'LOW' | 'MEDIUM' | 'HIGH'

export interface RiskAlertKeyFactor {
  name: string
  value: number | null
  impact: string
}

export interface NodeRiskAlert {
  companyName: string
  period: string
  alertLevel: RiskAlertLevel
  keyFactors: RiskAlertKeyFactor[]
  suggestions: string[]
  generatedAt: string
  modelName?: string
  remark?: string
}

export interface NodeRiskDetail {
  companyName: string
  dataPeriod: string
  currentRisk: boolean
  nextPeriod: string
  nextPeriodRisk: boolean
  currentFactors: RiskFactor[]
  nextPeriodFactors: RiskFactor[]
}
