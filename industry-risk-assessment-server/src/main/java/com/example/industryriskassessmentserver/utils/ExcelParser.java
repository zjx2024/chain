package com.example.industryriskassessmentserver.utils;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.stereotype.Component;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileInputStream;
import java.util.*;

@Component
public class ExcelParser {
    
    private static final Logger log = LoggerFactory.getLogger(ExcelParser.class);
    
    public Map<String, Integer> parseProductCodes(Sheet sheet) {
        Map<String, Integer> productCodes = new HashMap<>();
        int rowCount = sheet.getLastRowNum() + 1;
        log.debug("产品表总行数: {}", rowCount);
        
        // 检查第0行是否为表头
        Row headerRow = sheet.getRow(0);
        boolean hasHeader = headerRow != null && 
                            headerRow.getCell(0) != null && 
                            headerRow.getCell(0).getStringCellValue().contains("产品");
        
        int startRow = hasHeader ? 1 : 0;  // 如果有表头，从第1行开始；否则从第0行开始
        
        for (int i = startRow; i < rowCount; i++) {
            Row row = sheet.getRow(i);
            if (row == null) {
                log.warn("产品表第{}行为空", i);
                continue;
            }
            
            Cell nameCell = row.getCell(0);
            Cell codeCell = row.getCell(1);
            
            if (nameCell != null && codeCell != null) {
                String name = nameCell.getStringCellValue();
                int code;
                
                // 处理不同类型的单元格
                if (codeCell.getCellType() == CellType.NUMERIC) {
                    code = (int) codeCell.getNumericCellValue();
                } else {
                    // 尝试将字符串转换为整数
                    try {
                        code = Integer.parseInt(codeCell.getStringCellValue().trim());
                    } catch (NumberFormatException e) {
                        log.warn("产品表第{}行编号格式错误: {}", i, codeCell.getStringCellValue());
                        continue;
                    }
                }
                
                productCodes.put(name, code);
                log.debug("解析产品: {} -> {}", name, code);
            } else {
                log.warn("产品表第{}行数据不完整", i);
            }
        }
        
        log.info("成功解析{}个产品", productCodes.size());
        return productCodes;
    }
    
    public Map<String, Integer> parseCompanyCodes(Sheet sheet) {
        Map<String, Integer> companyCodes = new HashMap<>();
        int rowCount = sheet.getLastRowNum() + 1;
        log.debug("公司表总行数: {}", rowCount);
        
        // 检查第0行是否为表头
        Row headerRow = sheet.getRow(0);
        boolean hasHeader = headerRow != null && 
                            headerRow.getCell(0) != null && 
                            headerRow.getCell(0).getStringCellValue().contains("公司");
        
        int startRow = hasHeader ? 1 : 0;  // 如果有表头，从第1行开始；否则从第0行开始
        
        for (int i = startRow; i < rowCount; i++) {
            Row row = sheet.getRow(i);
            if (row == null) {
                log.warn("公司表第{}行为空", i);
                continue;
            }
            
            Cell nameCell = row.getCell(0);
            Cell codeCell = row.getCell(1);
            
            if (nameCell != null && codeCell != null) {
                String name = nameCell.getStringCellValue();
                int code;
                
                if (codeCell.getCellType() == CellType.NUMERIC) {
                    code = (int) codeCell.getNumericCellValue();
                } else {
                    try {
                        code = Integer.parseInt(codeCell.getStringCellValue().trim());
                    } catch (NumberFormatException e) {
                        log.warn("公司表第{}行编号格式错误: {}", i, codeCell.getStringCellValue());
                        continue;
                    }
                }
                
                companyCodes.put(name, code);
                log.debug("解析公司: {} -> {}", name, code);
            } else {
                log.warn("公司表第{}行数据不完整", i);
            }
        }
        
        log.info("成功解析{}个公司", companyCodes.size());
        return companyCodes;
    }
    
    public boolean[][] parseProductMatrix(Sheet sheet, int size) {
        boolean[][] matrix = new boolean[size][size];
        
        // 检查是否有表头行和表头列
        boolean hasHeaderRow = sheet.getRow(0) != null;
        boolean hasHeaderCol = hasHeaderRow && sheet.getRow(0).getCell(0) != null;
        
        int startRow = hasHeaderRow ? 1 : 0;
        int startCol = hasHeaderCol ? 1 : 0;
        
        for (int i = startRow; i < startRow + size; i++) {
            Row row = sheet.getRow(i);
            if (row == null) {
                log.warn("产品矩阵第{}行为空", i);
                continue;
            }
            
            for (int j = startCol; j < startCol + size; j++) {
                Cell cell = row.getCell(j);
                if (cell == null) {
                    log.warn("产品矩阵第{}行第{}列为空", i, j);
                    continue;
                }
                
                try {
                    matrix[i-startRow][j-startCol] = cell.getNumericCellValue() == 1;
                } catch (Exception e) {
                    log.warn("产品矩阵第{}行第{}列数据格式错误", i, j);
                }
            }
        }
        return matrix;
    }
    
