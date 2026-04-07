package com.example.industryriskassessmentserver.service.impl;

import com.example.industryriskassessmentserver.dto.graph.*;
import com.example.industryriskassessmentserver.dto.risk.NextPeriodRiskSummary;
import com.example.industryriskassessmentserver.dto.risk.RiskOverview;
import com.example.industryriskassessmentserver.service.NodeRiskService;
import com.example.industryriskassessmentserver.service.RiskStatusService;
import com.example.industryriskassessmentserver.service.DatasetService;
import com.example.industryriskassessmentserver.utils.ExcelParser;
import com.example.industryriskassessmentserver.config.FileUploadConfig;
import com.example.industryriskassessmentserver.exception.BusinessException;
import com.example.industryriskassessmentserver.entity.Dataset;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.example.industryriskassessmentserver.mapper.DatasetMapper;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileInputStream;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.Collectors;

@Service
public class RiskStatusServiceImpl implements RiskStatusService {
    
    private static final Logger log = LoggerFactory.getLogger(RiskStatusServiceImpl.class);
    
    @Autowired
    private ExcelParser excelParser;
    
    @Autowired
    private DatasetService datasetService;
    
    @Autowired
    private FileUploadConfig fileUploadConfig;

    @Autowired
    private NodeRiskService nodeRiskService;
    
    @Autowired
    private DatasetMapper datasetMapper;
    
    @Override
    public GraphData getIndustryChainGraph(Long industryChainId) {
        String filePath = datasetService.getLatestRelationDataset(industryChainId);
        
        String fullPath = fileUploadConfig.getBasePath() + "/" + filePath;
        log.info("开始解析Excel文件: {}", fullPath);
        
        try (FileInputStream fis = new FileInputStream(new File(fullPath));
             Workbook workbook = new XSSFWorkbook(fis)) {
            
            // 2. 解析各个sheet
            Sheet productSheet = workbook.getSheet("产品编号表");
            if (productSheet == null) {
                throw new BusinessException(500, "Excel文件中未找到'产品编号表'sheet");
            }
            
            Sheet companySheet = workbook.getSheet("公司编号表");
            if (companySheet == null) {
                throw new BusinessException(500, "Excel文件中未找到'公司编号表'sheet");
            }
            
            Sheet productMatrix = workbook.getSheet("产品-产品");
            if (productMatrix == null) {
                throw new BusinessException(500, "Excel文件中未找到'产品-产品'sheet");
            }
            
            Sheet productCompanyMatrix = workbook.getSheet("产品-公司");
            if (productCompanyMatrix == null) {
                throw new BusinessException(500, "Excel文件中未找到'产品-公司'sheet");
            }
            
            // 3. 解析数据
            try {
                Map<String, Integer> productCodes = excelParser.parseProductCodes(productSheet);
                log.info("解析到{}个产品", productCodes.size());
                
                Map<String, Integer> companyCodes = excelParser.parseCompanyCodes(companySheet);
                log.info("解析到{}个公司", companyCodes.size());
                
                boolean[][] productRelations = excelParser.parseProductMatrix(productMatrix, productCodes.size());
                boolean[][] productCompanyRelations = excelParser.parseProductCompanyMatrix(
                    productCompanyMatrix, productCodes.size(), companyCodes.size());
                
                return buildGraphData(productCodes, companyCodes, productRelations, productCompanyRelations);
                
            } catch (Exception e) {
                log.error("解析Excel数据失败", e);
                throw new BusinessException(500, "解析Excel数据失败：" + e.getMessage());
            }
            
        } catch (BusinessException e) {
            throw e;
        } catch (Exception e) {
            log.error("打开Excel文件失败", e);
            throw new BusinessException(500, "打开Excel文件失败：" + e.getMessage());
        }
    }
    
