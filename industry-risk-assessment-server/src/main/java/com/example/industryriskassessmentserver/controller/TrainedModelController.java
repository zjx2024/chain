package com.example.industryriskassessmentserver.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.industryriskassessmentserver.common.Result;
import com.example.industryriskassessmentserver.dto.ModelTestRequest;
import com.example.industryriskassessmentserver.dto.ModelTestResult;
import com.example.industryriskassessmentserver.entity.TrainedModel;
import com.example.industryriskassessmentserver.entity.TrainingTask;
import com.example.industryriskassessmentserver.entity.DictTaskType;
import com.example.industryriskassessmentserver.service.TrainedModelService;
import com.example.industryriskassessmentserver.service.ModelTestService;
import com.example.industryriskassessmentserver.service.TrainingTaskService;
import com.example.industryriskassessmentserver.service.ModelTrainingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.util.StringUtils;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/trained-models")
public class TrainedModelController {
    
    @Autowired
    private TrainedModelService trainedModelService;
    
    @Autowired
    private ModelTestService modelTestService;
    
    @Autowired
    private TrainingTaskService trainingTaskService;

    @Autowired
    private ModelTrainingService modelTrainingService;
    
    @Value("${chain.base-path:${CHAIN_BASE_PATH:/data/chain}}")
    private String chainBasePath;
    
    @Value("${model.storage.path:../models-storage}")
    private String modelStoragePath;
    
