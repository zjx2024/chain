package com.example.industryriskassessmentserver.interceptor;

import com.example.industryriskassessmentserver.common.ErrorCode;
import com.example.industryriskassessmentserver.exception.TokenException;
import com.example.industryriskassessmentserver.utils.JwtUtil;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.SignatureException;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@Component
public class JwtInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {
            return true;
        }

        String token = request.getHeader("Authorization");
        if (!StringUtils.hasText(token)) {
            throw new TokenException(ErrorCode.UNAUTHORIZED, "未登录或token已过期");
        }

        token = token.replace("Bearer ", "").trim();

        try {
            Claims claims = JwtUtil.parseToken(token);
            request.setAttribute("userId", Long.parseLong(claims.getSubject()));
            return true;
        } catch (ExpiredJwtException e) {
            throw new TokenException(ErrorCode.TOKEN_EXPIRED, "token已过期");
        } catch (SignatureException e) {
            throw new TokenException(ErrorCode.TOKEN_INVALID, "token不合法");
        } catch (Exception e) {
            throw new TokenException(ErrorCode.UNAUTHORIZED, "token验证失败");
        }
    }
}
