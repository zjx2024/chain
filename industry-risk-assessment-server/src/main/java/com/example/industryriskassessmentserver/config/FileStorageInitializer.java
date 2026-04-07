package com.example.industryriskassessmentserver.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.io.File;

@Component
public class FileStorageInitializer implements CommandLineRunner {
    
    private static final Logger log = LoggerFactory.getLogger(FileStorageInitializer.class);
    
    @Autowired
    private FileUploadConfig fileUploadConfig;
    
    @Override
    public void run(String... args) throws Exception {
        initializeStorageDirectory();
    }
    
    private void initializeStorageDirectory() {
        String basePath = fileUploadConfig.getBasePath();
        if (basePath == null || basePath.trim().isEmpty()) {
            log.warn("文件上传基础路径未配置");
            return;
        }
        
        File baseDir = new File(basePath);
        
        // 创建基础目录
        if (!baseDir.exists()) {
            if (baseDir.mkdirs()) {
                log.info("成功创建文件存储目录: {}", basePath);
            } else {
                log.error("创建文件存储目录失败: {}", basePath);
            }
        } else {
            log.info("文件存储目录已存在: {}", basePath);
        }
        
        // 检查目录权限
        if (!baseDir.canWrite()) {
            log.error("文件存储目录无写入权限: {}", basePath);
        }
        
        // 创建常用的子目录结构
        createSubDirectoriesIfNeeded(baseDir);
    }
    
    private void createSubDirectoriesIfNeeded(File baseDir) {
        // 可以预先创建一些子目录，比如按年份分组
        int currentYear = java.time.Year.now().getValue();
        for (int i = 0; i < 3; i++) { // 创建当前年份和未来两年的目录
            String yearPath = baseDir.getAbsolutePath() + File.separator + (currentYear + i);
            File yearDir = new File(yearPath);
            if (!yearDir.exists()) {
                yearDir.mkdirs();
                log.debug("创建年份目录: {}", yearPath);
            }
        }
    }
} 