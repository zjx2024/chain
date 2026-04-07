// 错误码枚举
export enum ErrorCode {
  SUCCESS = 200,
  PARAM_ERROR = 400,      // 参数错误
  UNAUTHORIZED = 401,     // 未授权
  FORBIDDEN = 403,        // 禁止访问
  NOT_FOUND = 404,        // 未找到
  INTERNAL_ERROR = 500,   // 服务器错误
  
  // 业务错误码
  USER_NOT_FOUND = 1001,  // 用户不存在
  PASSWORD_ERROR = 1002,  // 密码错误
  ACCOUNT_LOCKED = 1003,  // 账号被锁定
  TOKEN_EXPIRED = 1004,   // token过期
  TOKEN_INVALID = 1005,   // token无效
  REQUEST_FREQUENT = 1006 // 请求过于频繁
}

// 业务错误类
export class BusinessError extends Error {
  code: ErrorCode
  
  constructor(code: ErrorCode, message: string) {
    super(message)
    this.code = code
    this.name = 'BusinessError'
  }
} 