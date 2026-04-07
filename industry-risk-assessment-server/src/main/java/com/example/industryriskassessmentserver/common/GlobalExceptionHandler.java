package com.example.industryriskassessmentserver.common;

import com.example.industryriskassessmentserver.exception.BusinessException;
import com.example.industryriskassessmentserver.exception.TokenException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(BusinessException.class)
    public Result<String> handleBusinessException(BusinessException e) {
        log.error("业务异常: {}", e.getMessage());
        return Result.error(e.getCode(), e.getMessage());
    }

    @ExceptionHandler(Exception.class)
    public Result<String> handleException(Exception e) {
        log.error("系统异常", e);
        return Result.error(ErrorCode.INTERNAL_ERROR.getCode(), "系统错误，请稍后重试");
    }

    @ExceptionHandler(TokenException.class)
    public Result<String> handleTokenException(TokenException e) {
        log.warn("Token异常: {}", e.getMessage());
        ErrorCode errorCode = e.getErrorCode() != null ? e.getErrorCode() : ErrorCode.UNAUTHORIZED;
        return Result.error(errorCode.getCode(), e.getMessage());
    }
}
