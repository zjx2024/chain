package com.example.industryriskassessmentserver.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.industryriskassessmentserver.dto.DatasetQueryDTO;
import com.example.industryriskassessmentserver.entity.Dataset;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface DatasetMapper extends BaseMapper<Dataset> {
    // 自定义分页查询方法
    Page<Dataset> selectDatasetPage(Page<Dataset> page, @Param("query") DatasetQueryDTO query);
} 