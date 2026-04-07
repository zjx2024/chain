package com.example.industryriskassessmentserver.dto;

import lombok.Data;

@Data
public class ModelTestRequest {
    
    /**
     * 训练后模型ID
     */
    private Long trainedModelId;
    
    /**
     * 训练后模型名称
     */
    private String trainedModelName;
    
    /**
     * 测试数据集ID
     */
    private Long testDatasetId;
    
    /**
     * 测试数据集路径（可选，如果指定则优先使用）
     */
    private String testDatasetPath;
    
    /**
     * 测试批次大小
     */
    private Integer testBatchSize = 256;
    
    /**
     * 计算设备 (cuda/cpu)
     */
    private String device = "cuda";
    
    /**
     * 是否保存测试结果到文件
     */
    private Boolean saveResults = true;
    
    /**
     * 测试结果输出路径（可选）
     */
    private String outputPath;
} 