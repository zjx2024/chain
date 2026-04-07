import request from '@/utils/request'
import type { Dataset, DatasetQueryParams, PageResult, DictDatasetType, IndustryChain } from '@/types/dataset'

// 获取数据集列表
export function getDatasetList(params: DatasetQueryParams) {
    return request<PageResult<Dataset>>({
        url: '/api/dataset/list',
        method: 'get',
        params
    })
}

// 获取数据集详情
export function getDatasetById(id: number) {
    return request<Dataset>({
        url: `/api/dataset/${id}`,
        method: 'get'
    })
}

// 创建数据集
export function createDataset(data: Partial<Dataset>) {
    return request({
        url: '/api/dataset',
        method: 'post',
        data
    })
}

// 更新数据集
export function updateDataset(id: number, data: Partial<Dataset>) {
    return request({
        url: `/api/dataset/${id}`,
        method: 'put',
        data
    })
}

// 删除数据集
export function deleteDataset(id: number) {
    return request({
        url: `/api/dataset/${id}`,
        method: 'delete'
    })
}

// 上传数据集
export function uploadDataset(data: FormData) {
    return request({
        url: '/api/dataset/upload',
        method: 'post',
        data,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

// 获取数据集类型列表
export function getDatasetTypes() {
    return request<DictDatasetType[]>({
        url: '/api/dataset/types',
        method: 'get'
    })
}

// 获取产业链列表
export function getIndustryChains() {
    return request<IndustryChain[]>({
        url: '/api/dataset/industry-chains',
        method: 'get'
    })
}

// 获取指定产业链的数据期间列表
export function getDataPeriods(industryChainId: number) {
    return request<string[]>({
        url: `/api/dataset/periods/${industryChainId}`,
        method: 'get'
    })
} 