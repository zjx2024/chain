package com.example.industryriskassessmentserver.service;

import com.example.industryriskassessmentserver.dto.ModelTrainingRequest;
import com.example.industryriskassessmentserver.entity.Dataset;
import com.example.industryriskassessmentserver.entity.DictModel;
import com.example.industryriskassessmentserver.entity.ModelOptimizer;
import com.example.industryriskassessmentserver.entity.TrainingTask;
import com.example.industryriskassessmentserver.entity.TrainedModel;
import com.example.industryriskassessmentserver.config.ModelStorageConfig;
import com.example.industryriskassessmentserver.service.DatasetService;
import com.example.industryriskassessmentserver.service.ModelTrainingService;
import com.example.industryriskassessmentserver.service.TrainingTaskService;
import com.example.industryriskassessmentserver.service.TrainedModelService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.util.StringUtils;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;

@Service
public class ModelTrainingExecutionService {
    
    private static final Logger log = LoggerFactory.getLogger(ModelTrainingExecutionService.class);
    
    @Autowired
    private DatasetService datasetService;
    
    @Autowired
    private ModelTrainingService modelTrainingService;
    
    @Autowired
    private TrainingTaskService trainingTaskService;
    
    @Autowired
    private TrainedModelService trainedModelService;
    
    @Autowired
    private ModelStorageConfig modelStorageConfig;
    
    @Value("${model.training.python-env:${CHAIN_PYTHON_ENV:/usr/bin/python3}}")
    private String pythonExecutable;

    @Value("${chain.base-path:${CHAIN_BASE_PATH:/data/chain}}")
    private String chainBasePath;

    @Value("${chain.datasets-path:}")
    private String datasetsPathOverride;

    @Value("${chain.models-code-path:}")
    private String modelsCodePathOverride;
    
    /**
     * 启动模型训练
     */
    public CompletableFuture<TrainingTask> startTraining(ModelTrainingRequest request) {
        return CompletableFuture.supplyAsync(() -> {
            TrainingTask task = null;
            try {
                log.info("开始启动模型训练，请求参数: {}", request);
                
                // 1. 创建训练任务记录
                task = trainingTaskService.createTrainingTask(request);
                
                // 2. 获取数据集信息
                Dataset dataset = datasetService.getDatasetById(request.getDatasetId());
                if (dataset == null) {
                    throw new RuntimeException("数据集不存在: " + request.getDatasetId());
                }
                
                // 3. 获取模型信息
                DictModel model = modelTrainingService.getModelById(request.getModelId());
                if (model == null) {
                    throw new RuntimeException("模型不存在: " + request.getModelId());
                }
                
                // 4. 获取优化器信息
                List<ModelOptimizer> optimizers = modelTrainingService.getOptimizersByModelId(request.getModelId());
                ModelOptimizer optimizer = optimizers.stream()
                    .filter(opt -> opt.getOptimizerId().equals(request.getOptimizerId()))
                    .findFirst()
                    .orElseThrow(() -> new RuntimeException("优化器不存在: " + request.getOptimizerId()));
                
                // 5. 构建训练命令
                List<String> command = buildTrainingCommand(request, dataset, model, optimizer);
                
                // 6. 启动训练任务
                trainingTaskService.startTrainingTask(task.getId());
                
                // 7. 执行训练
                executeTraining(command, model, task);
                
                return task;
                
            } catch (Exception e) {
                log.error("模型训练启动失败", e);
                if (task != null) {
                    trainingTaskService.failTask(task.getId(), e.getMessage());
                }
                throw new RuntimeException("模型训练启动失败: " + e.getMessage());
            }
        });
    }
    
