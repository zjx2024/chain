package com.example.industryriskassessmentserver.dto;

import com.example.industryriskassessmentserver.validation.DataPeriod;
import lombok.Data;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Data
public class DatasetUploadDTO {
    @NotBlank(message = "数据集名称不能为空")
    private String name;
    
    @NotBlank(message = "数据集类型不能为空")
    private String typeCode;
    
    @NotNull(message = "产业链不能为空")
    private Long industryChainId;
    
    @DataPeriod
    private String dataPeriod;
} 