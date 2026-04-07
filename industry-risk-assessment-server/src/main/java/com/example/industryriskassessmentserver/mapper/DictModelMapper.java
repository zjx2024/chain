package com.example.industryriskassessmentserver.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.industryriskassessmentserver.entity.DictModel;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import java.util.List;

@Mapper
public interface DictModelMapper extends BaseMapper<DictModel> {
    
    /**
     * 根据任务类型ID获取可用模型列表
     */
    List<DictModel> getModelsByTaskTypeId(@Param("taskTypeId") Long taskTypeId);
} 