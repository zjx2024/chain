<template>
  <div class="data-upload-container">
    <el-card class="upload-card">
      <template #header>
        <div class="card-header">
          <h3>上传数据集</h3>
        </div>
      </template>

      <el-form
        ref="uploadFormRef"
        :model="uploadForm"
        :rules="uploadRules"
        label-width="100px"
      >
        <!-- 基本信息部分 -->
        <div class="form-section">
          <h4>基本信息</h4>
          <el-form-item label="数据集名称" prop="name">
            <el-input
              v-model="uploadForm.name"
              placeholder="请输入数据集名称"
              style="width: 360px"
            />
          </el-form-item>

          <el-form-item label="数据集类型" prop="typeCode">
            <el-select
              v-model="uploadForm.typeCode"
              placeholder="请选择数据集类型"
              style="width: 360px"
            >
              <el-option
                v-for="item in datasetTypes"
                :key="item.code"
                :label="item.name"
                :value="item.code"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="产业链" prop="industryChainId">
            <el-select
              v-model="uploadForm.industryChainId"
              placeholder="请选择产业链"
              style="width: 360px"
            >
              <el-option
                v-for="item in industryChains"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="数据期间" prop="dataPeriod">
            <div class="period-select">
              <el-select
                v-model="year"
                placeholder="选择年份"
                style="width: 120px"
                @change="updateDataPeriod"
              >
                <el-option
                  v-for="year in years"
                  :key="year"
                  :label="year"
                  :value="year"
                />
              </el-select>
              <el-select
                v-model="quarter"
                placeholder="选择季度"
                style="width: 120px"
                @change="updateDataPeriod"
              >
                <el-option
                  v-for="q in quarters"
                  :key="q.value"
                  :label="q.label"
                  :value="q.value"
                />
              </el-select>
            </div>
          </el-form-item>
        </div>

        <!-- 文件上传部分 -->
        <div class="form-section">
          <h4>文件上传</h4>
          <el-form-item label="数据文件" prop="file">
            <el-upload
              ref="uploadRef"
              class="upload-demo"
              drag
              action="#"
              :auto-upload="false"
              :on-change="handleFileChange"
              :on-remove="handleFileRemove"
              :before-upload="beforeUpload"
              accept=".xls,.xlsx,.dat"
              :limit="1"
              :http-request="customUpload"
            >
              <el-icon class="el-icon--upload"><Upload /></el-icon>
              <div class="el-upload__text">
                将文件拖到此处，或 <em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持上传 xls/xlsx/dat 格式文件，且文件大小不超过 50MB
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </div>

        <!-- 表单操作按钮 -->
        <div class="form-actions">
          <el-button type="primary" @click="handleSubmit" :loading="uploading">
            提交
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </div>
      </el-form>
    </el-card>

    <!-- 添加进度条 -->
    <el-progress 
      v-if="uploadProgress > 0" 
      :percentage="uploadProgress"
      :format="progressFormat"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { FormInstance, UploadInstance } from 'element-plus'
import { ElMessage } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { uploadDataset, getDatasetTypes, getIndustryChains } from '../../api/dataset'
import type { DictDatasetType, IndustryChain } from '@/types/dataset'

const router = useRouter()

// 表单引用
const uploadFormRef = ref<FormInstance>()
const uploadRef = ref<UploadInstance>()

// 上传状态
const uploading = ref(false)
const uploadProgress = ref(0)

// 上传表单数据
const uploadForm = ref({
  name: '',
  typeCode: '',
  industryChainId: null as number | null,
  dataPeriod: '',
  file: null as File | null
})

// 数据集类型选项
const datasetTypes = ref<DictDatasetType[]>([])
const industryChains = ref<IndustryChain[]>([])

// 获取选项数据
const fetchOptions = async () => {
    try {
        const [typesRes, chainsRes] = await Promise.all([
            getDatasetTypes(),
            getIndustryChains()
        ])
        datasetTypes.value = typesRes.data
        industryChains.value = chainsRes.data
    } catch (error) {
        console.error('获取选项数据失败:', error)
        ElMessage.error('获取选项数据失败')
    }
}

// 组件挂载时获取选项数据
onMounted(() => {
    fetchOptions()
})

// 年份选项（从10年前到当前年份）
const currentYear = new Date().getFullYear()
const years = Array.from(
  { length: 11 }, // 11年（包括当前年份）
  (_, i) => currentYear - 10 + i // 从10年前开始
).sort((a, b) => b - a) // 降序排列，最新年份在前

