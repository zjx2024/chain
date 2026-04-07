package com.example.industryriskassessmentserver.dto;

import com.example.industryriskassessmentserver.entity.User;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class LoginResult {
    private String token;
    private User user;
}
