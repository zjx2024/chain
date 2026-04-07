package com.example.industryriskassessmentserver.dto.graph;

import lombok.Data;
import lombok.Builder;

@Data
@Builder
public class GraphNode {
    private String id;
    private String name;
    private String category;
    private Integer symbolSize;
}