    private GraphData buildGraphData(
        Map<String, Integer> productCodes,
        Map<String, Integer> companyCodes,
        boolean[][] productRelations,
        boolean[][] productCompanyRelations
    ) {
        log.info("开始构建图谱数据");
        GraphData graphData = new GraphData();
        List<GraphNode> nodes = new ArrayList<>();
        List<GraphLink> links = new ArrayList<>();
        
        // 添加产品节点
        log.info("添加产品节点...");
        for (Map.Entry<String, Integer> entry : productCodes.entrySet()) {
            nodes.add(GraphNode.builder()
                .id("P" + entry.getValue())
                .name(entry.getKey())
                .category("产品")
                .symbolSize(18)
                .build());
        }
        
        // 添加公司节点
        log.info("添加公司节点...");
        for (Map.Entry<String, Integer> entry : companyCodes.entrySet()) {
            nodes.add(GraphNode.builder()
                .id("C" + entry.getValue())
                .name(entry.getKey())
                .category("公司")
                .symbolSize(22)
                .build());
        }
        
        // 添加产品间关系
        log.info("添加产品间关系...");
        int productRelationCount = 0;
        for (int i = 0; i < productRelations.length; i++) {
            for (int j = 0; j < productRelations[i].length; j++) {
                if (i != j && productRelations[i][j]) {  // 排除自己和自己的关系
                    log.debug("产品关系: P{} -> P{}, 值: {}", i, j, productRelations[i][j]);
                    links.add(GraphLink.builder()
                        .source("P" + i)
                        .target("P" + j)
                        .value(1)
                        .build());
                    productRelationCount++;
                }
            }
        }
        log.info("产品间关系数量: {}", productRelationCount);
        
        // 添加产品-公司关系
        log.info("添加产品-公司关系...");
        int productCompanyRelationCount = 0;
        for (int i = 0; i < productCompanyRelations.length; i++) {
            for (int j = 0; j < productCompanyRelations[i].length; j++) {
                if (productCompanyRelations[i][j]) {
                    log.debug("产品-公司关系: P{} -> C{}, 值: {}", i, j, productCompanyRelations[i][j]);
                    links.add(GraphLink.builder()
                        .source("P" + i)
                        .target("C" + j)
                        .value(1)
                        .build());
                    productCompanyRelationCount++;
                }
            }
        }
        log.info("产品-公司关系数量: {}", productCompanyRelationCount);
        
        // 添加类别定义
        List<GraphData.Category> categories = new ArrayList<>();
        GraphData.Category productCategory = new GraphData.Category();
        productCategory.setName("product");
        categories.add(productCategory);

        GraphData.Category companyCategory = new GraphData.Category();
        companyCategory.setName("company");
        categories.add(companyCategory);
        
        graphData.setNodes(nodes);
        graphData.setLinks(links);
        graphData.setCategories(categories);  // 设置类别
        
        log.info("图谱数据构建完成: {} 个节点, {} 个关系", nodes.size(), links.size());
        
        return graphData;
    }
    
