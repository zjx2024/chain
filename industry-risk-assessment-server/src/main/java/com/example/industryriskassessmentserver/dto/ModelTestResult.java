package com.example.industryriskassessmentserver.dto;

import lombok.Data;
import java.time.LocalDateTime;
import java.util.Map;

@Data
public class ModelTestResult {
    
    /**
     * 测试时间
     */
    private LocalDateTime testTime;
    
    /**
     * 训练后模型名称
     */
    private String trainedModelName;
    
    /**
     * 测试数据集名称
     */
    private String testDatasetName;
    
    /**
     * HR@10指标
     */
    private Double hr10;
    
    /**
     * NDCG@10指标
     */
    private Double ndcg10;
    
    /**
     * 测试损失
     */
    private Double testLoss;
    
    /**
     * 与训练时最佳性能的对比
     */
    private PerformanceComparison performanceComparison;
    
    /**
     * 测试结果文件路径
     */
    private String resultFilePath;
    
    /**
     * 测试状态 (SUCCESS/FAILED)
     */
    private String status;
    
    /**
     * 错误信息（如果测试失败）
     */
    private String errorMessage;
    
    /**
     * 额外的测试信息
     */
    private Map<String, Object> additionalInfo;
    
    @Data
    public static class PerformanceComparison {
        /**
         * HR@10相对变化百分比
         */
        private Double hrRelativeChange;
        
        /**
         * NDCG@10相对变化百分比
         */
        private Double ndcgRelativeChange;
        
        /**
         * HR@10绝对差值
         */
        private Double hrDifference;
        
        /**
         * NDCG@10绝对差值
         */
        private Double ndcgDifference;
        
        /**
         * 训练时最佳HR@10
         */
        private Double trainingBestHr;
        
        /**
         * 训练时最佳NDCG@10
         */
        private Double trainingBestNdcg;
    }
} 