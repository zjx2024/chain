package com.example.industryriskassessmentserver.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("task_type_model")
public class TaskTypeModel {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private Long taskTypeId;
    
    private Long modelId;
    
    private LocalDateTime createTime;
    
    // 关联字段，不在数据库表中
    @TableField(exist = false)
    private String taskTypeName;
    
    @TableField(exist = false)
    private String modelName;
} 