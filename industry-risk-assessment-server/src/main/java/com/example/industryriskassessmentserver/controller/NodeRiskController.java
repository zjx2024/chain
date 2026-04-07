package com.example.industryriskassessmentserver.controller;

import com.example.industryriskassessmentserver.common.Result;
import com.example.industryriskassessmentserver.service.NodeRiskService;
import com.example.industryriskassessmentserver.vo.NodeRiskStatusVO;
import com.example.industryriskassessmentserver.vo.NodeRiskAlertVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/node-risk")
public class NodeRiskController {
    @Autowired
    private NodeRiskService nodeRiskService;

    @GetMapping("/companies")
    public Result<List<String>> getCompanyNames(@RequestParam Long industryChainId) {
        return Result.success(nodeRiskService.listCompanyNames(industryChainId));
    }

    @GetMapping("/status")
    public Result<NodeRiskStatusVO> getNodeRiskStatus(@RequestParam Long industryChainId,
                                                      @RequestParam String dataPeriod,
                                                      @RequestParam String companyName) {
        return Result.success(nodeRiskService.getNodeRiskStatus(industryChainId, dataPeriod, companyName));
    }

    @GetMapping("/alerts")
    public Result<NodeRiskAlertVO> getNodeRiskAlert(@RequestParam Long industryChainId,
                                                    @RequestParam String dataPeriod,
                                                    @RequestParam String companyName) {
        return Result.success(nodeRiskService.getNodeRiskAlert(industryChainId, dataPeriod, companyName));
    }
}
