package com.example.industryriskassessmentserver.service;

import com.example.industryriskassessmentserver.vo.NodeRiskAlertVO;
import com.example.industryriskassessmentserver.vo.RiskFactorVO;

import java.util.List;

public interface RiskAlertModelService {

    /**
     * 根据 T+1 期风险因子调用大模型生成告警信息
     *
     * @param companyName 公司名
     * @param period      分析期
     * @param hasRisk     是否存在风险标签
     * @param alertLevel  系统已有的风险等级
     * @param factors     T+1 期 18 个风险因素
     * @return 告警结果，若模型不可用则返回兜底结果
     */
    NodeRiskAlertVO analyze(String companyName, String period, boolean hasRisk, String alertLevel, List<RiskFactorVO> factors);
}
