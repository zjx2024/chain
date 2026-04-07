package com.example.industryriskassessmentserver.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.industryriskassessmentserver.dto.ModelTrainingRequest;
import com.example.industryriskassessmentserver.entity.*;
import com.example.industryriskassessmentserver.mapper.TrainingTaskMapper;
import com.example.industryriskassessmentserver.service.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class TrainingTaskServiceImpl extends ServiceImpl<TrainingTaskMapper, TrainingTask> implements TrainingTaskService {
    
    private static final Logger log = LoggerFactory.getLogger(TrainingTaskServiceImpl.class);
    
    @Autowired
    private DatasetService datasetService;
    
    @Autowired
    private ModelTrainingService modelTrainingService;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Override
    public TrainingTask createTrainingTask(ModelTrainingRequest request) {
        try {
            // 获取相关信息
            Dataset dataset = datasetService.getDatasetById(request.getDatasetId());
            DictModel model = modelTrainingService.getModelById(request.getModelId());
            List<ModelOptimizer> optimizers = modelTrainingService.getOptimizersByModelId(request.getModelId());
            ModelOptimizer optimizer = optimizers.stream()
                .filter(opt -> opt.getOptimizerId().equals(request.getOptimizerId()))
                .findFirst()
                .orElseThrow(() -> new RuntimeException("优化器不存在"));
            
            String modelDisplayName = resolveModelDisplayName(model);
            
            // 构建任务名称
            String taskName = String.format("%s_%s_%d_%s_%.4f", 
                modelDisplayName, 
                dataset.getName(), 
                request.getEpochs(),
                optimizer.getOptimizerName(),
                request.getLearningRate() != null ? request.getLearningRate() : optimizer.getDefaultLr().doubleValue()
            );
            
            // 构建训练参数JSON
            Map<String, Object> trainingParams = new HashMap<>();
            trainingParams.put("clientsSampleRatio", request.getClientsSampleRatio());
            trainingParams.put("topkRatio", request.getTopkRatio());
            trainingParams.put("nClusters", request.getNClusters());
            trainingParams.put("privacyMethod", request.getPrivacyMethod());
            trainingParams.put("dp", request.getDp());
            
            // 创建训练任务
            TrainingTask task = new TrainingTask();
            task.setTaskName(taskName);
            task.setDatasetId(request.getDatasetId());
            task.setDatasetName(dataset.getName());
            task.setDataPeriod(request.getDataPeriod());
            task.setTaskTypeId(request.getTaskTypeId());
            task.setTaskTypeName("训练任务"); // 可以从task type表获取
            task.setModelId(request.getModelId());
            task.setModelName(modelDisplayName);
            task.setOptimizerId(request.getOptimizerId());
            task.setOptimizerName(optimizer.getOptimizerName());
            task.setLearningRate(request.getLearningRate() != null ? 
                BigDecimal.valueOf(request.getLearningRate()) : optimizer.getDefaultLr());
            task.setTotalEpochs(request.getEpochs());
            task.setCurrentEpoch(0);
            task.setStatus(TrainingTask.Status.PENDING);
            task.setTrainingParams(objectMapper.writeValueAsString(trainingParams));
            
            // 保存到数据库
            save(task);
            
            log.info("创建训练任务成功: {}", task.getTaskName());
            return task;
            
        } catch (Exception e) {
            log.error("创建训练任务失败", e);
            throw new RuntimeException("创建训练任务失败: " + e.getMessage());
        }
    }
    
    @Override
    public void startTrainingTask(Long taskId) {
        TrainingTask task = getById(taskId);
        if (task == null) {
            throw new RuntimeException("训练任务不存在");
        }
        
        task.setStatus(TrainingTask.Status.RUNNING);
        task.setStartTime(LocalDateTime.now());
        updateById(task);
        
        log.info("启动训练任务: {}", task.getTaskName());
    }
    
    @Override
    public List<TrainingTask> getRunningTasks() {
        return baseMapper.getRunningTasks();
    }
    
    @Override
    public List<TrainingTask> getRecentTasks(int limit) {
        return baseMapper.getRecentTasks(limit);
    }
    
    @Override
    public void updateCurrentEpoch(Long taskId, Integer currentEpoch) {
        baseMapper.updateCurrentEpoch(taskId, currentEpoch);
    }
    
    @Override
    public void completeTask(Long taskId) {
        TrainingTask task = getById(taskId);
        if (task != null) {
            task.setStatus(TrainingTask.Status.COMPLETED);
            task.setEndTime(LocalDateTime.now());
            task.setCurrentEpoch(task.getTotalEpochs()); // 设置为总轮次
            updateById(task);
            log.info("训练任务完成: {}", task.getTaskName());
        }
    }
    
    @Override
    public void terminateTask(Long taskId) {
        TrainingTask task = getById(taskId);
        if (task != null) {
            task.setStatus(TrainingTask.Status.TERMINATED);
            task.setEndTime(LocalDateTime.now());
            updateById(task);
            log.info("训练任务已终止: {}", task.getTaskName());
        }
    }
    
    @Override
    public void failTask(Long taskId, String errorMessage) {
        TrainingTask task = getById(taskId);
        if (task != null) {
            task.setStatus(TrainingTask.Status.FAILED);
            task.setEndTime(LocalDateTime.now());
            task.setErrorMessage(errorMessage);
            updateById(task);
            log.info("训练任务失败: {}, 错误: {}", task.getTaskName(), errorMessage);
        }
    }

    private String resolveModelDisplayName(DictModel model) {
        if (model != null && StringUtils.hasText(model.getDescription())) {
            return model.getDescription().trim();
        }
        return model != null && StringUtils.hasText(model.getName()) ? model.getName() : "训练模型";
    }
} 
