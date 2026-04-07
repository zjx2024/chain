package com.example.industryriskassessmentserver.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.industryriskassessmentserver.entity.DictOptimizer;
import com.example.industryriskassessmentserver.entity.ModelOptimizer;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import java.util.List;

@Mapper
public interface DictOptimizerMapper extends BaseMapper<DictOptimizer> {
    
    /**
     * 根据模型ID获取可用优化器列表（带默认学习率）
     */
    List<ModelOptimizer> getOptimizersByModelId(@Param("modelId") Long modelId);
} 