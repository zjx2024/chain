package com.example.industryriskassessmentserver.dto.risk;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class NextPeriodRiskSummary {
    private String nextPeriodLabel;
    private int riskCompanyCount;
    private int totalCompanyCount;
}
