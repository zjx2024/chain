package com.example.industryriskassessmentserver.exception;

import com.example.industryriskassessmentserver.common.ErrorCode;

public class TokenException extends RuntimeException {
    private final ErrorCode errorCode;

    public TokenException(ErrorCode errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }

    public ErrorCode getErrorCode() {
        return errorCode;
    }
}
