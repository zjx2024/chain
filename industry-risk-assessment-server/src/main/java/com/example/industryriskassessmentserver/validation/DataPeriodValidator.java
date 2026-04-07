package com.example.industryriskassessmentserver.validation;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import java.util.regex.Pattern;

public class DataPeriodValidator implements ConstraintValidator<DataPeriod, String> {
    private static final Pattern PATTERN = Pattern.compile("^\\d{4}Q[1-4]$");
    
    @Override
    public void initialize(DataPeriod constraintAnnotation) {
        // 初始化验证器
    }
    
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null || value.isEmpty()) {
            return true;  // 允许空值
        }
        return PATTERN.matcher(value).matches();
    }
} 