    public boolean[][] parseProductCompanyMatrix(Sheet sheet, int productSize, int companySize) {
        boolean[][] matrix = new boolean[productSize][companySize];
        
        // 检查是否有表头行和表头列
        boolean hasHeaderRow = sheet.getRow(0) != null;
        boolean hasHeaderCol = hasHeaderRow && sheet.getRow(0).getCell(0) != null;
        
        int startRow = hasHeaderRow ? 1 : 0;
        int startCol = hasHeaderCol ? 1 : 0;
        
        for (int i = startRow; i < startRow + productSize; i++) {
            Row row = sheet.getRow(i);
            if (row == null) {
                log.warn("产品-公司矩阵第{}行为空", i);
                continue;
            }
            
            for (int j = startCol; j < startCol + companySize; j++) {
                Cell cell = row.getCell(j);
                if (cell == null) {
                    log.warn("产品-公司矩阵第{}行第{}列为空", i, j);
                    continue;
                }
                
                try {
                    matrix[i-startRow][j-startCol] = cell.getNumericCellValue() == 1;
                } catch (Exception e) {
                    log.warn("产品-公司矩阵第{}行第{}列数据格式错误", i, j);
                }
            }
        }
        return matrix;
    }
    
    /**
     * 解析公司风险数据
     * @param sheet 公司风险数据表
     * @param companyCodes 公司编码映射
     * @return 公司风险状态映射，key为公司编码，value为是否为风险公司（true表示风险公司）
     */
    public Map<Integer, Boolean> parseCompanyRiskData(Sheet sheet, Map<String, Integer> companyCodes) {
        Map<Integer, Boolean> riskMap = new HashMap<>();
        int rowCount = sheet.getLastRowNum() + 1;
        log.debug("风险数据表总行数: {}", rowCount);
        
        // 检查第0行是否为表头
        Row headerRow = sheet.getRow(0);
        boolean hasHeader = headerRow != null;
        
        int startRow = hasHeader ? 1 : 0;  // 如果有表头，从第1行开始；否则从第0行开始
        
        // 找到风险标识列（最后一列）
        int lastColumn = -1;
        if (hasHeader) {
            lastColumn = headerRow.getLastCellNum() - 1;
            log.debug("风险标识列索引: {}", lastColumn);
        }
        
        if (lastColumn < 0) {
            log.warn("未找到风险标识列");
            return riskMap;
        }
        
        // 公司名称通常在第一列
        int nameColumnIndex = 0;
        
        for (int i = startRow; i < rowCount; i++) {
            Row row = sheet.getRow(i);
            if (row == null) {
                log.warn("风险数据表第{}行为空", i);
                continue;
            }
            
            Cell nameCell = row.getCell(nameColumnIndex);
            Cell riskCell = row.getCell(lastColumn);
            
            if (nameCell != null && riskCell != null) {
                String companyName = nameCell.getStringCellValue().trim();
                Integer companyCode = companyCodes.get(companyName);
                
                if (companyCode == null) {
                    log.warn("未找到公司编码: {}", companyName);
                    continue;
                }
                
                boolean isRisk = false;
                
                // 处理不同类型的风险单元格
                if (riskCell.getCellType() == CellType.NUMERIC) {
                    isRisk = riskCell.getNumericCellValue() == 1;
                } else if (riskCell.getCellType() == CellType.STRING) {
                    String value = riskCell.getStringCellValue().trim();
                    isRisk = "1".equals(value) || "是".equals(value) || "true".equalsIgnoreCase(value);
                } else if (riskCell.getCellType() == CellType.BOOLEAN) {
                    isRisk = riskCell.getBooleanCellValue();
                }
                
                riskMap.put(companyCode, isRisk);
                log.debug("解析公司风险: {} (编码: {}) -> {}", companyName, companyCode, isRisk ? "风险" : "正常");
            } else {
                log.warn("风险数据表第{}行数据不完整", i);
            }
        }
        
        log.info("成功解析{}个公司风险数据", riskMap.size());
        return riskMap;
    }
} 