package com.example.industryriskassessmentserver;

import org.junit.jupiter.api.Test;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

public class PasswordEncoderTest {
    @Test
    public void generatePassword() {
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        String rawPassword = "123456";
        String encodedPassword = encoder.encode(rawPassword);
        System.out.println("原始密码: " + rawPassword);
        System.out.println("加密后的密码: " + encodedPassword);
        System.out.println("验证结果: " + encoder.matches(rawPassword, encodedPassword));
        
        // 生成SQL语句
        System.out.println("\n更新数据库的SQL:");
        System.out.println("UPDATE user SET password = '" + encodedPassword + "' WHERE username = 'admin';");
    }
} 