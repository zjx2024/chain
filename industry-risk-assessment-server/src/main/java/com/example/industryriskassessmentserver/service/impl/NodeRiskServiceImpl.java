package com.example.industryriskassessmentserver.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.StringUtils;
import com.example.industryriskassessmentserver.common.ErrorCode;
import com.example.industryriskassessmentserver.config.FileUploadConfig;
import com.example.industryriskassessmentserver.dto.risk.NextPeriodRiskSummary;
import com.example.industryriskassessmentserver.entity.Dataset;
import com.example.industryriskassessmentserver.exception.BusinessException;
import com.example.industryriskassessmentserver.entity.IndustryChain;
import com.example.industryriskassessmentserver.mapper.DatasetMapper;
import com.example.industryriskassessmentserver.mapper.IndustryChainMapper;
import com.example.industryriskassessmentserver.service.NodeRiskService;
import com.example.industryriskassessmentserver.service.RiskAlertModelService;
import com.example.industryriskassessmentserver.vo.NodeRiskAlertVO;
import com.example.industryriskassessmentserver.vo.NodeRiskStatusVO;
import com.example.industryriskassessmentserver.vo.RiskFactorVO;
import org.apache.poi.ss.usermodel.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.Random;

@Service
public class NodeRiskServiceImpl implements NodeRiskService {

    @Value("${risk.node.base-path}")
    private String basePath;

    @Value("${risk.node.ic-file}")
    private String icFileName;

    @Value("${risk.node.ei-file}")
    private String eiFileName;

    @Value("${risk.node.future.ic-path}")
    private String futureIcPath;

    @Value("${risk.node.future.ei-path}")
    private String futureEiPath;

    @Value("${risk.node.future.ic-prefix:集成电路}")
    private String futureIcPrefix;

    @Value("${risk.node.future.ei-prefix:电子信息}")
    private String futureEiPrefix;

    @Autowired
    private IndustryChainMapper industryChainMapper;

    @Autowired
    private DatasetMapper datasetMapper;

    @Autowired
    private FileUploadConfig fileUploadConfig;

    @Autowired
    private RiskAlertModelService riskAlertModelService;

    private static final List<String> FACTOR_NAMES = Arrays.asList(
            "每股营业收入 [单位]元",
            "净资产收益率ROE(平均) [单位]%",
            "销售净利率 [单位]%",
            "资产负债率 [单位]%",
            "流动比率",
            "速动比率",
            "现金比率",
            "净资产负债率",
            "经营活动产生的现金流量净额/负债合计",
            "存货周转率 [单位]次",
            "应收账款周转率(不含应收票据) [单位]次",
            "流动资产周转率 [单位]次",
            "非流动资产周转率 [单位]%",
            "总资产周转率 [单位]次",
            "营业收入同比增长率 [单位]%",
            "总资产同比增长率 [单位]%",
            "每股净资产相对年初增长率 [单位]%",
            "总资产净利率-不含少数股东损益 [单位]%"
    );

    private static final int FACTOR_COUNT = FACTOR_NAMES.size();

    private final Map<String, NodeRiskDataset> datasetCache = new ConcurrentHashMap<>();

    @Override
    public List<String> listCompanyNames(Long industryChainId) {
        IndustryChain chain = getIndustryChain(industryChainId);
        NodeRiskDataset dataset = loadDatasetByChain(chain);
        return dataset.getCompanyNames();
    }

    @Override
    public NodeRiskStatusVO getNodeRiskStatus(Long industryChainId, String dataPeriod, String companyName) {
        if (industryChainId == null || StringUtils.isBlank(dataPeriod) || StringUtils.isBlank(companyName)) {
            throw new BusinessException(ErrorCode.PARAM_ERROR.getCode(), "产业链、数据期间和公司名称不能为空");
        }
        IndustryChain chain = getIndustryChain(industryChainId);
        NodeRiskDataset dataset = loadDatasetByChain(chain);
        NodeRiskDataset.CompanyRiskRecord record = dataset.getCompanyRisk(companyName.trim());
        if (record == null) {
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "未找到该公司对应的节点风险信息");
        }

