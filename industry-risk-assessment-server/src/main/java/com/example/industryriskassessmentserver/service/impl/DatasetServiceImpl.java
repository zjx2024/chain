package com.example.industryriskassessmentserver.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.industryriskassessmentserver.common.ErrorCode;
import com.example.industryriskassessmentserver.config.FileUploadConfig;
import com.example.industryriskassessmentserver.dto.DatasetQueryDTO;
import com.example.industryriskassessmentserver.dto.DatasetUploadDTO;
import com.example.industryriskassessmentserver.entity.Dataset;
import com.example.industryriskassessmentserver.entity.DictDatasetType;
import com.example.industryriskassessmentserver.entity.IndustryChain;
import com.example.industryriskassessmentserver.exception.BusinessException;
import com.example.industryriskassessmentserver.mapper.DatasetMapper;
import com.example.industryriskassessmentserver.mapper.DictDatasetTypeMapper;
import com.example.industryriskassessmentserver.mapper.IndustryChainMapper;
import com.example.industryriskassessmentserver.service.DatasetService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.UUID;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.Comparator;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
public class DatasetServiceImpl implements DatasetService {
    
    @Autowired
    private DatasetMapper datasetMapper;
    
    @Autowired
    private FileUploadConfig fileUploadConfig;
    
    @Autowired
    private DictDatasetTypeMapper dictDatasetTypeMapper;
    
    @Autowired
    private IndustryChainMapper industryChainMapper;
    
    @Override
    public Page<Dataset> listDatasets(DatasetQueryDTO queryDTO) {
        Page<Dataset> page = new Page<>(queryDTO.getPageNum(), queryDTO.getPageSize());
        // 使用自定义的分页查询方法
        return datasetMapper.selectDatasetPage(page, queryDTO);
    }
    
    @Override
    public Dataset getDatasetById(Long id) {
        return datasetMapper.selectById(id);
    }
    
    @Override
    public void createDataset(Dataset dataset) {
        // 如果需要，在这里添加数据期间的格式转换逻辑
        datasetMapper.insert(dataset);
    }
    
    @Override
    public void updateDataset(Dataset dataset) {
        datasetMapper.updateById(dataset);
    }
    
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteDataset(Long id) {
        // 1. 获取数据集信息
        Dataset dataset = datasetMapper.selectById(id);
        if (dataset == null) {
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "数据集不存在");
        }

        // 2. 删除本地文件
        if (StringUtils.hasText(dataset.getFilePath())) {
            String fullPath = fileUploadConfig.getBasePath() + "/" + dataset.getFilePath();
            File file = new File(fullPath);
            if (file.exists() && file.isFile()) {
                if (!file.delete()) {
                    log.warn("文件删除失败: {}", fullPath);
                }
            }
        }

        // 3. 逻辑删除数据库记录
        datasetMapper.deleteById(id);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void uploadDataset(DatasetUploadDTO uploadDTO, MultipartFile file) {
        // 1. 验证文件
        if (file == null || file.isEmpty()) {
            throw new BusinessException(ErrorCode.PARAM_ERROR.getCode(), "请选择要上传的文件");
        }
        
        // 2. 验证文件大小
        if (file.getSize() > fileUploadConfig.getMaxSize()) {
            throw new BusinessException(ErrorCode.PARAM_ERROR.getCode(), 
                String.format("文件大小超过限制：%dMB", fileUploadConfig.getMaxSize() / 1024 / 1024));
        }
        
        // 3. 验证文件类型
        String originalFilename = file.getOriginalFilename();
        if (!isValidDatasetFile(originalFilename)) {
            throw new BusinessException(ErrorCode.PARAM_ERROR.getCode(), "只支持数据集文件格式（.xls, .xlsx, .dat）");
        }
        
        try {
            // 4. 保存文件
            String fileName = generateFileName(originalFilename);
            String filePath = saveFile(file, fileName);
            
            // 5. 保存数据集信息
            Dataset dataset = new Dataset();
            dataset.setName(uploadDTO.getName());
            dataset.setTypeCode(uploadDTO.getTypeCode());
            dataset.setIndustryChainId(uploadDTO.getIndustryChainId());
            dataset.setDataPeriod(uploadDTO.getDataPeriod());
            dataset.setFilePath(filePath);
            dataset.setFileSize(file.getSize());
            dataset.setCreateTime(LocalDateTime.now());
            dataset.setUpdateTime(LocalDateTime.now());
            dataset.setCreateBy(1L);  // TODO: 从登录用户中获取
            dataset.setDeleted(0);
            
            datasetMapper.insert(dataset);
            
        } catch (IOException e) {
            throw new BusinessException(ErrorCode.INTERNAL_ERROR.getCode(), "文件上传失败：" + e.getMessage());
        }
    }
    
    // 验证是否为有效的数据集文件
    private boolean isValidDatasetFile(String filename) {
        if (filename == null) return false;
        return filename.endsWith(".xlsx") || filename.endsWith(".xls") || filename.endsWith(".dat");
    }
    
    // 生成文件名
    private String generateFileName(String originalFilename) {
        String extension = originalFilename.substring(originalFilename.lastIndexOf("."));
        return UUID.randomUUID().toString() + extension;
    }
    
    // 保存文件
    private String saveFile(MultipartFile file, String fileName) throws IOException {
        String datePath = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyy/MM/dd"));
        String uploadPath = fileUploadConfig.getBasePath() + "/" + datePath;
        
        File dir = new File(uploadPath);
        if (!dir.exists()) {
            dir.mkdirs();
        }
        
        String filePath = uploadPath + "/" + fileName;
        File dest = new File(filePath);
        file.transferTo(dest);
        
        return datePath + "/" + fileName;
    }

    @Override
    public List<DictDatasetType> getDatasetTypes() {
        return dictDatasetTypeMapper.selectList(null);
    }
    
    @Override
    public List<IndustryChain> getIndustryChains() {
        return industryChainMapper.selectList(null);
    }

    @Override
    public List<String> getDataPeriodsByIndustryChain(Long industryChainId) {
        return datasetMapper.selectList(
            new LambdaQueryWrapper<Dataset>()
                .eq(Dataset::getIndustryChainId, industryChainId)
                .select(Dataset::getDataPeriod)
        ).stream()
        .map(Dataset::getDataPeriod)
        .distinct()
        .sorted(Comparator.reverseOrder())  // 降序排序
        .collect(Collectors.toList());
    }

    @Override
    public String getLatestRelationDataset(Long industryChainId) {
        Dataset dataset = datasetMapper.selectOne(
            new LambdaQueryWrapper<Dataset>()
                .eq(Dataset::getIndustryChainId, industryChainId)
                .eq(Dataset::getTypeCode, "INDUSTRY_RELATION")
                .eq(Dataset::getDeleted, 0)
                .orderByDesc(Dataset::getCreateTime)
                .last("LIMIT 1")
        );
        
        if (dataset == null) {
            log.warn("未找到产业链[{}]的关系数据", industryChainId);
            throw new BusinessException(404, "请先上传该产业链的关系数据文件");
        }
        
        // 获取完整的文件路径
        String fullPath = fileUploadConfig.getBasePath() + "/" + dataset.getFilePath();
        log.info("准备读取文件: {}", fullPath);
        
        // 验证文件是否存在
        File file = new File(fullPath);
        if (!file.exists() || !file.isFile()) {
            log.error("文件不存在: {}", fullPath);
            throw new BusinessException(404, "关系数据文件已丢失，请重新上传");
        }
        
        return dataset.getFilePath();
    }
} 