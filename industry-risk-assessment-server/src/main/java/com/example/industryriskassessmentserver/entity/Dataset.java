package com.example.industryriskassessmentserver.entity;

import com.baomidou.mybatisplus.annotation.*;
import com.example.industryriskassessmentserver.validation.DataPeriod;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("dataset")
public class Dataset {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String name;
    
    @TableField("type_code")
    private String typeCode;  // 保持使用 type_code
    
    private Long industryChainId;
    
    @DataPeriod
    private String dataPeriod;
    
    private String filePath;
    
    private Long fileSize;
    
    private Integer deleted;  // 是否删除：0-未删除，1-已删除
    
    private LocalDateTime createTime;
    
    private LocalDateTime updateTime;
    
    private Long createBy;
    
    // 关联字段，不在数据库表中
    @TableField(exist = false)
    private String typeName;
    
    @TableField(exist = false)
    private String industryChainName;
} 