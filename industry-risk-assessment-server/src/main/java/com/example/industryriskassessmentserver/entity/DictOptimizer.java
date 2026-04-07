package com.example.industryriskassessmentserver.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("dict_optimizer")
public class DictOptimizer {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String code;
    
    private String name;
    
    private String description;
    
    private BigDecimal defaultLr;
    
    private LocalDateTime createTime;
    
    private LocalDateTime updateTime;
} 