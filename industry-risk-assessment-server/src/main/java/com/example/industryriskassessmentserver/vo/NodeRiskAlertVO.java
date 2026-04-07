package com.example.industryriskassessmentserver.vo;

import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Data
public class NodeRiskAlertVO {
    private String companyName;
    private String period;
    private String alertLevel;
    private List<KeyFactor> keyFactors = new ArrayList<>();
    private List<String> suggestions = new ArrayList<>();
    private String generatedAt;
    private String modelName;
    private String remark;

    @Data
    public static class KeyFactor {
        private String name;
        private Double value;
        private String impact;
    }
}
