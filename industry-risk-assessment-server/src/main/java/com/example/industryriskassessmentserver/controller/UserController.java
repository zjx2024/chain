package com.example.industryriskassessmentserver.controller;

import com.example.industryriskassessmentserver.common.Result;
import com.example.industryriskassessmentserver.dto.LoginDTO;
import com.example.industryriskassessmentserver.entity.User;
import com.example.industryriskassessmentserver.dto.LoginResult;
import com.example.industryriskassessmentserver.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.HashMap;
import java.util.Map;
import javax.validation.Valid;

@RestController
@RequestMapping("/api/user")
public class UserController {
    private static final Logger log = LoggerFactory.getLogger(UserController.class);
    
    @Autowired
    private UserService userService;
    
    @PostMapping("/login")
    public Result<Map<String, Object>> login(@RequestBody @Valid LoginDTO loginDTO) {
        log.info("登录请求参数: {}", loginDTO);
        LoginResult loginResult = userService.login(loginDTO);

        Map<String, Object> result = new HashMap<>();
        result.put("token", loginResult.getToken());
        result.put("userInfo", loginResult.getUser());
        
        return Result.success(result);
    }
    
    @GetMapping("/info")
    public Result<User> getUserInfo(HttpServletRequest request) {
        // 从request中获取userId
        Long userId = (Long) request.getAttribute("userId");
        User user = userService.getUserInfo(userId);
        return Result.success(user);
    }
} 
