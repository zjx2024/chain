package com.example.industryriskassessmentserver.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.industryriskassessmentserver.dto.DatasetQueryDTO;
import com.example.industryriskassessmentserver.dto.DatasetUploadDTO;
import com.example.industryriskassessmentserver.entity.Dataset;
import com.example.industryriskassessmentserver.entity.DictDatasetType;
import com.example.industryriskassessmentserver.entity.IndustryChain;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

public interface DatasetService {
    // 条件查询数据集列表
    Page<Dataset> listDatasets(DatasetQueryDTO queryDTO);
    
    // 根据ID获取数据集详情
    Dataset getDatasetById(Long id);
    
    // 创建数据集
    void createDataset(Dataset dataset);
    
    // 更新数据集
    void updateDataset(Dataset dataset);
    
    // 删除数据集
    void deleteDataset(Long id);
    
    // 上传数据集
    void uploadDataset(DatasetUploadDTO uploadDTO, MultipartFile file);
    
    // 获取数据集类型列表
    List<DictDatasetType> getDatasetTypes();
    
    // 获取产业链列表
    List<IndustryChain> getIndustryChains();

    List<String> getDataPeriodsByIndustryChain(Long industryChainId);

    /**
     * 获取产业链最新的关系数据文件路径
     */
    String getLatestRelationDataset(Long industryChainId);
} 