// 数据集基础信息接口
export interface Dataset {
    id: number
    name: string
    typeCode: string
    typeName?: string
    industryChainId: number
    industryChainName?: string
    dataPeriod: string
    filePath?: string
    fileSize?: number
    createTime: string
    updateTime: string
    createBy: number
    deleting?: boolean  // 删除中状态
}

// 查询参数接口
export interface DatasetQueryParams {
    pageNum: number
    pageSize: number
    name?: string
    typeCode?: string
    industryChainId?: number
}

// 分页响应数据接口
export interface PageResult<T> {
    records: T[]          // 数据列表
    total: number         // 总记录数
    size: number         // 每页显示条数
    current: number      // 当前页
    pages: number        // 总页数
}

// 数据集类型枚举
export enum DatasetType {
    FEATURE_LABEL = 'FEATURE_LABEL',      // 特征与标签数据
    INDUSTRY_RELATION = 'INDUSTRY_RELATION', // 产业链关系数据
    TRAIN_TEST = 'TRAIN_TEST'             // 训练测试数据
}

// 产业链类型枚举
export enum IndustryChainType {
    IC = 'IC',  // 集成电路产业链
    EI = 'EI'   // 电子信息产业链
}

// 数据集类型接口
export interface DictDatasetType {
    id: number
    code: string
    name: string
    createTime: string
}

// 产业链接口
export interface IndustryChain {
    id: number
    code: string
    name: string
    createTime: string
    updateTime: string
} 