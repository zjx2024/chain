package com.example.industryriskassessmentserver.service;

import com.example.industryriskassessmentserver.dto.ModelTestRequest;
import com.example.industryriskassessmentserver.dto.ModelTestResult;
import com.example.industryriskassessmentserver.entity.Dataset;
import com.example.industryriskassessmentserver.entity.TrainedModel;
import com.example.industryriskassessmentserver.config.ModelStorageConfig;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

@Slf4j
@Service
public class ModelTestService {
    
    @Autowired
    private TrainedModelService trainedModelService;
    
    @Autowired
    private DatasetService datasetService;
    
    @Autowired
    private ModelStorageConfig modelStorageConfig;
    
    @Value("${model.training.python-env:${CHAIN_PYTHON_ENV:/usr/bin/python3}}")
    private String pythonExecutable;

    @Value("${chain.base-path:${CHAIN_BASE_PATH:/data/chain}}")
    private String chainBasePath;

    @Value("${chain.datasets-path:}")
    private String datasetsPathOverride;
    
    /**
     * 异步执行模型测试
     */
    public CompletableFuture<ModelTestResult> testModelAsync(ModelTestRequest request) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return testModel(request);
            } catch (Exception e) {
                log.error("模型测试失败", e);
                ModelTestResult result = new ModelTestResult();
                result.setStatus("FAILED");
                result.setErrorMessage(e.getMessage());
                result.setTestTime(LocalDateTime.now());
                return result;
            }
        });
    }
    
    /**
     * 执行模型测试
     */
    public ModelTestResult testModel(ModelTestRequest request) throws IOException, InterruptedException {
        log.info("开始执行模型测试，请求参数: {}", request);
        
        // 1. 获取训练后模型信息
        TrainedModel trainedModel = getTrainedModel(request);
        
        // 2. 获取测试数据集信息
        Dataset testDataset = getTestDataset(request);
        
        // 3. 构建测试命令
        List<String> command = buildTestCommand(request, trainedModel, testDataset);
        
        // 4. 执行测试
        ModelTestResult result = executeTest(command, trainedModel, testDataset);
        
        log.info("模型测试完成: {}", trainedModel.getTrainedModelName());
        return result;
    }
    
    /**
     * 获取训练后模型
     */
    private TrainedModel getTrainedModel(ModelTestRequest request) {
        TrainedModel trainedModel = null;
        
        if (request.getTrainedModelId() != null) {
            trainedModel = trainedModelService.getById(request.getTrainedModelId());
        } else if (request.getTrainedModelName() != null) {
            trainedModel = trainedModelService.getByTrainedModelName(request.getTrainedModelName());
        }
        
        if (trainedModel == null) {
            throw new RuntimeException("训练后模型不存在");
        }
        
        return trainedModel;
    }
    
    /**
     * 获取测试数据集
     */
    private Dataset getTestDataset(ModelTestRequest request) {
        if (request.getTestDatasetId() != null) {
            Dataset dataset = datasetService.getDatasetById(request.getTestDatasetId());
            if (dataset == null) {
                throw new RuntimeException("测试数据集不存在: " + request.getTestDatasetId());
            }
            return dataset;
        }
        return null; // 可以为空，使用模型训练时的数据集
    }
    
    /**
     * 构建测试命令
     */
    private List<String> buildTestCommand(ModelTestRequest request, TrainedModel trainedModel, Dataset testDataset) {
        List<String> command = new ArrayList<>();
        
        // Python可执行文件路径
        command.add(pythonExecutable);
        
        // 测试脚本路径
        String originalModelPath = modelStorageConfig.getModelFullPath(
            trainedModel.getOriginalModelName().replace("GPFedRec-TopkEF21", "GPFedRec-TopkEF21/")
        );
        String testScriptPath = originalModelPath + File.separator + "test_model.py";
        command.add(testScriptPath);
        
        // 训练后模型名称
        command.add("--trained_model_name");
        command.add(resolveActualModelFolder(trainedModel));
        
        // 测试数据集路径
        if (request.getTestDatasetPath() != null) {
            command.add("--dataset_path");
            command.add(request.getTestDatasetPath());
        } else if (testDataset != null) {
            String datasetPath = getDatasetFullPath(testDataset);
            command.add("--dataset_path");
            command.add(datasetPath);
        }
        
        // 测试参数
        if (request.getTestBatchSize() != null) {
            command.add("--test_batch_size");
            command.add(request.getTestBatchSize().toString());
        }
        
        if (request.getDevice() != null) {
            command.add("--device");
            command.add(request.getDevice());
        }
        
        // 输出结果路径
        if (request.getSaveResults() && request.getOutputPath() != null) {
            command.add("--output_results");
            command.add(request.getOutputPath());
        } else if (request.getSaveResults()) {
            // 自动生成输出路径
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            String outputPath = trainedModel.getModelSavePath() + File.separator + 
                               "test_results_" + timestamp + ".json";
            command.add("--output_results");
            command.add(outputPath);
        }
        
        log.info("构建的测试命令: {}", String.join(" ", command));
        return command;
    }

    private String resolveActualModelFolder(TrainedModel trainedModel) {
        try {
            if (trainedModel.getModelSavePath() != null) {
                Path path = Paths.get(trainedModel.getModelSavePath());
                Path fileName = path.getFileName();
                if (fileName != null) {
                    return fileName.toString();
                }
            }
        } catch (Exception e) {
            log.warn("解析模型目录失败，使用展示名称: {}", e.getMessage());
        }
        return trainedModel.getTrainedModelName();
    }
    
    /**
     * 获取数据集完整路径
     */
    private String getDatasetFullPath(Dataset dataset) {
        return getDatasetsBasePath() + File.separator + dataset.getFilePath();
    }

    private String getDatasetsBasePath() {
        if (StringUtils.hasText(datasetsPathOverride)) {
            return datasetsPathOverride;
        }
        return chainBasePath + File.separator + "datasets";
    }
    
    /**
     * 执行测试命令
     */
    private ModelTestResult executeTest(List<String> command, TrainedModel trainedModel, Dataset testDataset) 
            throws IOException, InterruptedException {
        
        log.info("开始执行模型测试: {}", trainedModel.getTrainedModelName());
        
        // 设置工作目录为原始模型目录
        String originalModelPath = modelStorageConfig.getModelFullPath(
            trainedModel.getOriginalModelName().replace("GPFedRec-TopkEF21", "GPFedRec-TopkEF21/")
        );
        File workingDir = new File(originalModelPath);
        
        if (!workingDir.exists()) {
            throw new RuntimeException("原始模型目录不存在: " + originalModelPath);
        }
        
        // 创建进程构建器
        ProcessBuilder processBuilder = new ProcessBuilder(command);
        processBuilder.directory(workingDir);
        processBuilder.redirectErrorStream(true);
        
        // 启动进程
        Process process = processBuilder.start();
        
        // 等待进程完成
        int exitCode = process.waitFor();
        
        // 构建测试结果
        ModelTestResult result = new ModelTestResult();
        result.setTestTime(LocalDateTime.now());
        result.setTrainedModelName(trainedModel.getTrainedModelName());
        result.setTestDatasetName(testDataset != null ? testDataset.getName() : trainedModel.getDatasetName());
        
        if (exitCode == 0) {
            result.setStatus("SUCCESS");
            // 这里需要解析测试输出或读取结果文件来获取具体的测试指标
            // 暂时设置模拟数据
            result = parseTestResults(result, trainedModel);
        } else {
            result.setStatus("FAILED");
            result.setErrorMessage("测试进程异常退出，退出码: " + exitCode);
        }
        
        return result;
    }
    
    /**
     * 解析测试结果
     * 注意：这里是简化实现，实际应该解析测试脚本的输出或结果文件
     */
    private ModelTestResult parseTestResults(ModelTestResult result, TrainedModel trainedModel) {
        // 这里应该解析实际的测试结果
        // 由于TrainedModel中没有存储具体的性能指标，我们设置模拟数据
        
        // 设置模拟的测试结果
        result.setHr10(0.0800); // 模拟HR@10指标
        result.setNdcg10(0.0450); // 模拟NDCG@10指标
        result.setTestLoss(0.85);
        
        // 设置基本的性能对比信息
        ModelTestResult.PerformanceComparison comparison = new ModelTestResult.PerformanceComparison();
        comparison.setTrainingBestHr(0.0820); // 模拟训练时的最佳HR
        comparison.setTrainingBestNdcg(0.0470); // 模拟训练时的最佳NDCG
        
        if (result.getHr10() != null) {
            comparison.setHrDifference(result.getHr10() - comparison.getTrainingBestHr());
            comparison.setHrRelativeChange(comparison.getHrDifference() / comparison.getTrainingBestHr() * 100);
        }
        
        if (result.getNdcg10() != null) {
            comparison.setNdcgDifference(result.getNdcg10() - comparison.getTrainingBestNdcg());
            comparison.setNdcgRelativeChange(comparison.getNdcgDifference() / comparison.getTrainingBestNdcg() * 100);
        }
        
        result.setPerformanceComparison(comparison);
        
        // 添加额外信息
        java.util.Map<String, Object> additionalInfo = new java.util.HashMap<>();
        additionalInfo.put("note", "测试结果基于模拟数据，实际使用时需要解析真实的测试输出");
        additionalInfo.put("trainedModelPath", trainedModel.getModelSavePath());
        additionalInfo.put("bestEpoch", trainedModel.getBestEpoch());
        result.setAdditionalInfo(additionalInfo);
        
        return result;
    }
    
    /**
     * 验证Python环境和测试脚本
     */
    public boolean validateTestEnvironment() {
        try {
            // 检查Python环境
            ProcessBuilder pb = new ProcessBuilder(pythonExecutable, "--version");
            Process process = pb.start();
            int exitCode = process.waitFor();
            
            if (exitCode != 0) {
                log.error("Python环境验证失败");
                return false;
            }
            
            // 检查测试脚本是否存在
            String testScriptPath = modelStorageConfig.getModelFullPath("GPFedRec-TopkEF21/") + 
                                   File.separator + "test_model.py";
            File testScript = new File(testScriptPath);
            
            if (!testScript.exists()) {
                log.error("测试脚本不存在: {}", testScriptPath);
                return false;
            }
            
            return true;
            
        } catch (Exception e) {
            log.error("验证测试环境失败", e);
            return false;
        }
    }
} 
