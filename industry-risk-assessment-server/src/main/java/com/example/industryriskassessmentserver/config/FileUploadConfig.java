package com.example.industryriskassessmentserver.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;

@Configuration
@ConfigurationProperties(prefix = "file.upload")
@Component
public class FileUploadConfig {
    private String basePath;  // 基础存储路径
    private long maxSize;     // 最大文件大小
    
    // getter 和 setter
    public String getBasePath() {
        return basePath;
    }
    
    public void setBasePath(String basePath) {
        this.basePath = basePath;
    }
    
    public long getMaxSize() {
        return maxSize;
    }
    
    public void setMaxSize(long maxSize) {
        this.maxSize = maxSize;
    }
}