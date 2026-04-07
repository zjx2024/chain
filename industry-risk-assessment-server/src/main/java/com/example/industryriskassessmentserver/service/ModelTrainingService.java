package com.example.industryriskassessmentserver.service;

import com.example.industryriskassessmentserver.entity.DictTaskType;
import com.example.industryriskassessmentserver.entity.DictModel;
import com.example.industryriskassessmentserver.entity.ModelOptimizer;
import java.util.List;

public interface ModelTrainingService {
    
    /**
     * 获取所有任务类型
     */
    List<DictTaskType> getAllTaskTypes();

    /**
     * 根据任务类型ID获取任务类型
     */
    DictTaskType getTaskTypeById(Long taskTypeId);
    
    /**
     * 根据任务类型ID获取可用模型列表
     */
    List<DictModel> getModelsByTaskTypeId(Long taskTypeId);
    
    /**
     * 根据模型ID获取可用优化器列表（带默认学习率）
     */
    List<ModelOptimizer> getOptimizersByModelId(Long modelId);
    
    /**
     * 更新模型文件路径
     */
    void updateModelPath(Long modelId, String modelPath);
    
    /**
     * 根据模型ID获取模型详情
     */
    DictModel getModelById(Long modelId);

    /**
     * 根据模型名称获取模型详情
     */
    DictModel getModelByName(String modelName);
    
    /**
     * 检查模型文件是否存在
     */
    boolean checkModelFileExists(Long modelId);
    
    /**
     * 获取模型的完整文件系统路径
     */
    String getModelFullPath(Long modelId);
} 
