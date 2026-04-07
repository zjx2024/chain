package com.example.industryriskassessmentserver.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("dict_model")
public class DictModel {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String code;
    
    private String name;
    
    private String description;
    
    private String modelPath;
    
    private LocalDateTime createTime;
    
    private LocalDateTime updateTime;
} 