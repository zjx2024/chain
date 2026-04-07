package com.example.industryriskassessmentserver.service;

import com.example.industryriskassessmentserver.dto.graph.GraphData;
import com.example.industryriskassessmentserver.dto.risk.RiskOverview;

public interface RiskStatusService {
    GraphData getIndustryChainGraph(Long industryChainId);
    
    /**
     * 获取产业链风险概览数据
     * @param industryChainId 产业链ID
     * @param dataPeriod 数据期间
     * @return 风险概览数据
     */
    RiskOverview getRiskOverview(Long industryChainId, String dataPeriod);
} 