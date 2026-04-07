package com.example.industryriskassessmentserver.enums;

import lombok.Getter;

@Getter
public enum Quarter {
    Q1("Q1", "第一季度"),
    Q2("Q2", "第二季度"),
    Q3("Q3", "第三季度"),
    Q4("Q4", "第四季度");
    
    private final String code;
    private final String name;
    
    Quarter(String code, String name) {
        this.code = code;
        this.name = name;
    }
    
    public static Quarter fromCode(String code) {
        for (Quarter quarter : values()) {
            if (quarter.getCode().equals(code)) {
                return quarter;
            }
        }
        throw new IllegalArgumentException("Invalid quarter code: " + code);
    }
} 