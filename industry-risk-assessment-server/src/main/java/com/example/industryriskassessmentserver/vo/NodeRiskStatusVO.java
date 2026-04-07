package com.example.industryriskassessmentserver.vo;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.util.List;

@Data
public class NodeRiskStatusVO {
    private String companyName;
    private String dataPeriod;
    private boolean currentRisk;
    private String nextPeriod;
    private boolean nextPeriodRisk;
    private List<RiskFactorVO> currentFactors;
    private List<RiskFactorVO> nextPeriodFactors;

    /**
     * 用于内部调用的真实下一期标签，不对外返回
     */
    @JsonIgnore
    private String actualNextPeriod;
}
