package com.example.industryriskassessmentserver.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.example.industryriskassessmentserver.entity.TrainedModel;
import java.util.List;

public interface TrainedModelService extends IService<TrainedModel> {
    
    /**
     * 创建训练后模型记录
     */
    TrainedModel createTrainedModel(TrainedModel trainedModel);
    
    /**
     * 根据训练任务ID查询训练后模型
     */
    TrainedModel getByTrainingTaskId(Long trainingTaskId);
    
    /**
     * 根据模型名称查询训练后模型
     */
    TrainedModel getByTrainedModelName(String trainedModelName);
    
    /**
     * 获取所有可用的训练后模型
     */
    List<TrainedModel> getActiveModels();
    
    /**
     * 分页获取可用的训练后模型
     */
    IPage<TrainedModel> getActiveModelsPage(Page<TrainedModel> page, String keyword);
    
    /**
     * 归档模型
     */
    boolean archiveModel(Long id);
    
    /**
     * 删除模型
     */
    boolean deleteModel(Long id);
    
    /**
     * 生成训练后模型名称
     */
    String generateTrainedModelName(String originalModelName, String logFileName);
    
    /**
     * 生成模型保存路径
     */
    String generateModelSavePath(String originalModelName, String logFileName);
    
    /**
     * 获取基础模型存储路径
     */
    String getBaseModelStoragePath();
    
    /**
     * 修复缺失的训练模型记录
     */
    int fixMissingTrainedModelRecords();
} 