package com.example.industryriskassessmentserver.service.impl;

import com.example.industryriskassessmentserver.entity.IndustryChain;
import com.example.industryriskassessmentserver.mapper.IndustryChainMapper;
import com.example.industryriskassessmentserver.service.IndustryChainService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class IndustryChainServiceImpl implements IndustryChainService {
    @Autowired
    private IndustryChainMapper industryChainMapper;

    @Override
    public List<IndustryChain> list() {
        return industryChainMapper.selectList(null);
    }
} 