package com.example.industryriskassessmentserver.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties(prefix = "bailian")
public class BailianProperties {
    /**
     * 是否启用百炼大模型调用
     */
    private boolean enabled = false;

    /**
     * 应用基础地址，例如：https://dashscope.aliyuncs.com/api/v1/apps
     */
    private String apiUrl = "https://dashscope.aliyuncs.com/api/v1/apps";

    /**
     * 百炼应用 ID
     */
    private String appId;

    /**
     * 百炼 API Key
     */
    private String apiKey;

    /**
     * 请求模式，默认 blocking
     */
    private String responseMode = "blocking";

    /**
     * 使用的模型名称，例如 qwen-plus
     */
    private String model = "qwen-plus";

    /**
     * 连接/读取超时时间，毫秒
     */
    private int connectTimeout = 5000;
    private int readTimeout = 15000;
}
