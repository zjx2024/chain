package com.example.industryriskassessmentserver.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.example.industryriskassessmentserver.common.ErrorCode;
import com.example.industryriskassessmentserver.dto.LoginDTO;
import com.example.industryriskassessmentserver.dto.LoginResult;
import com.example.industryriskassessmentserver.entity.User;
import com.example.industryriskassessmentserver.exception.BusinessException;
import com.example.industryriskassessmentserver.mapper.UserMapper;
import com.example.industryriskassessmentserver.service.UserService;
import com.example.industryriskassessmentserver.utils.JwtUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {
    private static final Logger log = LoggerFactory.getLogger(UserServiceImpl.class);
    
    @Autowired
    private UserMapper userMapper;
    
    @Autowired
    private BCryptPasswordEncoder passwordEncoder;
    
    @Override
    public LoginResult login(LoginDTO loginDTO) {
        log.info("开始登录验证: {}", loginDTO.getUsername());
        User user = userMapper.selectOne(
            new LambdaQueryWrapper<User>()
                .eq(User::getUsername, loginDTO.getUsername())
        );
        
        if (user == null) {
            throw new BusinessException(ErrorCode.USER_NOT_FOUND.getCode(), "用户不存在");
        }
        
        // 打印密码验证信息，方便调试
        log.info("用户存在，开始验证密码");
        log.info("输入密码: {}", loginDTO.getPassword());
        log.info("数据库密码: {}", user.getPassword());
        
        boolean matches = passwordEncoder.matches(loginDTO.getPassword(), user.getPassword());
        log.info("密码验证结果: {}", matches);
        
        if (!matches) {
            log.info("密码验证失败");
            throw new BusinessException(ErrorCode.PASSWORD_ERROR.getCode(), "密码错误");
        }
        
        log.info("密码验证成功");
        String token = JwtUtil.generateToken(user.getId());
        log.info("生成token: {}", token);
        return new LoginResult(token, user);
    }
    
    @Override
    public User getUserInfo(Long userId) {
        return userMapper.selectById(userId);
    }
} 