        int periodIndex = dataset.getPeriodIndex(dataPeriod.trim());
        if (periodIndex < 0) {
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "节点风险文件中不存在该数据期间");
        }

        int currentRisk = record.getRiskByIndex(periodIndex);
        int nextIndex = dataset.getNextPeriodIndex(periodIndex);
        int nextRisk = record.getRiskByIndex(nextIndex);

        String currentPeriodValue = dataset.getPeriods().get(periodIndex);
        String nextPeriodValue = dataset.getPeriods().get(nextIndex);

        NodeRiskStatusVO vo = new NodeRiskStatusVO();
        vo.setCompanyName(record.getCompanyName());
        vo.setDataPeriod(currentPeriodValue);
        vo.setCurrentRisk(currentRisk == 1);
        vo.setNextPeriod("T+1期");
        vo.setActualNextPeriod(nextPeriodValue);
        vo.setNextPeriodRisk(nextRisk == 1);
        int rowIndex = record.getRowIndex();
        vo.setCurrentFactors(loadRiskFactorsForPeriod(chain.getId(), currentPeriodValue, rowIndex));
        List<RiskFactorVO> nextFactors = loadNextPeriodFactors(chain.getCode(), nextPeriodValue, rowIndex);
        String fluctuationSeed = record.getCompanyName() + "_" + nextPeriodValue;
        vo.setNextPeriodFactors(applyVirtualFluctuation(nextFactors, fluctuationSeed));
        return vo;
    }

    @Override
    public NodeRiskAlertVO getNodeRiskAlert(Long industryChainId, String dataPeriod, String companyName) {
        NodeRiskStatusVO statusVO = getNodeRiskStatus(industryChainId, dataPeriod, companyName);
        return riskAlertModelService.analyze(
                statusVO.getCompanyName(),
                statusVO.getActualNextPeriod(),
                statusVO.isNextPeriodRisk(),
                resolveAlertLevel(statusVO.isNextPeriodRisk()),
                statusVO.getNextPeriodFactors()
        );
    }

    @Override
    public NextPeriodRiskSummary getNextPeriodSummary(Long industryChainId, String dataPeriod) {
        if (industryChainId == null || StringUtils.isBlank(dataPeriod)) {
            throw new BusinessException(ErrorCode.PARAM_ERROR.getCode(), "产业链和数据期间不能为空");
        }
        IndustryChain chain = getIndustryChain(industryChainId);
        NodeRiskDataset dataset = loadDatasetByChain(chain);
        int periodIndex = dataset.getPeriodIndex(dataPeriod.trim());
        if (periodIndex < 0) {
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "节点风险文件中不存在该数据期间");
        }
        int nextIndex = dataset.getNextPeriodIndex(periodIndex);
        int total = 0;
        int riskCount = 0;
        for (NodeRiskDataset.CompanyRiskRecord record : dataset.getCompanyRiskRecords()) {
            total++;
            if (record.getRiskByIndex(nextIndex) == 1) {
                riskCount++;
            }
        }
        String nextLabel = dataset.getPeriods().isEmpty() ? "T+1期" : dataset.getPeriods().get(nextIndex);
        return new NextPeriodRiskSummary(nextLabel, riskCount, total);
    }

    private IndustryChain getIndustryChain(Long industryChainId) {
        IndustryChain chain = industryChainMapper.selectById(industryChainId);
        if (chain == null) {
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "产业链不存在");
        }
        return chain;
    }

    private NodeRiskDataset loadDatasetByChain(IndustryChain chain) {
        return datasetCache.computeIfAbsent(chain.getCode(), this::loadDataset);
    }

    private List<RiskFactorVO> loadRiskFactorsForPeriod(Long industryChainId, String dataPeriod, int rowIndex) {
        Path filePath = resolveFeatureDatasetPath(industryChainId, dataPeriod);
        List<Double> values = readFactorValues(filePath, rowIndex);
        return buildFactorVOs(values);
    }

    private List<RiskFactorVO> loadNextPeriodFactors(String chainCode, String period, int rowIndex) {
        Path filePath = resolveFutureDatasetPath(chainCode, period);
        List<Double> values = readFactorValues(filePath, rowIndex);
        return buildFactorVOs(values);
    }

    private NodeRiskDataset loadDataset(String chainCode) {
        String fileName = resolveFileName(chainCode);
        if (fileName == null) {
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "暂未配置该产业链的节点风险文件");
        }
        Path filePath = Paths.get(basePath, fileName);
        if (!Files.exists(filePath)) {
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "节点风险文件不存在：" + filePath);
        }
        try (Workbook workbook = WorkbookFactory.create(Files.newInputStream(filePath))) {
            Sheet sheet = workbook.getSheetAt(0);
            if (sheet == null) {
                throw new BusinessException(ErrorCode.INTERNAL_ERROR.getCode(), "节点风险文件中没有工作表");
            }
            DataFormatter formatter = new DataFormatter();

            Row headerRow = sheet.getRow(0);
            if (headerRow == null) {
                throw new BusinessException(ErrorCode.INTERNAL_ERROR.getCode(), "节点风险文件缺少表头");
            }

            List<String> periods = new ArrayList<>();
            int lastCellNum = headerRow.getLastCellNum();
            for (int i = 2; i < lastCellNum; i++) { // 前两列为编号和公司名
                Cell cell = headerRow.getCell(i);
                String header = formatter.formatCellValue(cell).trim();
                if (header.isEmpty()) {
                    continue;
                }
                periods.add(header);
            }
            if (periods.isEmpty()) {
                throw new BusinessException(ErrorCode.INTERNAL_ERROR.getCode(), "节点风险文件中未找到任何期间列");
            }

            Map<String, NodeRiskDataset.CompanyRiskRecord> companyMap = new LinkedHashMap<>();
            for (int rowIndex = 1; rowIndex <= sheet.getLastRowNum(); rowIndex++) {
                Row row = sheet.getRow(rowIndex);
                if (row == null) {
                    continue;
                }
                String companyName = formatter.formatCellValue(row.getCell(1)).trim();
                if (companyName.isEmpty()) {
                    continue;
                }

                int[] risks = new int[periods.size()];
                for (int i = 0; i < periods.size(); i++) {
                    Cell cell = row.getCell(i + 2);
                    String value = formatter.formatCellValue(cell).trim();
                    risks[i] = "1".equals(value) ? 1 : 0;
                }

                int companyRowIndex = parseRowIdentifier(row, formatter, rowIndex - 1);
                companyMap.put(companyName, new NodeRiskDataset.CompanyRiskRecord(companyName, risks, companyRowIndex));
            }

            return new NodeRiskDataset(periods, companyMap);
        } catch (IOException e) {
            throw new BusinessException(ErrorCode.INTERNAL_ERROR.getCode(), "读取节点风险文件失败：" + e.getMessage());
        }
    }

    private String resolveFileName(String chainCode) {
        if ("IC".equalsIgnoreCase(chainCode)) {
            return icFileName;
        }
        if ("EI".equalsIgnoreCase(chainCode)) {
            return eiFileName;
        }
        return null;
    }

    private Path resolveFeatureDatasetPath(Long industryChainId, String dataPeriod) {
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
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "未找到对应期间的特征标签数据，请先上传数据集");
        }
        Path filePath = Paths.get(fileUploadConfig.getBasePath(), dataset.getFilePath());
        if (!Files.exists(filePath)) {
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "特征标签数据文件不存在：" + filePath);
        }
        return filePath;
    }

    private Path resolveFutureDatasetPath(String chainCode, String period) {
        String directory;
        String prefix;
        if ("IC".equalsIgnoreCase(chainCode)) {
            directory = futureIcPath;
            prefix = futureIcPrefix;
        } else if ("EI".equalsIgnoreCase(chainCode)) {
            directory = futureEiPath;
            prefix = futureEiPrefix;
        } else {
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "暂未配置该产业链的T+1特征数据文件");
        }
        if (directory == null || directory.isEmpty() || prefix == null || prefix.isEmpty()) {
            throw new BusinessException(ErrorCode.INTERNAL_ERROR.getCode(), "T+1特征文件目录信息未配置完整");
        }
        Path filePath = Paths.get(directory, prefix + "_" + period + ".xlsx");
        if (!Files.exists(filePath)) {
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "未找到对应的T+1特征文件：" + filePath);
        }
        return filePath;
    }

    private List<Double> readFactorValues(Path filePath, int targetRowIndex) {
        if (!Files.exists(filePath)) {
            throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "特征标签文件不存在：" + filePath);
        }
        try (Workbook workbook = WorkbookFactory.create(Files.newInputStream(filePath))) {
            Sheet sheet = workbook.getSheetAt(0);
            if (sheet == null) {
                throw new BusinessException(ErrorCode.INTERNAL_ERROR.getCode(), "特征标签文件缺少工作表");
            }
            DataFormatter formatter = new DataFormatter();
            for (int rowIdx = 1; rowIdx <= sheet.getLastRowNum(); rowIdx++) {
                Row row = sheet.getRow(rowIdx);
                if (row == null) {
                    continue;
                }
                int currentIndex = parseRowIdentifier(row, formatter, rowIdx - 1);
                if (currentIndex == targetRowIndex) {
                    return extractFactorValues(row, formatter);
                }
            }
        } catch (IOException e) {
            throw new BusinessException(ErrorCode.INTERNAL_ERROR.getCode(), "读取特征标签数据失败：" + e.getMessage());
        }
        throw new BusinessException(ErrorCode.NOT_FOUND.getCode(), "特征标签数据中未找到匹配的公司行");
    }

    private List<Double> extractFactorValues(Row row, DataFormatter formatter) {
        List<Double> values = new ArrayList<>(FACTOR_COUNT);
        for (int col = 1; col <= FACTOR_COUNT; col++) {
            values.add(parseNumericValue(row.getCell(col), formatter));
        }
        return values;
    }

    private Double parseNumericValue(Cell cell, DataFormatter formatter) {
        if (cell == null) {
            return null;
        }
        if (cell.getCellType() == CellType.NUMERIC) {
            return cell.getNumericCellValue();
        }
        String text = formatter.formatCellValue(cell).trim();
        if (text.isEmpty()) {
            return null;
        }
        try {
            return Double.parseDouble(text);
        } catch (NumberFormatException ex) {
            return null;
        }
    }

    private List<RiskFactorVO> buildFactorVOs(List<Double> values) {
        List<RiskFactorVO> factors = new ArrayList<>(FACTOR_COUNT);
        for (int i = 0; i < FACTOR_COUNT; i++) {
            RiskFactorVO factorVO = new RiskFactorVO();
            factorVO.setIndex(i);
            factorVO.setName(FACTOR_NAMES.get(i));
            factorVO.setValue(values != null && i < values.size() ? values.get(i) : null);
            factors.add(factorVO);
        }
        return factors;
    }

    private String resolveAlertLevel(boolean hasRisk) {
        return hasRisk ? "HIGH" : "LOW";
    }

    private int parseRowIdentifier(Row row, DataFormatter formatter, int fallback) {
        Cell idCell = row.getCell(0);
        if (idCell == null) {
            return fallback;
        }
        String raw = formatter.formatCellValue(idCell).trim();
        if (raw.isEmpty()) {
            return fallback;
        }
        try {
            return (int) Math.round(Double.parseDouble(raw));
        } catch (NumberFormatException ex) {
            return fallback;
        }
    }

    private List<RiskFactorVO> applyVirtualFluctuation(List<RiskFactorVO> factors, String seedKey) {
        if (factors == null) {
            return null;
        }
        long seed = seedKey == null ? 0L : seedKey.hashCode();
        Random random = new Random(seed);
        for (RiskFactorVO factor : factors) {
            Double origin = factor.getValue();
            if (origin == null) {
                continue;
            }
            double adjusted = origin + calculateOffset(factor.getIndex(), origin, random);
            adjusted = clampValue(factor.getIndex(), adjusted);
            factor.setValue(round(adjusted));
        }
        return factors;
    }

    private double calculateOffset(int index, double value, Random random) {
        double direction = random.nextBoolean() ? 1.0 : -1.0;
        switch (index) {
            case 0:
                return direction * Math.max(0.2, Math.abs(value) * randomRange(random, 0.03, 0.08));
            case 1:
            case 2:
            case 8:
            case 12:
            case 14:
            case 15:
            case 16:
            case 17:
                return direction * Math.max(0.5, Math.abs(value) * randomRange(random, 0.04, 0.1));
            case 3:
                return direction * randomRange(random, 1.0, 3.5);
            case 4:
                return direction * randomRange(random, 0.05, 0.18);
            case 5:
                return direction * randomRange(random, 0.05, 0.15);
            case 6:
                return direction * randomRange(random, 0.03, 0.12);
            case 7:
                return direction * randomRange(random, 0.08, 0.2);
            case 9:
                return direction * randomRange(random, 0.15, 0.45);
            case 10:
                return direction * randomRange(random, 0.2, 0.6);
            case 11:
                return direction * randomRange(random, 0.08, 0.25);
            case 13:
                return direction * randomRange(random, 0.05, 0.18);
            default:
                return direction * randomRange(random, 0.05, 0.2);
        }
    }

    private double clampValue(int index, double value) {
        switch (index) {
            case 0:
                return Math.max(value, 0);
            case 1:
            case 2:
            case 8:
                return Math.max(Math.min(value, 120), -100);
            case 3:
                return Math.max(Math.min(value, 100), 0);
            case 4:
            case 5:
            case 6:
            case 7:
            case 9:
            case 10:
            case 11:
            case 13:
                return Math.max(value, 0);
            case 12:
                return Math.max(Math.min(value, 150), 0);
            case 14:
            case 15:
            case 16:
            case 17:
                return Math.max(Math.min(value, 200), -200);
            default:
                return value;
        }
    }

    private double randomRange(Random random, double min, double max) {
        return min + (max - min) * random.nextDouble();
    }

    private double round(double value) {
        return Math.round(value * 10000.0) / 10000.0;
    }

    /**
     * 简单的数据集缓存结构
     */
    private static class NodeRiskDataset {
        private final List<String> periods;
        private final Map<String, CompanyRiskRecord> companyRiskMap;

        NodeRiskDataset(List<String> periods, Map<String, CompanyRiskRecord> companyRiskMap) {
            this.periods = Collections.unmodifiableList(periods);
            this.companyRiskMap = companyRiskMap;
        }

        List<String> getPeriods() {
            return periods;
        }

        List<String> getCompanyNames() {
            return new ArrayList<>(companyRiskMap.keySet());
        }

        Collection<CompanyRiskRecord> getCompanyRiskRecords() {
            return companyRiskMap.values();
        }

        CompanyRiskRecord getCompanyRisk(String companyName) {
            CompanyRiskRecord record = companyRiskMap.get(companyName);
            if (record != null) {
                return record;
            }
            // 尝试忽略大小写匹配
            return companyRiskMap.entrySet().stream()
                    .filter(entry -> entry.getKey().equalsIgnoreCase(companyName))
                    .map(Map.Entry::getValue)
                    .findFirst()
                    .orElse(null);
        }

        int getPeriodIndex(String dataPeriod) {
            for (int i = 0; i < periods.size(); i++) {
                if (periods.get(i).equalsIgnoreCase(dataPeriod)) {
                    return i;
                }
            }
            return -1;
        }

        int getNextPeriodIndex(int currentIndex) {
            if (periods.isEmpty()) {
                return currentIndex;
            }
            return (currentIndex + 1) % periods.size();
        }

        private static class CompanyRiskRecord {
            private final String companyName;
            private final int[] risks;
            private final int rowIndex;

            CompanyRiskRecord(String companyName, int[] risks, int rowIndex) {
                this.companyName = companyName;
                this.risks = risks;
                this.rowIndex = rowIndex;
            }

            String getCompanyName() {
                return companyName;
            }

            int getRiskByIndex(int index) {
                if (index < 0 || index >= risks.length) {
                    return 0;
                }
                return risks[index];
            }

            int getRowIndex() {
                return rowIndex;
            }
        }
    }
}