    /**
     * 构建训练命令
     */
    private List<String> buildTrainingCommand(ModelTrainingRequest request, Dataset dataset, 
                                            DictModel model, ModelOptimizer optimizer) {
        List<String> command = new ArrayList<>();
        
        // Python可执行文件路径
        command.add(pythonExecutable);
        
        // 根据模型类型选择不同的训练脚本
        String modelCodePath = getModelCodePath(model);
        String trainScriptPath;
        
        log.info("构建训练脚本，模型code: {}", model.getCode());
        if ("HAN_MODEL".equals(model.getCode())) {
            // HAN模型使用main.py
            trainScriptPath = modelCodePath + "main.py";
        } else if ("HIERTRANSFERGNN_MODEL".equals(model.getCode())) {
            // HierTransferGNN模型使用main_pure.py
            trainScriptPath = modelCodePath + "main_pure.py";
        } else if ("METAPATH2VEC".equals(model.getCode())) {
            // MetaPath2vec 使用脚本 MetaPath2vec.py，不传可变超参，按原始默认参数运行
            trainScriptPath = modelCodePath + "MetaPath2vec.py";
        } else {
            // 其他模型使用train.py
            trainScriptPath = modelCodePath + "train.py";
        }
        command.add(trainScriptPath);
        
        // 根据模型类型构建不同的参数
        if ("HAN_MODEL".equals(model.getCode())) {
            // HAN模型的参数
            String datasetPath = getDatasetFullPath(dataset);
            command.add("--feat-file");
            command.add(datasetPath);
            
            // 添加产业链类型参数
            command.add("--industry-chain-id");
            command.add(dataset.getIndustryChainId().toString());
            
            command.add("--epochs");
            command.add(request.getEpochs().toString());
            
            // 学习率（使用用户输入的或默认的）
            Double learningRate = request.getLearningRate();
            if (learningRate == null) {
                learningRate = optimizer.getDefaultLr().doubleValue();
            }
            command.add("--lr");
            command.add(learningRate.toString());
            
        } else if ("HIERTRANSFERGNN_MODEL".equals(model.getCode())) {
            // HierTransferGNN模型的参数
            String datasetPath = getDatasetFullPath(dataset);
            command.add("--feat-file");
            command.add(datasetPath);
            
            // 添加产业链类型参数
            command.add("--industry-chain-id");
            command.add(dataset.getIndustryChainId().toString());
            
            command.add("--epochs");
            command.add(request.getEpochs().toString());
            
            // 学习率（使用用户输入的或默认的）
            Double learningRate = request.getLearningRate();
            if (learningRate == null) {
                learningRate = optimizer.getDefaultLr().doubleValue();
            }
            command.add("--lr");
            command.add(learningRate.toString());
            
        } else if ("METAPATH2VEC".equals(model.getCode())) {
            // MetaPath2vec 不接收任何动态训练参数，保持脚本默认超参
            // 此分支刻意不添加额外参数
        } else {
            // GPFedRec等其他模型的参数
        String datasetPath = getDatasetFullPath(dataset);
        command.add("--dataset_path");
        command.add(datasetPath);
        
        // 基础训练参数
        command.add("--dataset");
        // 处理数据集名称映射
        String datasetName = dataset.getName().replace("_" + dataset.getDataPeriod(), "");
        command.add(datasetName);
        
        command.add("--num_round");
        command.add(request.getEpochs().toString());
        
        // 学习率（使用用户输入的或默认的）
        Double learningRate = request.getLearningRate();
        if (learningRate == null) {
            learningRate = optimizer.getDefaultLr().doubleValue();
        }
        command.add("--lr");
        command.add(learningRate.toString());
        
        // 优化器（将优化器名称转换为小写）
        command.add("--optimizer");
        command.add(optimizer.getOptimizerName().toLowerCase());
        
        // 高级参数
        command.add("--clients_sample_ratio");
        command.add(request.getClientsSampleRatio().toString());
        
        command.add("--topk_ratio");
        command.add(request.getTopkRatio().toString());
        
        command.add("--n_clusters");
        command.add(request.getNClusters().toString());
        
        command.add("--privacy_method");
        command.add(request.getPrivacyMethod());
        
        if ("differential_privacy".equals(request.getPrivacyMethod())) {
            command.add("--dp");
            command.add(request.getDp().toString());
        }
        
        // 添加模型保存路径参数 - 只传递基础路径给Python，让Python自己管理子目录
        // 获取基础存储路径，不包含模型特定的子目录
        String baseModelStoragePath = getBaseModelStoragePath();
        
        // 确保路径格式正确，将反斜杠转换为正斜杠（Python更容易处理）
        String normalizedPath = baseModelStoragePath.replace("\\", "/");
        
        // 添加调试日志
        log.info("传递给Python的基础模型保存路径: {}", normalizedPath);
        
        command.add("--model_save_path");
        command.add(normalizedPath);
        
        command.add("--save_best_model");
        command.add("true");
        
        // 启用进度输出
        command.add("--progress_output");
        command.add("true");
        }
        
        log.info("构建的训练命令: {}", String.join(" ", command));
        return command;
    }
    
