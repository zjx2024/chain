package com.example.industryriskassessmentserver.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.industryriskassessmentserver.entity.TrainingTask;
import com.example.industryriskassessmentserver.dto.ModelTrainingRequest;

import java.util.List;

public interface TrainingTaskService extends IService<TrainingTask> {
    
    /**
     * 创建训练任务
     */
    TrainingTask createTrainingTask(ModelTrainingRequest request);
    
    /**
     * 启动训练任务
     */
    void startTrainingTask(Long taskId);
    
    /**
     * 获取正在运行的训练任务列表
     */
    List<TrainingTask> getRunningTasks();
    
    /**
     * 获取最近的训练任务列表
     */
    List<TrainingTask> getRecentTasks(int limit);
    
    /**
     * 更新训练任务的当前轮次
     */
    void updateCurrentEpoch(Long taskId, Integer currentEpoch);
    
    /**
     * 完成训练任务
     */
    void completeTask(Long taskId);
    
    /**
     * 终止训练任务
     */
    void terminateTask(Long taskId);
    
    /**
     * 标记任务失败
     */
    void failTask(Long taskId, String errorMessage);
} 