package com.example.industryriskassessmentserver.controller;

import com.example.industryriskassessmentserver.common.Result;
import com.example.industryriskassessmentserver.dto.graph.GraphData;
import com.example.industryriskassessmentserver.dto.risk.RiskOverview;
import com.example.industryriskassessmentserver.service.RiskStatusService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/risk-status")
public class RiskStatusController {
    @Autowired
    private RiskStatusService riskStatusService;
    
    @GetMapping("/graph/{industryChainId}")
    public Result<GraphData> getIndustryChainGraph(@PathVariable Long industryChainId) {
        return Result.success(riskStatusService.getIndustryChainGraph(industryChainId));
    }
    
    /**
     * 获取产业链风险概览数据
     * @param industryChainId 产业链ID
     * @param dataPeriod 数据期间
     * @return 风险概览数据
     */
    @GetMapping("/overview/{industryChainId}")
    public Result<RiskOverview> getRiskOverview(
            @PathVariable Long industryChainId,
            @RequestParam String dataPeriod) {
        return Result.success(riskStatusService.getRiskOverview(industryChainId, dataPeriod));
    }
} 