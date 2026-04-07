package com.example.industryriskassessmentserver.dto.graph;

import lombok.Data;
import lombok.Builder;

@Data
@Builder
public class GraphLink {
    private String source;
    private String target;
    private Integer value;
} 