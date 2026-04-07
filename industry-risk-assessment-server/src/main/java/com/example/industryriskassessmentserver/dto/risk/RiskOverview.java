package com.example.industryriskassessmentserver.dto.risk;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 风险概览数据传输对象
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RiskOverview {
    /**
     * 风险企业数量
     */
    private int riskCompanyCount;
    
    /**
     * 总企业数量
     */
    private int totalCompanyCount;
    
    /**
     * 风险企业列表
     */
    private java.util.List<String> riskCompanies;
    
    /**
     * 正常企业列表
     */
    private java.util.List<String> normalCompanies;

    /**
     * 风险等级（低风险/中风险/高风险/待评估）
     */
    private String riskLevel;

    /**
     * 产业链抵抗力得分
     */
    private double resilienceScore;

    /**
     * 产业链恢复力得分
     */
    private double recoveryScore;

    /**
     * 产业链完整性得分
     */
    private double integrityScore;

    /**
     * 完整性等级（完整/不完整）
     */
    private String integrityLevel;

    /**
     * 下一期标识（例如 T+1期 或 实际期数）
     */
    private String nextPeriodLabel;

    /**
     * 下一期风险企业数量
     */
    private int nextPeriodRiskCompanyCount;

    /**
     * 下一期风险等级
     */
    private String nextPeriodRiskLevel;

}
