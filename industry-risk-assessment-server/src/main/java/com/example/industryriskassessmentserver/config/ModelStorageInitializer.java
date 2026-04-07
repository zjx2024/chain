package com.example.industryriskassessmentserver.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.io.File;

@Component
@Order(2) // 在文件存储初始化器之后执行
public class ModelStorageInitializer implements CommandLineRunner {
    
    private static final Logger log = LoggerFactory.getLogger(ModelStorageInitializer.class);
    
    @Autowired
    private ModelStorageConfig modelStorageConfig;
    
    @Override
    public void run(String... args) throws Exception {
        initializeModelStorageDirectories();
    }
    
    private void initializeModelStorageDirectories() {
        // 初始化模型存储目录
        createDirectoryIfNotExists(modelStorageConfig.getBasePath(), "模型存储");
        
        // 不再自动创建模型子目录，按需创建
    }
    
    private void createDirectoryIfNotExists(String path, String description) {
        if (path == null || path.trim().isEmpty()) {
            log.warn("{}目录路径未配置", description);
            return;
        }
        
        File dir = new File(path);
        
        if (!dir.exists()) {
            if (dir.mkdirs()) {
                log.info("成功创建{}目录: {}", description, path);
            } else {
                log.error("创建{}目录失败: {}", description, path);
            }
        } else {
            log.info("{}目录已存在: {}", description, path);
        }
        
        // 检查目录权限
        if (!dir.canWrite()) {
            log.error("{}目录无写入权限: {}", description, path);
        }
    }
    

} 