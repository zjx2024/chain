package com.example.industryriskassessmentserver.dto;

import lombok.Data;

@Data
public class DatasetQueryDTO {
    private Integer pageNum = 1;
    private Integer pageSize = 10;
    private String name;        // 数据集名称（模糊查询）
    private String typeCode;    // 数据集类型编码
    private Long industryChainId;  // 产业链ID
} 