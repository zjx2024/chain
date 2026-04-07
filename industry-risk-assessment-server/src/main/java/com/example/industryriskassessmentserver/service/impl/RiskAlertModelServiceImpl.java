package com.example.industryriskassessmentserver.service.impl;

import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.baomidou.mybatisplus.core.toolkit.StringUtils;
import com.example.industryriskassessmentserver.config.BailianProperties;
import com.example.industryriskassessmentserver.service.RiskAlertModelService;
import com.example.industryriskassessmentserver.vo.NodeRiskAlertVO;
import com.example.industryriskassessmentserver.vo.RiskFactorVO;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@Service
@Slf4j
public class RiskAlertModelServiceImpl implements RiskAlertModelService {

    private static final DateTimeFormatter DATE_TIME_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private static final int DEFAULT_FACTOR_LIMIT = 4;
    private static final Map<String, String> FACTOR_THRESHOLD_GUIDE;

    static {
        Map<String, String> map = new LinkedHashMap<>();
        map.put("每股营业收入 [单位]元", "低于2判为隐患，2-8为注意，≥8为健康。");
        map.put("净资产收益率ROE(平均) [单位]%", "ROE<0为红色，0-8%为黄色，≥8%为绿色。");
        map.put("销售净利率 [单位]%", "净利率<0红色，0-8%黄色，≥8%绿色。");
        map.put("资产负债率 [单位]%", "20%-60%为健康区，≤75%为注意，其他区间视为高风险。");
        map.put("流动比率", "<1红色，1-1.5黄色，≥1.5绿色。");
        map.put("速动比率", "<0.6红色，0.6-1黄色，≥1绿色。");
        map.put("现金比率", "<0.15红色，0.15-0.35黄色，≥0.35绿色。");
        map.put("净资产负债率", "≤0.7绿色，0.7-1.2黄色，>1.2红色。");
        map.put("经营活动产生的现金流量净额/负债合计", "<0红色，0-0.2黄色，≥0.2绿色。");
        map.put("存货周转率 [单位]次", "<1.5红色，1.5-3黄色，≥3绿色。");
        map.put("应收账款周转率(不含应收票据) [单位]次", "<2红色，2-5黄色，≥5绿色。");
        map.put("流动资产周转率 [单位]次", "<0.7红色，0.7-1.1黄色，≥1.1绿色。");
        map.put("非流动资产周转率 [单位]%", "<30%红色，30%-80%黄色，≥80%绿色。");
        map.put("总资产周转率 [单位]次", "<0.3红色，0.3-0.6黄色，≥0.6绿色。");
        map.put("营业收入同比增长率 [单位]%", "<0红色，0-5%黄色，≥5%绿色。");
        map.put("总资产同比增长率 [单位]%", "<0红色，0-8%黄色，≥8%绿色。");
        map.put("每股净资产相对年初增长率 [单位]%", "<0红色，0-8%黄色，≥8%绿色。");
        map.put("总资产净利率-不含少数股东损益 [单位]%", "<0红色，0-5%黄色，≥5%绿色。");
        FACTOR_THRESHOLD_GUIDE = Collections.unmodifiableMap(map);
    }

    private final BailianProperties bailianProperties;
    private final ObjectMapper objectMapper;
    private final Generation generation = new Generation();

    public RiskAlertModelServiceImpl(BailianProperties bailianProperties, ObjectMapper objectMapper) {
        this.bailianProperties = bailianProperties;
        this.objectMapper = objectMapper;
    }

    @Override
    public NodeRiskAlertVO analyze(String companyName, String period, boolean hasRisk, String alertLevel, List<RiskFactorVO> factors) {
        if (!bailianProperties.isEnabled() || StringUtils.isBlank(bailianProperties.getApiKey())) {
            log.warn("智能分析未启用或配置缺失，enabled={}, apiKeyEmpty={}",
                    bailianProperties.isEnabled(),
                    StringUtils.isBlank(bailianProperties.getApiKey()));
            return buildFallback(companyName, period, hasRisk, alertLevel, factors, "智能分析未启用");
        }
        try {
            String systemPrompt = buildSystemPrompt();
            String userPrompt = buildUserPrompt(companyName, alertLevel, factors);
            GenerationParam param = GenerationParam.builder()
                    .apiKey(bailianProperties.getApiKey())
                    .model(bailianProperties.getModel())
                    .messages(Arrays.asList(
                            Message.builder().role(Role.SYSTEM.getValue()).content(systemPrompt).build(),
                            Message.builder().role(Role.USER.getValue()).content(userPrompt).build()
                    ))
                    .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                    .build();
            GenerationResult result = generation.call(param);
            String content = result.getOutput()
                    .getChoices()
                    .get(0)
                    .getMessage()
                    .getContent();
            NodeRiskAlertVO alertVO = objectMapper.readValue(content, NodeRiskAlertVO.class);
            enrichAlert(alertVO, companyName, period, hasRisk, alertLevel, factors);
            alertVO.setPeriod("T+1期");
            if (StringUtils.isBlank(alertVO.getModelName())) {
                alertVO.setModelName(bailianProperties.getModel());
            }
            return alertVO;
        } catch (Exception ex) {
            log.error("调用百炼模型生成节点风险告警失败", ex);
            return buildFallback(companyName, period, hasRisk, alertLevel, factors, "暂无法获取模型分析，请稍后再试");
        }
    }

    private String buildSystemPrompt() {
        return "你是一名资深金融风险分析师。系统提供某公司 T+1 期的 18 个财务指标（包含名称、数值、阈值提示）。"
                + "阈值只作为单项参考，需要结合多项指标的协同或抵消关系，解释系统给出的风险等级为何合理，并给出缓释建议。"
                + "输出 JSON，字段包含 companyName、period、alertLevel、keyFactors、suggestions。"
                + "keyFactors 数组长度 2~5，每项包含 name/value/impact，name 必须与输入完全一致。"
                + "建议 2~4 条，可包含具体指标改进目标。如果发现缺失值需要说明。";
    }

