package com.example.industryriskassessmentserver.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("training_task")
public class TrainingTask {
    
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("task_name")
    private String taskName;
    
    @TableField("dataset_id")
    private Long datasetId;
    
    @TableField("dataset_name")
    private String datasetName;
    
    @TableField("data_period")
    private String dataPeriod;
    
    @TableField("task_type_id")
    private Long taskTypeId;
    
    @TableField("task_type_name")
    private String taskTypeName;
    
    @TableField("model_id")
    private Long modelId;
    
    @TableField("model_name")
    private String modelName;
    
    @TableField("optimizer_id")
    private Long optimizerId;
    
    @TableField("optimizer_name")
    private String optimizerName;
    
    @TableField("learning_rate")
    private BigDecimal learningRate;
    
    @TableField("total_epochs")
    private Integer totalEpochs;
    
    @TableField("current_epoch")
    private Integer currentEpoch;
    
    @TableField("status")
    private String status;
    
    @TableField("start_time")
    private LocalDateTime startTime;
    
    @TableField("end_time")
    private LocalDateTime endTime;
    
    @TableField("process_id")
    private String processId;
    
    @TableField("error_message")
    private String errorMessage;
    
    @TableField("training_params")
    private String trainingParams;
    
    @TableField("trained_model_id")
    private Long trainedModelId;
    
    @TableField("trained_model_name")
    private String trainedModelName;
    
    @TableField(value = "create_time", fill = FieldFill.INSERT)
    private LocalDateTime createTime;
    
    @TableField(value = "update_time", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
    
    // 训练状态枚举
    public static class Status {
        public static final String PENDING = "PENDING";     // 待启动
        public static final String RUNNING = "RUNNING";     // 训练中
        public static final String COMPLETED = "COMPLETED"; // 已完成
        public static final String TERMINATED = "TERMINATED"; // 已终止
        public static final String FAILED = "FAILED";       // 失败
    }
} 