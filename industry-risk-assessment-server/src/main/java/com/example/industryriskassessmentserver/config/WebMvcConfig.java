package com.example.industryriskassessmentserver.config;

import com.example.industryriskassessmentserver.interceptor.JwtInterceptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {
    @Autowired
    private JwtInterceptor jwtInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 目前合作方只需要公开访问产业链状态/节点风险等接口，因此暂时关闭 JWT 拦截器；
        // 如果日后恢复鉴权，可重新启用下方配置。
        // registry.addInterceptor(jwtInterceptor)
        //         .addPathPatterns("/api/**")
        //         .excludePathPatterns(
        //                 "/api/user/login",
        //                 "/api/user/register"
        //         );
    }
}
