package com.example.industryriskassessmentserver.controller;

import com.example.industryriskassessmentserver.common.Result;
import com.example.industryriskassessmentserver.dto.ModelTrainingRequest;
import com.example.industryriskassessmentserver.entity.DictTaskType;
import com.example.industryriskassessmentserver.entity.DictModel;
import com.example.industryriskassessmentserver.entity.ModelOptimizer;
import com.example.industryriskassessmentserver.entity.TrainingTask;
import com.example.industryriskassessmentserver.service.ModelTrainingService;
import com.example.industryriskassessmentserver.service.ModelTrainingExecutionService;
import com.example.industryriskassessmentserver.service.TrainingTaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;
import java.util.List;
import java.util.concurrent.CompletableFuture;

@RestController
@RequestMapping("/api/model-training")
public class ModelTrainingController {
    
    @Autowired
    private ModelTrainingService modelTrainingService;
    
    @Autowired
    private ModelTrainingExecutionService modelTrainingExecutionService;
    
    @Autowired
    private TrainingTaskService trainingTaskService;
    
    /**
     * 获取所有任务类型
     */
    @GetMapping("/task-types")
    public Result<List<DictTaskType>> getAllTaskTypes() {
        List<DictTaskType> taskTypes = modelTrainingService.getAllTaskTypes();
        return Result.success(taskTypes);
    }
    
    /**
     * 根据任务类型ID获取可用模型列表
     */
    @GetMapping("/models/{taskTypeId}")
    public Result<List<DictModel>> getModelsByTaskTypeId(@PathVariable Long taskTypeId) {
        List<DictModel> models = modelTrainingService.getModelsByTaskTypeId(taskTypeId);
        return Result.success(models);
    }
    
    /**
     * 根据模型ID获取可用优化器列表（带默认学习率）
     */
    @GetMapping("/optimizers/{modelId}")
    public Result<List<ModelOptimizer>> getOptimizersByModelId(@PathVariable Long modelId) {
        List<ModelOptimizer> optimizers = modelTrainingService.getOptimizersByModelId(modelId);
        return Result.success(optimizers);
    }
    
    /**
     * 获取模型详情
     */
    @GetMapping("/model/{modelId}")
    public Result<DictModel> getModelById(@PathVariable Long modelId) {
        DictModel model = modelTrainingService.getModelById(modelId);
        return Result.success(model);
    }
    
    /**
     * 更新模型文件路径
     */
    @PutMapping("/model/{modelId}/path")
    public Result<Void> updateModelPath(@PathVariable Long modelId, @RequestBody String modelPath) {
        modelTrainingService.updateModelPath(modelId, modelPath);
        return Result.success(null);
    }
    
    /**
     * 检查模型文件是否存在
     */
    @GetMapping("/model/{modelId}/exists")
    public Result<Boolean> checkModelFileExists(@PathVariable Long modelId) {
        boolean exists = modelTrainingService.checkModelFileExists(modelId);
        return Result.success(exists);
    }
    
    /**
     * 获取模型的完整文件系统路径
     */
    @GetMapping("/model/{modelId}/fullpath")
    public Result<String> getModelFullPath(@PathVariable Long modelId) {
        String fullPath = modelTrainingService.getModelFullPath(modelId);
        return Result.success(fullPath);
    }
    
    /**
     * 启动模型训练
     */
    @PostMapping("/start")
    public Result<TrainingTask> startTraining(@Valid @RequestBody ModelTrainingRequest request) {
        try {
            // 异步启动训练
            CompletableFuture<TrainingTask> future = modelTrainingExecutionService.startTraining(request);
            TrainingTask task = future.get(); // 等待训练启动完成
            
            return Result.success(task);
        } catch (Exception e) {
            return Result.error(500, "模型训练启动失败: " + e.getMessage());
        }
    }
    

    
    /**
     * 获取正在运行的训练任务列表
     */
    @GetMapping("/tasks/running")
    public Result<List<TrainingTask>> getRunningTasks() {
        List<TrainingTask> tasks = trainingTaskService.getRunningTasks();
        return Result.success(tasks);
    }
    
    /**
     * 获取最近的训练任务列表
     */
    @GetMapping("/tasks/recent")
    public Result<List<TrainingTask>> getRecentTasks(@RequestParam(defaultValue = "10") int limit) {
        List<TrainingTask> tasks = trainingTaskService.getRecentTasks(limit);
        return Result.success(tasks);
    }
    
    /**
     * 终止训练任务
     */
    @PostMapping("/tasks/{taskId}/terminate")
    public Result<String> terminateTask(@PathVariable Long taskId) {
        try {
            trainingTaskService.terminateTask(taskId);
            return Result.success("训练任务已终止");
        } catch (Exception e) {
            return Result.error(500, "终止训练任务失败: " + e.getMessage());
        }
    }
} 