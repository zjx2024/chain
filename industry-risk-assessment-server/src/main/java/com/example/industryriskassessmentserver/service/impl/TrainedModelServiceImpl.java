package com.example.industryriskassessmentserver.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.industryriskassessmentserver.entity.TrainedModel;
import com.example.industryriskassessmentserver.entity.TrainingTask;
import com.example.industryriskassessmentserver.entity.DictModel;
import com.example.industryriskassessmentserver.mapper.TrainedModelMapper;
import com.example.industryriskassessmentserver.service.TrainedModelService;
import com.example.industryriskassessmentserver.service.TrainingTaskService;
import com.example.industryriskassessmentserver.service.ModelTrainingService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.io.File;
import java.util.List;

@Slf4j
@Service
public class TrainedModelServiceImpl extends ServiceImpl<TrainedModelMapper, TrainedModel> 
        implements TrainedModelService {
    
    @Value("${model.storage.base-path:${CHAIN_MODELS_PATH:${CHAIN_BASE_PATH:/data/chain}/models-storage}}")
    private String modelStorageBasePath;
    
    @Autowired
    private TrainingTaskService trainingTaskService;
    
    @Autowired
    private ModelTrainingService modelTrainingService;
    
    @Override
    public TrainedModel createTrainedModel(TrainedModel trainedModel) {
        // 不再自动创建目录 - Python已经创建了实际的模型目录
        // ensureDirectoryExists(trainedModel.getModelSavePath());
        
        // 设置默认状态
        if (trainedModel.getStatus() == null) {
            trainedModel.setStatus(TrainedModel.Status.ACTIVE);
        }
        
        // 保存到数据库
        this.save(trainedModel);
        log.info("创建训练后模型记录: {}", trainedModel.getTrainedModelName());
        
        return trainedModel;
    }
    
    @Override
    public TrainedModel getByTrainingTaskId(Long trainingTaskId) {
        QueryWrapper<TrainedModel> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("training_task_id", trainingTaskId);
        return this.getOne(queryWrapper);
    }
    
    @Override
    public TrainedModel getByTrainedModelName(String trainedModelName) {
        QueryWrapper<TrainedModel> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("trained_model_name", trainedModelName);
        return this.getOne(queryWrapper);
    }
    
    @Override
    public List<TrainedModel> getActiveModels() {
        QueryWrapper<TrainedModel> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("status", TrainedModel.Status.ACTIVE)
                   .orderByDesc("create_time");
        return this.list(queryWrapper);
    }
    
    @Override
    public IPage<TrainedModel> getActiveModelsPage(Page<TrainedModel> page, String keyword) {
        QueryWrapper<TrainedModel> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("status", TrainedModel.Status.ACTIVE);
        
        // 如果有关键词，进行模糊查询
        if (StringUtils.hasText(keyword)) {
            queryWrapper.and(wrapper -> wrapper
                .like("trained_model_name", keyword)
                .or()
                .like("original_model_name", keyword)
                .or()
                .like("dataset_name", keyword)
                .or()
                .like("optimizer_name", keyword)
            );
        }
        
        queryWrapper.orderByDesc("create_time");
        return this.page(page, queryWrapper);
    }
    
    @Override
    public boolean archiveModel(Long id) {
        TrainedModel model = this.getById(id);
        if (model != null) {
            model.setStatus(TrainedModel.Status.ARCHIVED);
            return this.updateById(model);
        }
        return false;
    }
    
    @Override
    public boolean deleteModel(Long id) {
        TrainedModel model = this.getById(id);
        if (model != null) {
            model.setStatus(TrainedModel.Status.DELETED);
            return this.updateById(model);
        }
        return false;
    }
    
    @Override
    public String generateTrainedModelName(String originalModelName, String logFileName) {
        String prefix = resolveDisplayPrefix(originalModelName);
        String suffix = sanitizeSuffix(logFileName);
        if (!StringUtils.hasText(suffix)) {
            return prefix;
        }
        return prefix + "_" + suffix;
    }
    
    @Override
    public String generateModelSavePath(String originalModelName, String logFileName) {
        // 移除日志文件的扩展名
        String logFileNameWithoutExt = logFileName.replaceAll("\\.(txt|log)$", "");
        
        // 构建完整路径
        String fullPath = modelStorageBasePath + File.separator + originalModelName + File.separator + logFileNameWithoutExt;
        
        // 添加调试日志
        log.info("generateModelSavePath - 基础路径: {}", modelStorageBasePath);
        log.info("generateModelSavePath - 原始模型名: {}", originalModelName);
        log.info("generateModelSavePath - 日志文件名（去扩展名）: {}", logFileNameWithoutExt);
        log.info("generateModelSavePath - 完整路径: {}", fullPath);
        
        return fullPath;
    }
    
    /**
     * 获取基础模型存储路径
     */
    public String getBaseModelStoragePath() {
        return modelStorageBasePath;
    }

    private String resolveDisplayPrefix(String originalModelName) {
        DictModel dictModel = modelTrainingService.getModelByName(originalModelName);
        if (dictModel != null && StringUtils.hasText(dictModel.getDescription())) {
            return dictModel.getDescription().trim();
        }
        return originalModelName;
    }

    private String sanitizeSuffix(String logFileName) {
        if (!StringUtils.hasText(logFileName)) {
            return "";
        }
        String sanitized = logFileName.replaceAll("\\.(txt|log)$", "");
        return sanitized.replaceAll("[\\\\/]+", "_");
    }
    
    @Override
    public int fixMissingTrainedModelRecords() {
        log.info("开始修复缺失的训练模型记录");
        
        // 查找已完成但没有trained_model_name的训练任务
        QueryWrapper<TrainingTask> taskQuery = new QueryWrapper<>();
        taskQuery.eq("status", TrainingTask.Status.COMPLETED)
                .isNull("trained_model_name");
        
        List<TrainingTask> missingTasks = trainingTaskService.list(taskQuery);
        log.info("找到 {} 个需要修复的训练任务", missingTasks.size());
        
        int fixedCount = 0;
        
        for (TrainingTask task : missingTasks) {
            try {
                // 获取模型信息
                DictModel model = modelTrainingService.getModelById(task.getModelId());
                if (model == null) {
                    log.warn("跳过任务 {}: 找不到模型信息", task.getId());
                    continue;
                }
                
                // 生成日志文件名和模型名称
                String logFileName = generateLogFileNameForTask(task);
                String trainedModelName = generateTrainedModelName(model.getName(), logFileName);
                
                // 检查是否已经存在相同名称的记录
                TrainedModel existing = getByTrainedModelName(trainedModelName);
                if (existing != null) {
                    log.warn("跳过任务 {}: 已存在同名模型记录", task.getId());
                    continue;
                }
                
                // 创建训练后模型记录
                TrainedModel trainedModel = new TrainedModel();
                trainedModel.setTrainedModelName(trainedModelName);
                trainedModel.setOriginalModelId(model.getId());
                trainedModel.setOriginalModelName(model.getName());
                trainedModel.setTrainingTaskId(task.getId());
                trainedModel.setModelSavePath(generateModelSavePath(model.getName(), logFileName));
                trainedModel.setLogFileName(logFileName);
                trainedModel.setTrainingEpochs(task.getTotalEpochs());
                trainedModel.setLearningRate(task.getLearningRate());
                trainedModel.setDatasetName(task.getDatasetName());
                trainedModel.setOptimizerName(task.getOptimizerName());
                trainedModel.setStatus(TrainedModel.Status.ACTIVE);
                trainedModel.setBestEpoch(task.getTotalEpochs());
                
                // 保存记录
                TrainedModel savedModel = createTrainedModel(trainedModel);
                
                // 更新训练任务
                task.setTrainedModelName(trainedModelName);
                task.setTrainedModelId(savedModel.getId());
                trainingTaskService.updateById(task);
                
                fixedCount++;
                log.info("已修复任务 {}: 创建模型记录 {}", task.getId(), trainedModelName);
                
            } catch (Exception e) {
                log.error("修复任务 {} 失败", task.getId(), e);
            }
        }
        
        log.info("修复完成，共修复 {} 个记录", fixedCount);
        return fixedCount;
    }
    
    /**
     * 为训练任务生成日志文件名
     */
    private String generateLogFileNameForTask(TrainingTask task) {
        String timestamp = java.time.LocalDateTime.now()
            .format(java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd_HH-mm"));
        
        String datasetBaseName = task.getDatasetName();
        if (datasetBaseName.contains("_")) {
            datasetBaseName = datasetBaseName.substring(0, datasetBaseName.lastIndexOf("_"));
        }
        
        return String.format("%s_task_%d_fixed_%s.txt",
            datasetBaseName,
            task.getId(),
            timestamp
        );
    }
    
    /**
     * 确保目录存在
     */
    private void ensureDirectoryExists(String path) {
        try {
            File directory = new File(path);
            if (!directory.exists()) {
                boolean created = directory.mkdirs();
                if (created) {
                    log.info("创建模型存储目录: {}", path);
                } else {
                    log.warn("创建模型存储目录失败: {}", path);
                }
            }
        } catch (Exception e) {
            log.error("创建模型存储目录异常: {}", path, e);
        }
    }
} 
