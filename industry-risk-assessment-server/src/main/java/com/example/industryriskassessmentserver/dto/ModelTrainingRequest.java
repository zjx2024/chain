package com.example.industryriskassessmentserver.dto;

import lombok.Data;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Min;
import javax.validation.constraints.DecimalMin;

@Data
public class ModelTrainingRequest {
    
    @NotNull(message = "数据集ID不能为空")
    private Long datasetId;
    
    @NotNull(message = "数据期间不能为空")
    private String dataPeriod;
    
    @NotNull(message = "任务类型ID不能为空")
    private Long taskTypeId;
    
    @NotNull(message = "模型ID不能为空")
    private Long modelId;
    
    @NotNull(message = "优化器ID不能为空")
    private Long optimizerId;
    
    @NotNull(message = "训练轮次不能为空")
    @Min(value = 1, message = "训练轮次必须大于0")
    private Integer epochs;
    
    @DecimalMin(value = "0.0", inclusive = false, message = "学习率必须大于0")
    private Double learningRate; // 可选，为空时使用默认学习率
    
    // 可选的高级参数
    private Double clientsSampleRatio = 1.0; // 客户端采样比例
    private Double topkRatio = 0.1; // Top-k压缩比例
    private Integer nClusters = 5; // 聚类数量
    private String privacyMethod = "none"; // 隐私保护方法
    private Double dp = 1e-6; // 差分隐私参数
} 