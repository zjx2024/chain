package com.example.industryriskassessmentserver.controller;

import com.example.industryriskassessmentserver.common.Result;
import com.example.industryriskassessmentserver.entity.IndustryChain;
import com.example.industryriskassessmentserver.service.IndustryChainService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/industry-chain")
public class IndustryChainController {
    @Autowired
    private IndustryChainService industryChainService;
    
    @GetMapping("/list")
    public Result<List<IndustryChain>> list() {
        return Result.success(industryChainService.list());
    }
} 