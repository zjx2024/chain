package com.example.industryriskassessmentserver.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("industry_chain")
public class IndustryChain {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String code;
    
    private String name;
    
    @TableField("create_time")
    private LocalDateTime createTime;
    
    @TableField("update_time")
    private LocalDateTime updateTime;
} 