    private String buildUserPrompt(String companyName, String alertLevel, List<RiskFactorVO> factors) {
        String factorsJson = buildFactorsJson(factors);
        return new StringBuilder()
                .append("公司名称：").append(companyName).append("\n")
                .append("T+1 期：T+1期\n")
                .append("系统风险等级：").append(alertLevel).append("\n")
                .append("风险指标 JSON：").append(factorsJson).append("\n")
                .append("请根据以上信息直接返回 JSON。")
                .toString();
    }

    private String buildFactorsJson(List<RiskFactorVO> factors) {
        if (factors == null || factors.isEmpty()) {
            return "[]";
        }
        List<Map<String, Object>> list = factors.stream().map(item -> {
            Map<String, Object> map = new LinkedHashMap<>();
            map.put("index", item.getIndex());
            map.put("name", item.getName());
            map.put("value", item.getValue());
            map.put("threshold", FACTOR_THRESHOLD_GUIDE.getOrDefault(item.getName(), ""));
            return map;
        }).collect(Collectors.toList());
        try {
            return objectMapper.writeValueAsString(list);
        } catch (Exception ex) {
            log.warn("构建因素JSON失败，使用回退格式。", ex);
            return list.toString();
        }
    }

    private void enrichAlert(NodeRiskAlertVO alertVO,
                             String companyName,
                             String period,
                             boolean hasRisk,
                             String alertLevel,
                             List<RiskFactorVO> factors) {
        if (StringUtils.isBlank(alertVO.getCompanyName())) {
            alertVO.setCompanyName(companyName);
        }
        if (StringUtils.isBlank(alertVO.getPeriod())) {
            alertVO.setPeriod(period);
        }
        if (StringUtils.isBlank(alertVO.getAlertLevel())) {
            if (StringUtils.isNotBlank(alertLevel)) {
                alertVO.setAlertLevel(alertLevel);
            } else {
                alertVO.setAlertLevel(hasRisk ? "HIGH" : "LOW");
            }
        } else {
            alertVO.setAlertLevel(alertVO.getAlertLevel().toUpperCase());
        }
        if (alertVO.getGeneratedAt() == null) {
            alertVO.setGeneratedAt(DATE_TIME_FORMATTER.format(LocalDateTime.now()));
        }
        if (alertVO.getKeyFactors() == null || alertVO.getKeyFactors().isEmpty()) {
            alertVO.setKeyFactors(buildKeyFactors(factors));
        }
        if (alertVO.getSuggestions() == null || alertVO.getSuggestions().isEmpty()) {
            alertVO.setSuggestions(buildDefaultSuggestions(hasRisk));
        }
    }

    private NodeRiskAlertVO buildFallback(String companyName,
                                          String period,
                                          boolean hasRisk,
                                          String alertLevel,
                                          List<RiskFactorVO> factors,
                                          String reason) {
        log.warn("返回智能分析兜底结果，company={}, reason={}, alertLevel={}, hasRisk={}",
                companyName, reason, alertLevel, hasRisk);
        NodeRiskAlertVO vo = new NodeRiskAlertVO();
        vo.setCompanyName(companyName);
        vo.setPeriod("T+1期");
        if (StringUtils.isNotBlank(alertLevel)) {
            vo.setAlertLevel(alertLevel);
        } else {
            vo.setAlertLevel(hasRisk ? "HIGH" : "MEDIUM");
        }
        vo.setKeyFactors(buildKeyFactors(factors));
        vo.setSuggestions(buildDefaultSuggestions(hasRisk));
        vo.setGeneratedAt(DATE_TIME_FORMATTER.format(LocalDateTime.now()));
        vo.setModelName("fallback");
        vo.setRemark(reason);
        return vo;
    }

    private List<NodeRiskAlertVO.KeyFactor> buildKeyFactors(List<RiskFactorVO> factors) {
        if (factors == null || factors.isEmpty()) {
            return Collections.emptyList();
        }
        return factors.stream()
                .filter(item -> item.getValue() != null)
                .sorted((a, b) -> Double.compare(Math.abs(b.getValue()), Math.abs(a.getValue())))
                .limit(DEFAULT_FACTOR_LIMIT)
                .map(item -> {
                    NodeRiskAlertVO.KeyFactor keyFactor = new NodeRiskAlertVO.KeyFactor();
                    keyFactor.setName(item.getName());
                    keyFactor.setValue(item.getValue());
                    String guide = FACTOR_THRESHOLD_GUIDE.get(item.getName());
                    if (StringUtils.isNotBlank(guide)) {
                        keyFactor.setImpact(String.format("%s 当前值 %.2f。阈值参考：%s", item.getName(), item.getValue(), guide));
                    } else {
                        keyFactor.setImpact(String.format("%s 指标值为 %.2f，需保持关注。", item.getName(), item.getValue()));
                    }
                    return keyFactor;
                })
                .collect(Collectors.toList());
    }

    private List<String> buildDefaultSuggestions(boolean hasRisk) {
        List<String> suggestions = new ArrayList<>();
        if (hasRisk) {
            suggestions.add("请立刻复核 T+1 期关键财务指标，关注现金流与资产质量变化。");
            suggestions.add("结合业务团队意见制定风险化解计划，并在系统内更新跟进记录。");
        } else {
            suggestions.add("继续保持指标在合理区间，必要时设置阈值监控确保波动可控。");
        }
        suggestions.add("如指标异常持续，请在 24 小时内启动人工二次审核流程。");
        return suggestions;
    }
}
