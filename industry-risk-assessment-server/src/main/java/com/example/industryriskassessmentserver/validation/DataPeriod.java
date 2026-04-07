package com.example.industryriskassessmentserver.validation;

import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.*;

@Documented
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = DataPeriodValidator.class)
public @interface DataPeriod {
    String message() default "数据期间格式不正确，正确格式为：2024Q1";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
} 