    /**
     * 分页获取可用的训练后模型
     */
    @GetMapping
    public Result<Map<String, Object>> getActiveModels(
            @RequestParam(defaultValue = "1") Integer current,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) String keyword) {
        
        Page<TrainedModel> page = new Page<>(current, size);
        IPage<TrainedModel> result = trainedModelService.getActiveModelsPage(page, keyword);
        
        Map<String, Object> data = new HashMap<>();
        data.put("records", result.getRecords());
        data.put("total", result.getTotal());
        data.put("current", result.getCurrent());
        data.put("size", result.getSize());
        data.put("pages", result.getPages());
        
        return Result.success(data);
    }
    
    /**
     * 获取所有可用的训练后模型（不分页，用于其他接口）
     */
    @GetMapping("/all")
    public Result<List<TrainedModel>> getAllActiveModels() {
        List<TrainedModel> models = trainedModelService.getActiveModels();
        return Result.success(models);
    }
    
    /**
     * 根据ID获取训练后模型详情
     */
    @GetMapping("/{id}")
    public Result<TrainedModel> getModelById(@PathVariable Long id) {
        TrainedModel model = trainedModelService.getById(id);
        if (model == null) {
            return Result.error(404, "训练后模型不存在");
        }
        refreshMetaPathMetricsIfNeeded(model);
        populateTaskTypeInfo(model);
        return Result.success(model);
    }
    
    /**
     * 获取训练过程图片列表
     */
    @GetMapping("/{id}/training-plots")
    public Result<List<Map<String, String>>> getTrainingPlots(@PathVariable Long id) {
        try {
            System.out.println("开始获取训练图片列表，模型ID: " + id);
            
            TrainedModel model = trainedModelService.getById(id);
            if (model == null) {
                System.out.println("模型不存在，ID: " + id);
                return Result.error(404, "训练后模型不存在");
            }
            
            // 构建训练图片目录路径
            String modelSavePath = model.getModelSavePath();
            System.out.println("模型保存路径: " + modelSavePath);
            
            if (modelSavePath == null || modelSavePath.isEmpty()) {
                System.out.println("模型保存路径为空");
                return Result.error(404, "该模型未保存过程数据");
            }
            
            // 规范化路径，处理Windows路径分隔符
            Path normalizedPath = resolveModelSavePath(modelSavePath);
            if (normalizedPath == null) {
                System.out.println("模型保存路径无法解析");
                return Result.error(404, "该模型未保存过程数据");
            }
            Path trainingPlotsPath = normalizedPath.resolve("training_plots");
            
            System.out.println("训练图片目录路径: " + trainingPlotsPath.toString());
            System.out.println("训练图片目录是否存在: " + Files.exists(trainingPlotsPath));
            System.out.println("训练图片目录是否为目录: " + Files.isDirectory(trainingPlotsPath));
            
            if (!Files.exists(trainingPlotsPath) || !Files.isDirectory(trainingPlotsPath)) {
                System.out.println("训练图片目录不存在或不是目录");
                return Result.error(404, "该模型未保存过程数据");
            }
            
            // 获取所有PNG图片文件
            List<Map<String, String>> plots = Files.list(trainingPlotsPath)
                    .filter(path -> path.toString().toLowerCase().endsWith(".png"))
                    .sorted((p1, p2) -> {
                        // 按文件名排序，优先显示特定类型的图片
                        String name1 = p1.getFileName().toString().toLowerCase();
                        String name2 = p2.getFileName().toString().toLowerCase();
                        
                        // 定义图片优先级
                        int priority1 = getImagePriority(name1);
                        int priority2 = getImagePriority(name2);
                        
                        if (priority1 != priority2) {
                            return Integer.compare(priority1, priority2);
                        }
                        
                        return name1.compareTo(name2);
                    })
                    .map(path -> {
                        Map<String, String> plotInfo = new HashMap<>();
                        String fileName = path.getFileName().toString();
                        plotInfo.put("filename", fileName);
                        plotInfo.put("displayName", getDisplayName(fileName));
                        plotInfo.put("url", "/api/trained-models/" + id + "/training-plots/" + fileName);
                        System.out.println("找到图片文件: " + fileName);
                        return plotInfo;
                    })
                    .collect(Collectors.toList());
            
            System.out.println("共找到 " + plots.size() + " 个图片文件");
            
            if (plots.isEmpty()) {
                System.out.println("未找到图片文件");
                return Result.error(404, "该模型未保存过程数据");
            }
            
            return Result.success(plots);
            
        } catch (IOException e) {
            System.err.println("读取训练图片失败: " + e.getMessage());
            e.printStackTrace();
            return Result.error(500, "读取训练图片失败: " + e.getMessage());
        }
    }
    
    /**
     * 获取训练过程图片文件
     */
    @GetMapping("/{id}/training-plots/{filename}")
    public ResponseEntity<Resource> getTrainingPlotImage(@PathVariable Long id, @PathVariable String filename) {
        try {
            System.out.println("开始获取训练图片，模型ID: " + id + ", 文件名: " + filename);
            
            TrainedModel model = trainedModelService.getById(id);
            if (model == null) {
                System.out.println("模型不存在，ID: " + id);
                return ResponseEntity.notFound().build();
            }
            
            String modelSavePath = model.getModelSavePath();
            System.out.println("模型保存路径: " + modelSavePath);
            
            if (modelSavePath == null || modelSavePath.isEmpty()) {
                System.out.println("模型保存路径为空");
                return ResponseEntity.notFound().build();
            }
            
            Path normalizedPath = resolveModelSavePath(modelSavePath);
            if (normalizedPath == null) {
                System.out.println("模型保存路径无法解析");
                return ResponseEntity.notFound().build();
            }
            Path imagePath = normalizedPath.resolve("training_plots").resolve(filename);
            
            System.out.println("图片完整路径: " + imagePath.toString());
            System.out.println("图片文件是否存在: " + Files.exists(imagePath));
            
            if (!Files.exists(imagePath)) {
                System.out.println("图片文件不存在: " + imagePath);
                return ResponseEntity.notFound().build();
            }
            
            if (!Files.isRegularFile(imagePath)) {
                System.out.println("不是常规文件: " + imagePath);
                return ResponseEntity.notFound().build();
            }
            
            // 安全检查：确保文件在预期目录内
            Path trainingPlotsPath = normalizedPath.resolve("training_plots");
            if (!imagePath.startsWith(trainingPlotsPath)) {
                System.out.println("安全检查失败，文件不在预期目录内");
                return ResponseEntity.badRequest().build();
            }
            
            // 检查文件是否可读
            if (!Files.isReadable(imagePath)) {
                System.out.println("文件不可读: " + imagePath);
                return ResponseEntity.status(403).build();
            }
            
            Resource resource = new UrlResource(imagePath.toUri());
            
            if (!resource.exists() || !resource.isReadable()) {
                System.out.println("资源不存在或不可读");
                return ResponseEntity.notFound().build();
            }
            
            System.out.println("成功获取图片资源");
            
            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=\"" + filename + "\"")
                    .contentType(MediaType.IMAGE_PNG)
                    .body(resource);
                    
        } catch (Exception e) {
            System.err.println("获取训练图片失败: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.internalServerError().build();
        }
    }
    
    /**
     * 获取图片显示优先级
     */
    private int getImagePriority(String filename) {
        if (filename.contains("training_curves")) {
            return 1; // 训练曲线最优先
        } else if (filename.contains("test_curves")) {
            return 2; // 测试曲线第二
        } else if (filename.contains("comparison")) {
            return 3; // 对比图第三
        } else if (filename.contains("performance")) {
            return 4; // 性能图第四
        } else {
            return 5; // 其他图片
        }
    }
    
    /**
     * 获取图片显示名称
     */
    private String getDisplayName(String filename) {
        String name = filename.toLowerCase();
        if (name.contains("training_curves")) {
            return "训练曲线";
        } else if (name.contains("test_curves")) {
            return "测试曲线";
        } else if (name.contains("train_vs_test") || name.contains("comparison")) {
            return "训练测试对比";
        } else if (name.contains("performance")) {
            return "性能对比";
        } else {
            // 去掉扩展名和时间戳，返回更友好的名称
            return filename.replaceAll("\\.(png|jpg|jpeg)$", "")
                          .replaceAll("_\\d{4}-\\d{2}-\\d{2}_\\d{2}-\\d{2}-\\d{2}", "")
                          .replaceAll("_", " ");
        }
    }

    /**
     * 从 stdout 中提取 MetaPath2vec 的评估结果三行
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
            System.out.println("[DEBUG] 处理行: " + t);
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
            boolean captured = false;
            if (t.contains("F1")) {
                f1 = value;
                captured = true;
                System.out.println("[DEBUG] 捕获F1: " + value);
            } else if (lower.contains("auc")) {
                auc = value;
                captured = true;
                System.out.println("[DEBUG] 捕获AUC: " + value);
            } else if (accuracy == null &&
                      (lower.contains("accuracy") || t.contains("准确率") || t.contains("准确") || t.contains("׼ȷ") || lower.contains("acc"))) {
                accuracy = value;
                captured = true;
                System.out.println("[DEBUG] 捕获准确率: " + value);
            }
        }

        if (accuracy == null && f1 == null && auc == null) {
            System.out.println("[DEBUG] 未捕获到任何指标");
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

        String result = block.toString();
        System.out.println("[DEBUG] 最终提取结果: " + result);
        return result;
    }

    /**
     * 当 MetaPath2vec 模型 description 缺失或准确率异常时，重新从 stdout.txt 解析指标
     */
    private void refreshMetaPathMetricsIfNeeded(TrainedModel model) {
        if (!"MetaPath2vec".equals(model.getOriginalModelName())) {
            return;
        }
        boolean needRefresh = false;
        String desc = model.getDescription();
        if (desc == null || desc.trim().isEmpty() || !desc.contains("准确率")) {
            needRefresh = true;
        } else {
            java.util.regex.Matcher matcher =
                    java.util.regex.Pattern.compile("准确率[:：]\\s*([0-9]+(?:\\.[0-9]+)?)")
                            .matcher(desc);
            if (matcher.find()) {
                try {
                    double value = Double.parseDouble(matcher.group(1));
                    if (value >= 1d) {
                        needRefresh = true;
                    }
                } catch (NumberFormatException ignore) {
                }
            }
        }
        if (!needRefresh) {
            return;
        }
        String savePath = model.getModelSavePath();
        if (savePath == null || savePath.isEmpty()) {
            return;
        }
        Path normalized = resolveModelSavePath(savePath);
        if (normalized == null) {
            return;
        }
        Path stdoutPath = normalized.resolve("stdout.txt");
        if (!Files.exists(stdoutPath) || !Files.isRegularFile(stdoutPath)) {
            return;
        }
        String metrics = null;
        // UTF-8
        try {
            String stdout = new String(Files.readAllBytes(stdoutPath), StandardCharsets.UTF_8);
            metrics = extractMetaPath2vecMetrics(stdout);
        } catch (Exception e) {
            System.out.println("[WARN] 重新解析 stdout 失败: " + e.getMessage());
        }
        // fallback GBK
        if (metrics == null || metrics.trim().isEmpty()) {
            try {
                String stdout = new String(Files.readAllBytes(stdoutPath), "GBK");
                metrics = extractMetaPath2vecMetrics(stdout);
            } catch (Exception ignored) {
            }
        }
        if (metrics != null && !metrics.trim().isEmpty()) {
            model.setDescription(metrics);
            try {
                trainedModelService.updateById(model);
            } catch (Exception ignored) {
            }
        }
    }

    private void populateTaskTypeInfo(TrainedModel model) {
        if (model.getTrainingTaskId() == null) {
            return;
        }
        TrainingTask task = trainingTaskService.getById(model.getTrainingTaskId());
        if (task == null) {
            return;
        }
        model.setTaskTypeId(task.getTaskTypeId());
        model.setTaskTypeName(task.getTaskTypeName());
        if (task.getTaskTypeId() != null) {
            DictTaskType type = modelTrainingService.getTaskTypeById(task.getTaskTypeId());
            if (type != null) {
                model.setTaskTypeCode(type.getCode());
                if (model.getTaskTypeName() == null || model.getTaskTypeName().trim().isEmpty()) {
                    model.setTaskTypeName(type.getName());
                }
            }
        }
    }

    /**
     * 根据训练任务ID获取训练后模型
     */
    @GetMapping("/by-training-task/{taskId}")
    public Result<TrainedModel> getModelByTrainingTaskId(@PathVariable Long taskId) {
        TrainedModel model = trainedModelService.getByTrainingTaskId(taskId);
        if (model == null) {
            return Result.error(404, "该训练任务暂无训练后模型");
        }
        return Result.success(model);
    }
    
    /**
     * 根据模型名称获取训练后模型
     */
    @GetMapping("/by-name/{modelName}")
    public Result<TrainedModel> getModelByName(@PathVariable String modelName) {
        TrainedModel model = trainedModelService.getByTrainedModelName(modelName);
        if (model == null) {
            return Result.error(404, "训练后模型不存在");
        }
        return Result.success(model);
    }
    
    /**
     * 归档模型
     */
    @PutMapping("/{id}/archive")
    public Result<String> archiveModel(@PathVariable Long id) {
        boolean success = trainedModelService.archiveModel(id);
        if (success) {
            return Result.success("模型已归档");
        } else {
            return Result.error(500, "归档失败");
        }
    }
    
    /**
     * 删除模型
     */
    @DeleteMapping("/{id}")
    public Result<String> deleteModel(@PathVariable Long id) {
        boolean success = trainedModelService.deleteModel(id);
        if (success) {
            return Result.success("模型已删除");
        } else {
            return Result.error(500, "删除失败");
        }
    }
    
    /**
     * 测试训练后模型
     */
    @PostMapping("/test")
    public Result<ModelTestResult> testModel(@RequestBody ModelTestRequest request) {
        try {
            ModelTestResult result = modelTestService.testModel(request);
            return Result.success(result);
        } catch (Exception e) {
            return Result.error(500, "模型测试失败: " + e.getMessage());
        }
    }
    
    /**
     * 异步测试训练后模型
     */
    @PostMapping("/test-async")
    public Result<String> testModelAsync(@RequestBody ModelTestRequest request) {
        try {
            CompletableFuture<ModelTestResult> future = modelTestService.testModelAsync(request);
            // 这里可以返回任务ID，让前端轮询结果
            return Result.success("模型测试已启动，请稍后查看结果");
        } catch (Exception e) {
            return Result.error(500, "启动模型测试失败: " + e.getMessage());
        }
    }
    
    /**
     * 验证测试环境
     */
    @GetMapping("/test/validate-environment")
    public Result<Boolean> validateTestEnvironment() {
        boolean isValid = modelTestService.validateTestEnvironment();
        if (isValid) {
            return Result.success(true);
        } else {
            return Result.error(500, "测试环境验证失败");
        }
    }
    
    /**
     * 临时方法：为已完成但缺少trained_model记录的任务创建记录
     */
    @PostMapping("/fix-missing-records")
    public Result<String> fixMissingRecords() {
        try {
            int fixedCount = trainedModelService.fixMissingTrainedModelRecords();
            return Result.success("已修复 " + fixedCount + " 个缺失的训练模型记录");
        } catch (Exception e) {
            return Result.error(500, "修复失败: " + e.getMessage());
        }
    }
    
    /**
     * 测试方法：验证模型保存路径生成
     */
    @GetMapping("/test-path-generation")
    public Result<String> testPathGeneration() {
        try {
            String logFileName = "ml-100k_task_test_completed_2025-06-25_14-30.txt";
            String modelName = "GPFedRec-TopkEF21";
            
            String trainedModelName = trainedModelService.generateTrainedModelName(modelName, logFileName);
            String modelSavePath = trainedModelService.generateModelSavePath(modelName, logFileName);
            
            String result = String.format("测试路径生成:\n" +
                    "模型名称: %s\n" +
                    "日志文件名: %s\n" +
                    "训练后模型名称: %s\n" +
                    "模型保存路径: %s", 
                    modelName, logFileName, trainedModelName, modelSavePath);
            
            return Result.success(result);
        } catch (Exception e) {
            return Result.error(500, "测试失败: " + e.getMessage());
        }
    }

    private Path resolveModelSavePath(String rawPath) {
        if (!StringUtils.hasText(rawPath)) {
            return null;
        }
        String normalized = rawPath.replace("\\", "/");
        if (normalized.matches("^[A-Za-z]:/.*")) {
            int idx = normalized.indexOf(':');
            normalized = normalized.substring(idx + 1);
            if (!normalized.startsWith("/")) {
                normalized = "/" + normalized;
            }
        }
        String windowsRoot = "/projects/chain";
        if (normalized.startsWith(windowsRoot)) {
            normalized = chainBasePath + normalized.substring(windowsRoot.length());
        }
        Path path = Paths.get(normalized).normalize();
        if (!path.isAbsolute()) {
            path = Paths.get(chainBasePath).resolve(path).normalize();
        }
        return path;
    }
}
