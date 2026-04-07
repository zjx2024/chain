package com.example.industryriskassessmentserver.service;

import com.example.industryriskassessmentserver.dto.LoginDTO;
import com.example.industryriskassessmentserver.entity.User;
import com.example.industryriskassessmentserver.dto.LoginResult;

public interface UserService {
    LoginResult login(LoginDTO loginDTO);
    User getUserInfo(Long userId);
} 