    /**
     * 获取数据集完整路径
     */
    private String getDatasetFullPath(Dataset dataset) {
        return buildPath(getDatasetsBasePath(), dataset.getFilePath());
    }
    
    /**
     * 获取基础模型存储路径
     */
    private String getBaseModelStoragePath() {
        // 直接从配置中获取基础路径，不添加任何子目录
        return trainedModelService.getBaseModelStoragePath();
    }
    
    /**
     * 获取模型代码路径（在models目录下）
     */
    private String getModelCodePath(DictModel model) {
        return buildPath(getModelCodeBasePath(), model.getModelPath());
    }

    private String getDatasetsBasePath() {
        if (StringUtils.hasText(datasetsPathOverride)) {
            return datasetsPathOverride;
        }
        return chainBasePath + File.separator + "datasets";
    }

    private String getModelCodeBasePath() {
        if (StringUtils.hasText(modelsCodePathOverride)) {
            return modelsCodePathOverride;
        }
        return chainBasePath + File.separator + "models";
    }

    private String buildPath(String base, String child) {
        return base + File.separator + (child == null ? "" : child);
    }
    
    /**
     * 执行训练命令
     */
    private void executeTraining(List<String> command, DictModel model, TrainingTask task) throws IOException, InterruptedException {
        log.info("开始执行模型训练: {}", model.getName());
        
        // 设置工作目录为模型代码目录（在models目录下）
        String modelCodePath = getModelCodePath(model);
        File workingDir = new File(modelCodePath);
        
        if (!workingDir.exists()) {
            throw new RuntimeException("模型代码目录不存在: " + modelCodePath);
        }
        
        // 创建进程构建器
        ProcessBuilder processBuilder = new ProcessBuilder(command);
        processBuilder.directory(workingDir);
        processBuilder.redirectErrorStream(true); // 将错误输出重定向到标准输出
        
        // 设置环境变量，确保使用正确的conda虚拟环境
        java.util.Map<String, String> env = processBuilder.environment();
        
        log.info("Python可执行文件路径: {}", pythonExecutable);
        log.info("File.separator: {}", File.separator);
        
        // 设置Python路径环境变量
        String pythonDir;
        int lastSeparatorIndex = pythonExecutable.lastIndexOf(File.separator);
        if (lastSeparatorIndex == -1) {
            // 如果没有找到文件分隔符，尝试查找正斜杠或反斜杠
            lastSeparatorIndex = Math.max(pythonExecutable.lastIndexOf('/'), pythonExecutable.lastIndexOf('\\'));
        }
        
        if (lastSeparatorIndex > 0) {
            pythonDir = pythonExecutable.substring(0, lastSeparatorIndex);
        } else {
            pythonDir = chainBasePath;
            log.warn("无法从Python路径中提取目录，使用chain.base-path: {}", pythonDir);
        }
        
        log.info("提取的Python目录: {}", pythonDir);
        
        // Conda 虚拟环境需要 DLLs、Library/bin、Scripts 等目录才能正确加载 numpy/torch
        enhancePythonEnv(env, pythonDir);
        
        log.info("设置的环境变量:");
        log.info("PATH: {}", env.get("PATH"));
        log.info("PYTHONPATH: {}", env.get("PYTHONPATH"));
        log.info("PYTHONHOME: {}", env.get("PYTHONHOME"));
        log.info("CONDA_DEFAULT_ENV: {}", env.get("CONDA_DEFAULT_ENV"));
        log.info("CONDA_PREFIX: {}", env.get("CONDA_PREFIX"));
        log.info("CONDA_PYTHON_EXE: {}", env.get("CONDA_PYTHON_EXE"));
        log.info("工作目录: {}", workingDir.getAbsolutePath());
        
        // 启动进程
        Process process = processBuilder.start();
        
        log.info("模型训练进程已启动，任务ID: {}", task.getId());
        log.info("完整训练命令: {}", String.join(" ", command));
        
        // 异步监控训练进程并读取输出
        CompletableFuture.runAsync(() -> {
            java.nio.charset.Charset streamCharset;
            try {
                streamCharset = java.nio.charset.Charset.forName("GBK");
            } catch (Exception e) {
                streamCharset = java.nio.charset.StandardCharsets.UTF_8;
            }
            try (java.io.BufferedReader reader = new java.io.BufferedReader(
                    new java.io.InputStreamReader(process.getInputStream(), streamCharset))) {
                
                String line;
                StringBuilder fullOutput = new StringBuilder();
                while ((line = reader.readLine()) != null) {
                    log.info("[训练输出] {}", line);
                    fullOutput.append(line).append(System.lineSeparator());
                    
                    // 解析训练进度 - 根据模型类型使用不同的解析规则
                    if ("HAN Model".equals(model.getName()) && line.contains("Epoch") && line.contains("|")) {
                        // HAN模型的进度格式: "Epoch 1 |Train Acc 0.xxxx| ..."
                        try {
                            java.util.regex.Pattern pattern = java.util.regex.Pattern.compile("Epoch\\s+(\\d+)\\s+\\|");
                            java.util.regex.Matcher matcher = pattern.matcher(line);
                            if (matcher.find()) {
                                int currentEpoch = Integer.parseInt(matcher.group(1));
                                trainingTaskService.updateCurrentEpoch(task.getId(), currentEpoch);
                                log.info("更新HAN模型训练进度: 任务ID={}, 轮次={}", task.getId(), currentEpoch);
                            }
                        } catch (Exception e) {
                            log.warn("解析HAN模型训练进度失败: {}", line, e);
                        }
                    } else if ("HierTransferGNN Model".equals(model.getName()) && line.contains("Epoch") && line.contains("Train Loss")) {
                        // HierTransferGNN模型的进度格式: "Epoch 1/400: Train Loss: 0.xxxx" 或 "Epoch 10/400: Train Loss: 0.xxxx, Val Acc: 0.xxxx, F1: 0.xxxx, AUC: 0.xxxx"
                        log.info("检测到HierTransferGNN模型进度行: {}", line);
                        try {
                            java.util.regex.Pattern pattern = java.util.regex.Pattern.compile("Epoch\\s+(\\d+)/(\\d+):");
                            java.util.regex.Matcher matcher = pattern.matcher(line);
                            if (matcher.find()) {
                                int currentEpoch = Integer.parseInt(matcher.group(1));
                                trainingTaskService.updateCurrentEpoch(task.getId(), currentEpoch);
                                log.info("更新HierTransferGNN模型训练进度: 任务ID={}, 轮次={}", task.getId(), currentEpoch);
                            } else {
                                log.warn("HierTransferGNN模型进度行匹配失败: {}", line);
                            }
                        } catch (Exception e) {
                            log.warn("解析HierTransferGNN模型训练进度失败: {}", line, e);
                        }
                    } else if (line.contains("Round") && line.contains("starts")) {
                        // GPFedRec模型的进度格式: "Round 0 starts !"
                        try {
                            java.util.regex.Pattern pattern = java.util.regex.Pattern.compile("Round\\s+(\\d+)\\s+starts");
                            java.util.regex.Matcher matcher = pattern.matcher(line);
                            if (matcher.find()) {
                                int currentRound = Integer.parseInt(matcher.group(1));
                                // Python从0开始计数，我们转换为从1开始的轮次显示
                                int displayRound = currentRound + 1;
                                trainingTaskService.updateCurrentEpoch(task.getId(), displayRound);
                                log.info("更新GPFedRec模型训练进度: 任务ID={}, Python轮次={}, 显示轮次={}", task.getId(), currentRound, displayRound);
                            }
                        } catch (Exception e) {
                            log.warn("解析GPFedRec模型训练进度失败: {}", line, e);
                        }
                    }
                }
                
                int exitCode = process.waitFor();
                if (exitCode == 0) {
                    if ("METAPATH2VEC".equals(model.getCode())) {
                        // MetaPath2vec：解析评估结果三行文本，创建存储目录与日志，并保存到 TrainedModel.description
                        handleMetaPath2vecCompletion(task, model, fullOutput.toString());
                    } else {
                        // 训练完成后创建训练后模型记录
                        handleTrainingCompletion(task, model);
                    }
                    trainingTaskService.completeTask(task.getId());
                    log.info("训练任务完成，任务ID: {}", task.getId());
                } else {
                    trainingTaskService.failTask(task.getId(), "训练进程异常退出，退出码: " + exitCode);
                    log.error("训练任务失败，任务ID: {}, 退出码: {}", task.getId(), exitCode);
                }
            } catch (Exception e) {
                trainingTaskService.failTask(task.getId(), "训练进程监控异常: " + e.getMessage());
                log.error("训练进程监控异常，任务ID: {}", task.getId(), e);
            }
        });
    }

