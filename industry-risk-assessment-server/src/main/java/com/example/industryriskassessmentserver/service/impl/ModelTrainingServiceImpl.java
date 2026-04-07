package com.example.industryriskassessmentserver.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.example.industryriskassessmentserver.entity.DictTaskType;
import com.example.industryriskassessmentserver.entity.DictModel;
import com.example.industryriskassessmentserver.entity.ModelOptimizer;
import com.example.industryriskassessmentserver.mapper.DictTaskTypeMapper;
import com.example.industryriskassessmentserver.mapper.DictModelMapper;
import com.example.industryriskassessmentserver.mapper.DictOptimizerMapper;
import com.example.industryriskassessmentserver.service.ModelTrainingService;
import com.example.industryriskassessmentserver.config.ModelStorageConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import java.util.List;
import java.io.File;

@Service
public class ModelTrainingServiceImpl implements ModelTrainingService {
    
    @Autowired
    private DictTaskTypeMapper dictTaskTypeMapper;
    
    @Autowired
    private DictModelMapper dictModelMapper;
    
    @Autowired
    private DictOptimizerMapper dictOptimizerMapper;
    
    @Autowired
    private ModelStorageConfig modelStorageConfig;
    
    @Override
    public List<DictTaskType> getAllTaskTypes() {
        return dictTaskTypeMapper.selectList(null);
    }

    @Override
    public DictTaskType getTaskTypeById(Long taskTypeId) {
        if (taskTypeId == null) {
            return null;
        }
        return dictTaskTypeMapper.selectById(taskTypeId);
    }
    
    @Override
    public List<DictModel> getModelsByTaskTypeId(Long taskTypeId) {
        return dictModelMapper.getModelsByTaskTypeId(taskTypeId);
    }
    
    @Override
    public List<ModelOptimizer> getOptimizersByModelId(Long modelId) {
        return dictOptimizerMapper.getOptimizersByModelId(modelId);
    }
    
    @Override
    public void updateModelPath(Long modelId, String modelPath) {
        DictModel model = new DictModel();
        model.setId(modelId);
        model.setModelPath(modelPath);
        dictModelMapper.updateById(model);
    }
    
    @Override
    public DictModel getModelById(Long modelId) {
        return dictModelMapper.selectById(modelId);
    }

    @Override
    public DictModel getModelByName(String modelName) {
        if (!StringUtils.hasText(modelName)) {
            return null;
        }
        LambdaQueryWrapper<DictModel> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(DictModel::getName, modelName).last("LIMIT 1");
        return dictModelMapper.selectOne(wrapper);
    }
    
    @Override
    public boolean checkModelFileExists(Long modelId) {
        DictModel model = dictModelMapper.selectById(modelId);
        if (model == null || !StringUtils.hasText(model.getModelPath())) {
            return false;
        }
        
        String fullPath = modelStorageConfig.getModelFullPath(model.getModelPath());
        File modelFile = new File(fullPath);
        
        // 如果是目录路径，检查目录是否存在
        if (model.getModelPath().endsWith("/")) {
            return modelFile.exists() && modelFile.isDirectory();
        }
        // 如果是文件路径，检查文件是否存在
        else {
            return modelFile.exists() && modelFile.isFile();
        }
    }
    
    @Override
    public String getModelFullPath(Long modelId) {
        DictModel model = dictModelMapper.selectById(modelId);
        if (model == null || !StringUtils.hasText(model.getModelPath())) {
            return null;
        }
        
        return modelStorageConfig.getModelFullPath(model.getModelPath());
    }
} 
