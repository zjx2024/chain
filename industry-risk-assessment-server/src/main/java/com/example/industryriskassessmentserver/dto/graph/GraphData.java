package com.example.industryriskassessmentserver.dto.graph;

import lombok.Data;
import java.util.List;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
public class GraphData {
    private List<GraphNode> nodes;
    private List<GraphLink> links;
    private List<Category> categories;

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Category {
        private String name;
    }
} 