    /**
     * 为 ProcessBuilder 的环境变量补充 Conda 相关目录
     */
    private void enhancePythonEnv(java.util.Map<String, String> env, String pythonDir) {
        java.util.List<String> extraPaths = new java.util.ArrayList<>();
        extraPaths.add(pythonDir);
        extraPaths.add(pythonDir + File.separator + "Scripts");
        extraPaths.add(pythonDir + File.separator + "Library" + File.separator + "bin");
        extraPaths.add(pythonDir + File.separator + "DLLs");

        String currentPath = env.get("PATH");
        StringBuilder newPath = new StringBuilder();
        for (String p : extraPaths) {
            newPath.append(p).append(File.pathSeparator);
        }
        if (currentPath != null) {
            newPath.append(currentPath);
        }
        env.put("PATH", newPath.toString());

        env.put("PYTHONHOME", pythonDir);
        env.put("PYTHONPATH",
            pythonDir + File.separator + "Lib" + File.pathSeparator +
            pythonDir + File.separator + "Lib" + File.separator + "site-packages");
        env.put("CONDA_PREFIX", pythonDir);
        int lastSep = pythonDir.lastIndexOf(File.separator);
        if (lastSep > -1 && lastSep < pythonDir.length() - 1) {
            env.put("CONDA_DEFAULT_ENV", pythonDir.substring(lastSep + 1));
        }
    }