    @Override
    public RiskOverview getRiskOverview(Long industryChainId, String dataPeriod) {
        log.info("获取产业链[{}]在[{}]期间的风险概览数据", industryChainId, dataPeriod);
        
        // 查询指定产业链和数据期间的特征标签数据集
        Dataset dataset = datasetMapper.selectOne(
            new LambdaQueryWrapper<Dataset>()
                .eq(Dataset::getIndustryChainId, industryChainId)
                .eq(Dataset::getTypeCode, "FEATURE_LABEL")
                .eq(Dataset::getDataPeriod, dataPeriod)
                .eq(Dataset::getDeleted, 0)
                .orderByDesc(Dataset::getCreateTime)
                .last("LIMIT 1")
        );
        
        if (dataset == null) {
            log.warn("未找到产业链[{}]在[{}]期间的特征标签数据", industryChainId, dataPeriod);
            throw new BusinessException(404, "未找到指定期间的特征标签数据");
        }
        
        // 获取完整的文件路径
        String fullPath = fileUploadConfig.getBasePath() + "/" + dataset.getFilePath();
        log.info("准备读取文件: {}", fullPath);
        
        // 验证文件是否存在
        File file = new File(fullPath);
        if (!file.exists() || !file.isFile()) {
            log.error("文件不存在: {}", fullPath);
            throw new BusinessException(404, "特征标签数据文件已丢失，请重新上传");
        }
        
        try (FileInputStream fis = new FileInputStream(file);
             Workbook workbook = new XSSFWorkbook(fis)) {
            
            // 获取第一个Sheet（不限表名）
            if (workbook.getNumberOfSheets() == 0) {
                log.error("Excel文件中没有任何表");
                throw new BusinessException(400, "Excel文件格式错误：文件中没有任何表");
            }
            
            Sheet dataSheet = workbook.getSheetAt(0);
            log.info("使用第一个表：{}", dataSheet.getSheetName());
            
            // 构建公司名称到编号的映射
            Map<String, Integer> companyCodes = new HashMap<>();
            int rowCount = dataSheet.getLastRowNum() + 1;
            log.debug("数据表总行数: {}", rowCount);
            
            // 检查第0行是否为表头
            Row headerRow = dataSheet.getRow(0);
            boolean hasHeader = headerRow != null;
            
            int startRow = hasHeader ? 1 : 0;  // 如果有表头，从第1行开始；否则从第0行开始
            
            // 公司名称通常在第一列
            int nameColumnIndex = 0;
            
            // 找到风险标识列（最后一列）
            int lastColumn = -1;
            if (hasHeader) {
                lastColumn = headerRow.getLastCellNum() - 1;
                log.debug("风险标识列索引: {}", lastColumn);
            } else if (dataSheet.getRow(0) != null) {
                lastColumn = dataSheet.getRow(0).getLastCellNum() - 1;
            }
            
            if (lastColumn < 0) {
                log.warn("未找到风险标识列，使用默认值0");
                lastColumn = 0;
            }
            
            // 解析公司名称和风险数据
            Map<Integer, Boolean> companyRiskMap = new HashMap<>();
            
            for (int i = startRow; i < rowCount; i++) {
                Row row = dataSheet.getRow(i);
                if (row == null) {
                    log.warn("数据表第{}行为空", i);
                    continue;
                }
                
                Cell nameCell = row.getCell(nameColumnIndex);
                Cell riskCell = row.getCell(lastColumn);
                
                if (nameCell != null) {
                    String companyName = "";
                    
                    // 处理不同类型的名称单元格
                    if (nameCell.getCellType() == CellType.STRING) {
                        companyName = nameCell.getStringCellValue().trim();
                    } else if (nameCell.getCellType() == CellType.NUMERIC) {
                        companyName = String.valueOf((int)nameCell.getNumericCellValue());
                    }
                    
                    if (!companyName.isEmpty()) {
                        // 为每个公司分配一个唯一编号
                        int companyCode = i - startRow;
                        companyCodes.put(companyName, companyCode);
                        
                        // 解析风险状态
                        boolean isRisk = false;
                        
                        if (riskCell != null) {
                            // 处理不同类型的风险单元格
                            if (riskCell.getCellType() == CellType.NUMERIC) {
                                isRisk = riskCell.getNumericCellValue() == 1;
                            } else if (riskCell.getCellType() == CellType.STRING) {
                                String value = riskCell.getStringCellValue().trim();
                                isRisk = "1".equals(value) || "是".equals(value) || "true".equalsIgnoreCase(value);
                            } else if (riskCell.getCellType() == CellType.BOOLEAN) {
                                isRisk = riskCell.getBooleanCellValue();
                            }
                        }
                        
                        companyRiskMap.put(companyCode, isRisk);
                        log.debug("解析公司风险: {} (编码: {}) -> {}", companyName, companyCode, isRisk ? "风险" : "正常");
                    }
                }
            }
            
            // 构建风险概览数据
            RiskOverview riskOverview = new RiskOverview();
            
            // 计算风险公司数量和总公司数量
            int totalCompanyCount = companyCodes.size();
            int riskCompanyCount = (int) companyRiskMap.values().stream().filter(Boolean::booleanValue).count();
            
            riskOverview.setTotalCompanyCount(totalCompanyCount);
            riskOverview.setRiskCompanyCount(riskCompanyCount);
            
            // 获取风险公司和正常公司列表
            List<String> riskCompanies = new ArrayList<>();
            List<String> normalCompanies = new ArrayList<>();
            
            for (Map.Entry<String, Integer> entry : companyCodes.entrySet()) {
                String companyName = entry.getKey();
                Integer companyCode = entry.getValue();
                Boolean isRisk = companyRiskMap.getOrDefault(companyCode, false);
                
                if (isRisk) {
                    riskCompanies.add(companyName);
                } else {
                    normalCompanies.add(companyName);
                }
            }
            
            riskOverview.setRiskCompanies(riskCompanies);
            riskOverview.setNormalCompanies(normalCompanies);

            double riskRatio = totalCompanyCount == 0 ? 0 : (double) riskCompanyCount / totalCompanyCount;
            riskOverview.setRiskLevel(determineRiskLevel(totalCompanyCount, riskRatio));

            double resilience = generateScore();
            double recovery = generateScore();
            double integrity = formatScore((resilience + recovery) / 2);
            riskOverview.setResilienceScore(resilience);
            riskOverview.setRecoveryScore(recovery);
            riskOverview.setIntegrityScore(integrity);
            riskOverview.setIntegrityLevel(determineIntegrityLevel(integrity));
            riskOverview.setNextPeriodLabel("T+1期");
            riskOverview.setNextPeriodRiskCompanyCount(0);
            riskOverview.setNextPeriodRiskLevel("待评估");
            populateNextPeriodForecast(industryChainId, dataPeriod, riskOverview);
            
            log.info("风险概览数据生成完成: 总公司数={}, 风险公司数={}", totalCompanyCount, riskCompanyCount);
            return riskOverview;
            
        } catch (Exception e) {
            log.error("解析Excel文件失败", e);
            throw new BusinessException(500, "解析Excel文件失败: " + e.getMessage());
        }
    }

