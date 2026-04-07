package com.example.industryriskassessmentserver.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

import javax.annotation.PostConstruct;

@Configuration
@ConfigurationProperties(prefix = "model.storage")
@Component
public class ModelStorageConfig {
    
    private String basePath;
    
    @Value("${chain.base-path:${CHAIN_BASE_PATH:/data/chain}}")
    private String chainBasePath;
    
    @PostConstruct
    public void init() {
        if (!StringUtils.hasText(basePath)) {
            basePath = chainBasePath + "/models-storage";
        }
    }
    
    // getter 和 setter
    public String getBasePath() {
        return basePath;
    }
    
    public void setBasePath(String basePath) {
        this.basePath = basePath;
    }
    
    
    
    /**
     * 获取模型的完整存储路径
     */
    public String getModelFullPath(String modelPath) {
        if (modelPath == null || modelPath.isEmpty()) {
            return null;
        }
        return basePath + "/" + modelPath;
    }
    
    /**
     * 生成模型存储路径
     */
    public String generateModelPath(String modelCode) {
        return modelCode + "/";
    }
} 
