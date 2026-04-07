package com.example.industryriskassessmentserver.service;

import com.example.industryriskassessmentserver.dto.risk.NextPeriodRiskSummary;
import com.example.industryriskassessmentserver.vo.NodeRiskAlertVO;
import com.example.industryriskassessmentserver.vo.NodeRiskStatusVO;
import java.util.List;

public interface NodeRiskService {
    /**
     * 获取指定产业链的公司名称列表
     */
    List<String> listCompanyNames(Long industryChainId);

    /**
     * 根据产业链、期间、公司名称获取节点风险状态
     */
    NodeRiskStatusVO getNodeRiskStatus(Long industryChainId, String dataPeriod, String companyName);

    /**
     * 获取节点风险告警信息
     */
    NodeRiskAlertVO getNodeRiskAlert(Long industryChainId, String dataPeriod, String companyName);

    /**
     * 统计下一期间（T+1）风险企业数量
     */
    NextPeriodRiskSummary getNextPeriodSummary(Long industryChainId, String dataPeriod);
}