    private String determineRiskLevel(int totalCompanyCount, double riskRatio) {
        if (totalCompanyCount == 0) {
            return "待评估";
        }
        if (riskRatio > 0.5) {
            return "高风险";
        }
        if (riskRatio > 0.35) {
            return "中风险";
        }
        return "低风险";
    }

    private String determineIntegrityLevel(double integrityScore) {
        return integrityScore >= 0.68 ? "完整" : "不完整";
    }

    // 旧版布局逻辑已移除，使用前端力导向自动布局

    private double generateScore() {
        double raw = 0.65 + ThreadLocalRandom.current().nextDouble(0.08);
        return formatScore(raw);
    }

    private double formatScore(double value) {
        return BigDecimal.valueOf(value).setScale(2, RoundingMode.HALF_UP).doubleValue();
    }

    private void populateNextPeriodForecast(Long industryChainId, String dataPeriod, RiskOverview overview) {
        try {
            NextPeriodRiskSummary summary = nodeRiskService.getNextPeriodSummary(industryChainId, dataPeriod);
            if (summary == null) {
                return;
            }
            overview.setNextPeriodLabel("T+1期");
            overview.setNextPeriodRiskCompanyCount(summary.getRiskCompanyCount());
            double ratio = summary.getTotalCompanyCount() == 0
                    ? 0
                    : (double) summary.getRiskCompanyCount() / summary.getTotalCompanyCount();
            overview.setNextPeriodRiskLevel(determineRiskLevel(summary.getTotalCompanyCount(), ratio));
        } catch (Exception ex) {
            log.warn("无法计算T+1期风险预测: {}", ex.getMessage());
        }
    }
}
