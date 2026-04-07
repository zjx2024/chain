package com.example.industryriskassessmentserver.entity;

import com.baomidou.mybatisplus.annotation.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("trained_model")
public class TrainedModel {
    
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("trained_model_name")
    private String trainedModelName;
    
    @JsonIgnore
    @TableField("original_model_id")
    private Long originalModelId;
    
    @JsonIgnore
    @TableField("original_model_name")
    private String originalModelName;
    
    @TableField("training_task_id")
    private Long trainingTaskId;
    
    @TableField("model_save_path")
    private String modelSavePath;
    
    @TableField("log_file_name")
    private String logFileName;
    
    @TableField("training_epochs")
    private Integer trainingEpochs;
    
    @TableField("learning_rate")
    private BigDecimal learningRate;
    
    @TableField("best_epoch")
    private Integer bestEpoch;
    
    @TableField("model_size")
    private Long modelSize;
    
    @TableField("training_duration")
    private Integer trainingDuration;
    
    @TableField("dataset_name")
    private String datasetName;
    
    @TableField("optimizer_name")
    private String optimizerName;
    
    @TableField("status")
    private String status;
    
    @TableField("description")
    private String description;
    
    @TableField(value = "create_time", fill = FieldFill.INSERT)
    private LocalDateTime createTime;
    
    @TableField(value = "update_time", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;

    @TableField(exist = false)
    private Long taskTypeId;

    @TableField(exist = false)
    private String taskTypeCode;

    @TableField(exist = false)
    private String taskTypeName;
    
    // 模型状态枚举
    public static class Status {
        public static final String ACTIVE = "ACTIVE";       // 可用
        public static final String ARCHIVED = "ARCHIVED";   // 已归档
        public static final String DELETED = "DELETED";     // 已删除
    }
} 