    /**
     * MetaPath2vec 训练完成后的特殊处理：
     * - 解析 stdout 中的评估结果三行
     * - 在 models-storage 下创建目录并写入日志
     * - 将三行评估结果写入 trained_model.description
     */
    private void handleMetaPath2vecCompletion(TrainingTask task, DictModel model, String stdout) {
        try {
            // 提取评估结果三行
            String metricsBlock = extractMetaPath2vecMetrics(stdout);
            if (metricsBlock == null || metricsBlock.trim().isEmpty()) {
                metricsBlock = "评估结果未捕获\n";
            }

            // 生成保存目录名（与现有命名风格一致）
            String timestamp = java.time.LocalDateTime.now()
                .format(java.time.format.DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            String datasetBase = task.getDatasetName();
            String lrPart = task.getLearningRate() != null ? String.format("%.3f", task.getLearningRate()) : "0.001";
            String dirName = String.format("MetaPath2vec_%s_epochs%d_lr%s_%s",
                datasetBase, task.getTotalEpochs(), lrPart, timestamp);

            String basePath = getBaseModelStoragePath();
            java.io.File saveDir = new java.io.File(basePath, dirName);
            if (!saveDir.exists()) {
                boolean ok = saveDir.mkdirs();
                if (!ok) {
                    log.warn("创建模型保存目录失败: {}", saveDir.getAbsolutePath());
                }
            }

            // 写入完整标准输出到日志文件（使用 GBK 保持一致）
            String logFileName = "stdout.txt";
            java.nio.file.Path logPath = java.nio.file.Paths.get(saveDir.getAbsolutePath(), logFileName);
            try {
                java.nio.file.Files.write(logPath, stdout.getBytes("GBK"));
            } catch (Exception e) {
                log.warn("写入MetaPath2vec日志文件失败: {}", logPath, e);
            }

            // 创建训练后模型记录
            TrainedModel trainedModel = new TrainedModel();
            String displayName = buildDisplayModelName(model, dirName);
            trainedModel.setTrainedModelName(displayName);
            trainedModel.setOriginalModelId(model.getId());
            trainedModel.setOriginalModelName(model.getName());
            trainedModel.setTrainingTaskId(task.getId());
            trainedModel.setModelSavePath(saveDir.getAbsolutePath());
            trainedModel.setLogFileName(logFileName);
            trainedModel.setTrainingEpochs(task.getTotalEpochs());
            trainedModel.setLearningRate(task.getLearningRate());
            trainedModel.setDatasetName(task.getDatasetName());
            trainedModel.setOptimizerName(task.getOptimizerName());
            trainedModel.setStatus(TrainedModel.Status.ACTIVE);
            trainedModel.setBestEpoch(task.getTotalEpochs());
            trainedModel.setDescription(metricsBlock);

            TrainedModel saved = trainedModelService.createTrainedModel(trainedModel);
            log.info("MetaPath2vec 训练后模型记录已创建，ID: {}", saved.getId());

            task.setTrainedModelName(displayName);
            task.setTrainedModelId(saved.getId());
            trainingTaskService.updateById(task);
        } catch (Exception e) {
            log.error("MetaPath2vec 训练完成处理失败，任务ID: {}", task.getId(), e);
        }
    }

    /**
     * 从 stdout 中提取评估结果三行文本
     */
    private String extractMetaPath2vecMetrics(String stdout) {
        if (stdout == null) {
            return null;
        }

        String[] lines = stdout.split("\r?\n");
        String accuracy = null;
        String f1 = null;
        String auc = null;

        java.util.regex.Pattern numberPattern = java.util.regex.Pattern.compile("[:：]\\s*([0-9]+(?:\\.[0-9]+)?)");
        java.util.regex.Pattern fallbackNumberPattern = java.util.regex.Pattern.compile("([0-9]+(?:\\.[0-9]+)?)");

        for (String raw : lines) {
            if (raw == null) {
                continue;
            }
            String t = raw.trim();
            if (t.isEmpty()) {
                continue;
            }

            java.util.regex.Matcher matcher = numberPattern.matcher(t);
            String value = null;
            if (matcher.find()) {
                value = matcher.group(1);
            } else {
                java.util.regex.Matcher fallback = fallbackNumberPattern.matcher(t);
                if (fallback.find()) {
                    value = fallback.group(1);
                } else {
                    continue;
                }
            }
            String lower = t.toLowerCase();
            if (t.contains("F1")) {
                f1 = value;
            } else if (lower.contains("auc")) {
                auc = value;
            } else if (accuracy == null &&
                      (lower.contains("accuracy") || t.contains("准确率") || t.contains("准确") || t.contains("׼ȷ") || lower.contains("acc"))) {
                accuracy = value;
            }
        }

        if (accuracy == null && f1 == null && auc == null) {
            return null;
        }

        StringBuilder block = new StringBuilder();
        block.append("评估结果:").append(System.lineSeparator());
        if (accuracy != null) {
            block.append("准确率: ").append(accuracy).append(System.lineSeparator());
        }
        if (f1 != null) {
            block.append("F1分数: ").append(f1).append(System.lineSeparator());
        }
        if (auc != null) {
            block.append("AUC值: ").append(auc).append(System.lineSeparator());
        }
        return block.toString();
    }
    
    /**
     * 生成日志文件名
     */
    private String generateLogFileName(ModelTrainingRequest request, Dataset dataset, 
                                     DictModel model, ModelOptimizer optimizer) {
        // 构建类似于GPFedRec模型中的日志文件名格式
        String timestamp = java.time.LocalDateTime.now()
            .format(java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd_HH-mm"));
        
        String datasetName = dataset.getName().replace("_" + dataset.getDataPeriod(), "");
        String privacyPart = "differential_privacy".equals(request.getPrivacyMethod()) ? 
            "differential_privacy" + request.getDp() : "no_privacy";
        
        return String.format("%s_user_clustering_%d_%s_full_topk%.1f_cumcluster10_ef21w3_client%.1f_lr%.1f_r%d_mp2_%s.txt",
            datasetName,
            request.getNClusters(),
            privacyPart,
            request.getTopkRatio(),
            request.getClientsSampleRatio(),
            request.getLearningRate() != null ? request.getLearningRate() : 
                optimizer.getDefaultLr().doubleValue(),
            request.getEpochs(),
            timestamp
        );
    }
    
    /**
     * 处理训练完成后的操作
     */
    private void handleTrainingCompletion(TrainingTask task, DictModel model) {
        try {
            log.info("开始处理训练完成后操作，任务ID: {}, 模型名称: {}", task.getId(), model.getName());
            
            // 扫描models-storage目录，找到Python实际创建的模型目录
            String actualModelPath = findActualModelPath(model.getName());
            if (actualModelPath == null) {
                log.warn("未找到实际的模型保存目录，跳过创建TrainedModel记录。模型名称: {}", model.getName());
                return;
            }
            
            // 从实际路径中提取模型名称（目录名）
            String actualModelName = new File(actualModelPath).getName();
            
            log.info("找到实际模型路径: {}", actualModelPath);
            log.info("实际模型名称: {}", actualModelName);
            
            // 创建训练后模型记录
            String displayName = buildDisplayModelName(model, actualModelName);

            TrainedModel trainedModel = new TrainedModel();
            trainedModel.setTrainedModelName(displayName);
            trainedModel.setOriginalModelId(model.getId());
            trainedModel.setOriginalModelName(model.getName());
            trainedModel.setTrainingTaskId(task.getId());
            trainedModel.setModelSavePath(actualModelPath);  // 使用实际路径
            trainedModel.setLogFileName(""); // 不需要日志文件名
            trainedModel.setTrainingEpochs(task.getTotalEpochs());
            trainedModel.setLearningRate(task.getLearningRate());
            trainedModel.setDatasetName(task.getDatasetName());
            trainedModel.setOptimizerName(task.getOptimizerName());
            trainedModel.setStatus(TrainedModel.Status.ACTIVE);
            
            // 设置最佳轮次（设置为总轮次）
            trainedModel.setBestEpoch(task.getTotalEpochs());
            
            // 保存训练后模型记录
            TrainedModel savedModel = trainedModelService.createTrainedModel(trainedModel);
            log.info("训练后模型记录已创建，ID: {}", savedModel.getId());
            
            // 更新训练任务的训练后模型信息
            task.setTrainedModelName(displayName);
            task.setTrainedModelId(savedModel.getId());
            trainingTaskService.updateById(task);
            
            log.info("训练任务已更新，训练后模型: {}", actualModelName);
            
        } catch (Exception e) {
            log.error("处理训练完成后操作失败，任务ID: {}", task.getId(), e);
            // 即使创建 TrainedModel 失败，也不影响训练任务的完成状态
        }
    }
    
    /**
     * 查找Python实际创建的模型目录
     */
    private String findActualModelPath(String modelName) {
        try {
            String baseStoragePath = getBaseModelStoragePath();
            File storageDir = new File(baseStoragePath);
            
            if (!storageDir.exists() || !storageDir.isDirectory()) {
                log.warn("模型存储目录不存在: {}", baseStoragePath);
                return null;
            }
            
            DictModel model = modelTrainingService.getModelByName(modelName);
            String searchPrefix = getModelDirectoryPrefix(model);
            if (!StringUtils.hasText(searchPrefix)) {
                searchPrefix = sanitizeDirectoryName(modelName);
            }
            final String finalSearchPrefix = searchPrefix;
            final String finalModelName = modelName;

            log.info("搜索模型目录，基础路径: {}, 搜索前缀: {}", baseStoragePath, searchPrefix);

            // 查找最新创建的以搜索前缀开头的目录
            File[] modelDirs = storageDir.listFiles(file -> 
                file.isDirectory() && 
                file.getName().startsWith(finalSearchPrefix) &&
                !file.getName().equals(finalModelName)  // 排除原始模型名目录
            );
            
            if (modelDirs == null || modelDirs.length == 0) {
                log.warn("未找到以 {} 开头的模型目录", searchPrefix);
                // 打印所有目录用于调试
                File[] allDirs = storageDir.listFiles(File::isDirectory);
                if (allDirs != null) {
                    log.info("models-storage目录中的所有子目录:");
                    for (File dir : allDirs) {
                        log.info("  - {}", dir.getName());
                    }
                }
                return null;
            }
            
            // 返回最新修改的目录
            File latestDir = modelDirs[0];
            for (File dir : modelDirs) {
                if (dir.lastModified() > latestDir.lastModified()) {
                    latestDir = dir;
                }
            }
            
            log.info("找到最新的模型目录: {}", latestDir.getAbsolutePath());
            return latestDir.getAbsolutePath();
            
        } catch (Exception e) {
            log.error("查找实际模型路径时出错", e);
            return null;
        }
    }
    
    private String getModelDisplayPrefix(DictModel model) {
        if (model != null && StringUtils.hasText(model.getDescription())) {
            return model.getDescription().trim();
        }
        return model != null && StringUtils.hasText(model.getName()) ? model.getName() : "训练模型";
    }

    private String getModelDirectoryPrefix(DictModel model) {
        if (model == null || !StringUtils.hasText(model.getName())) {
            return "";
        }
        String modelName = model.getName();
        if ("HAN Model".equals(modelName)) {
            return "HAN_Model_";
        }
        if ("HierTransferGNN Model".equals(modelName)) {
            return "HierTransferGNN_Model_";
        }
        if ("MetaPath2vec".equalsIgnoreCase(modelName) || "MetaPath2vec_Model".equalsIgnoreCase(modelName)) {
            return "MetaPath2vec_";
        }
        if ("GPFedRec-TopkEF21".equalsIgnoreCase(modelName)) {
            return "GPFedRec-TopkEF21_";
        }
        return sanitizeDirectoryName(modelName);
    }

    private String buildDisplayModelName(DictModel model, String rawName) {
        String prefix = getModelDisplayPrefix(model);
        String suffix = rawName != null ? rawName : "";
        String dirPrefix = getModelDirectoryPrefix(model);
        if (StringUtils.hasText(dirPrefix) && suffix.startsWith(dirPrefix)) {
            suffix = suffix.substring(dirPrefix.length());
        }
        if (suffix.startsWith("_")) {
            suffix = suffix.substring(1);
        }
        return StringUtils.hasText(suffix) ? prefix + "_" + suffix : prefix;
    }

    private String sanitizeDirectoryName(String input) {
        return StringUtils.hasText(input) ? input.replace("-", "_").replace(" ", "_") : "";
    }
    
    /**
     * 为已完成的训练任务生成日志文件名
     */
    private String generateLogFileNameForCompletedTask(TrainingTask task) {
        // 使用当前时间作为时间戳，避免依赖可能为空的 start_time
        String timestamp = java.time.LocalDateTime.now()
            .format(java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd_HH-mm"));
        
        // 简化的日志文件名格式
        String datasetBaseName = task.getDatasetName();
        if (datasetBaseName.contains("_")) {
            datasetBaseName = datasetBaseName.substring(0, datasetBaseName.lastIndexOf("_"));
        }
        
        return String.format("%s_task_%d_completed_%s.txt",
            datasetBaseName,
            task.getId(),
            timestamp
        );
    }
    

} 
