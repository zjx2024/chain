package com.example.industryriskassessmentserver.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("model_optimizer")
public class ModelOptimizer {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private Long modelId;
    
    private Long optimizerId;
    
    private BigDecimal defaultLr;
    
    private LocalDateTime createTime;
    
    // 关联字段，不在数据库表中
    @TableField(exist = false)
    private String modelName;
    
    @TableField(exist = false)
    private String optimizerName;
} 