// 季度选项
const quarters = [
  { value: 'Q1', label: '第一季度' },
  { value: 'Q2', label: '第二季度' },
  { value: 'Q3', label: '第三季度' },
  { value: 'Q4', label: '第四季度' }
]

const year = ref(currentYear)
const quarter = ref('')

// 更新数据期间
const updateDataPeriod = () => {
  if (year.value && quarter.value) {
    uploadForm.value.dataPeriod = `${year.value}${quarter.value}`
  }
}

// 表单验证规则
const uploadRules = {
  name: [
    { required: true, message: '请输入数据集名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符之间', trigger: 'blur' }
  ],
  typeCode: [
    { required: true, message: '请选择数据集类型', trigger: 'change' }
  ],
  industryChainId: [
    { required: true, message: '请选择产业链', trigger: 'change' }
  ],
  file: [
    { required: true, message: '请上传数据文件', trigger: 'change' }
  ]
}

// 文件改变事件
const handleFileChange = (file: any) => {
  uploadForm.value.file = file.raw
}

// 文件移除事件
const handleFileRemove = () => {
  uploadForm.value.file = null
}

const progressFormat = (percentage: number) => {
    if (percentage === 100) {
        return '上传完成'
    }
    return `${percentage}%`
}

// 上传前校验
const beforeUpload = (file: File) => {
  const maxSize = 50 * 1024 * 1024 // 50MB
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过 50MB')
    return false
  }
  
  // 验证文件格式
  const fileName = file.name.toLowerCase()
  const validExtensions = ['.xls', '.xlsx', '.dat']
  const isValidType = validExtensions.some(ext => fileName.endsWith(ext))
  
  if (!isValidType) {
    ElMessage.error('只支持上传 xls、xlsx、dat 格式的文件')
    return false
  }
  
  return true
}

// 自定义上传方法
const customUpload = async (options: any) => {
    try {
        const formData = new FormData()
        formData.append('file', options.file)
        formData.append('name', uploadForm.value.name)
        formData.append('typeCode', uploadForm.value.typeCode)
        formData.append('industryChainId', uploadForm.value.industryChainId!.toString())
        formData.append('dataPeriod', uploadForm.value.dataPeriod)
        
        await uploadDataset(formData)
        
        ElMessage.success('上传成功')
        router.push('/data/edit')
    } catch (error) {
        console.error('上传失败:', error)
        ElMessage.error('上传失败')
    }
}

// 提交表单
const handleSubmit = async () => {
    if (!uploadFormRef.value) return
    
    try {
        await uploadFormRef.value.validate()
        
        if (!uploadForm.value.file) {
            ElMessage.error('请选择要上传的文件')
            return
        }
        
        uploading.value = true
        
        // 构建FormData
        const formData = new FormData()
        formData.append('name', uploadForm.value.name)
        formData.append('typeCode', uploadForm.value.typeCode)
        formData.append('industryChainId', uploadForm.value.industryChainId!.toString())
        formData.append('dataPeriod', uploadForm.value.dataPeriod)
        formData.append('file', uploadForm.value.file)
        
        await uploadDataset(formData)
        
        ElMessage.success('上传成功')
        // 跳转到数据列表页
        router.push('/data/edit')
        
    } catch (error) {
        console.error('上传失败:', error)
        ElMessage.error('上传失败')
    } finally {
        uploading.value = false
    }
}

// 重置表单
const resetForm = () => {
  if (uploadFormRef.value) {
    uploadFormRef.value.resetFields()
  }
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
  uploadForm.value.file = null
}
</script>

<style scoped lang="scss">
.data-upload-container {
  padding: 20px;

  .upload-card {
    max-width: 800px;
    margin: 0 auto;

    .card-header {
      h3 {
        margin: 0;
        font-size: 18px;
        font-weight: 500;
      }
    }

    .form-section {
      margin-bottom: 30px;

      h4 {
        margin: 0 0 20px;
        padding-bottom: 10px;
        border-bottom: 1px solid #eee;
        color: #606266;
      }
    }

    .form-actions {
      margin-top: 30px;
      text-align: center;
    }

    :deep(.upload-demo) {
      width: 360px;

      .el-upload {
        width: 100%;
        
        .el-upload-dragger {
          width: 100%;
        }
      }

      .el-upload__tip {
        color: #909399;
      }
    }
  }

  .period-select {
    display: flex;
    gap: 10px;
  }
}
</style> 