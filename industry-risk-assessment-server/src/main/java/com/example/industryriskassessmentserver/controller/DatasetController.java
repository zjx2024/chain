package com.example.industryriskassessmentserver.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.industryriskassessmentserver.common.Result;
import com.example.industryriskassessmentserver.dto.DatasetQueryDTO;
import com.example.industryriskassessmentserver.dto.DatasetUploadDTO;
import com.example.industryriskassessmentserver.entity.Dataset;
import com.example.industryriskassessmentserver.entity.DictDatasetType;
import com.example.industryriskassessmentserver.entity.IndustryChain;
import com.example.industryriskassessmentserver.service.DatasetService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/dataset")
public class DatasetController {
    private static final Logger log = LoggerFactory.getLogger(DatasetController.class);
    
    @Autowired
    private DatasetService datasetService;
    
    @GetMapping("/list")
    public Result<Page<Dataset>> listDatasets(DatasetQueryDTO queryDTO) {
        try {
            log.info("查询数据集列表: {}", queryDTO);
            Page<Dataset> page = datasetService.listDatasets(queryDTO);
            log.info("查询数据集列表成功: total={}", page.getTotal());
            return Result.success(page);
        } catch (Exception e) {
            log.error("查询数据集列表失败", e);
            throw e;
        }
    }
    
    @GetMapping("/{id}")
    public Result<Dataset> getDataset(@PathVariable Long id) {
        Dataset dataset = datasetService.getDatasetById(id);
        return Result.success(dataset);
    }
    
    @PostMapping("/upload")
    public Result<Void> uploadDataset(
            @Valid DatasetUploadDTO uploadDTO,
            @RequestParam("file") MultipartFile file) {
        datasetService.uploadDataset(uploadDTO, file);
        return Result.success(null);
    }
    
    @GetMapping("/types")
    public Result<List<DictDatasetType>> getDatasetTypes() {
        List<DictDatasetType> types = datasetService.getDatasetTypes();
        return Result.success(types);
    }
    
    @GetMapping("/industry-chains")
    public Result<List<IndustryChain>> getIndustryChains() {
        List<IndustryChain> chains = datasetService.getIndustryChains();
        return Result.success(chains);
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteDataset(@PathVariable Long id) {
        try {
            log.info("删除数据集: id={}", id);
            datasetService.deleteDataset(id);
            log.info("删除数据集成功");
            return Result.success(null);
        } catch (Exception e) {
            log.error("删除数据集失败", e);
            throw e;
        }
    }

    @PutMapping("/{id}")
    public Result<Void> updateDataset(@PathVariable Long id, @RequestBody @Valid Dataset dataset) {
        try {
            log.info("更新数据集: id={}, dataset={}", id, dataset);
            dataset.setId(id);
            datasetService.updateDataset(dataset);
            log.info("更新数据集成功");
            return Result.success(null);
        } catch (Exception e) {
            log.error("更新数据集失败", e);
            throw e;
        }
    }

    @GetMapping("/periods/{industryChainId}")
    public Result<List<String>> getDataPeriods(@PathVariable Long industryChainId) {
        return Result.success(datasetService.getDataPeriodsByIndustryChain(industryChainId));
    }
} 