<template>
  <div class="data-edit-container">
    <!-- 顶部操作区 -->
    <div class="header">
      <h2>数据集列表</h2>
      <el-button type="primary" :icon="Refresh" @click="fetchData" :loading="loading">
        刷新
      </el-button>
    </div>

    <!-- 筛选表单 -->
    <el-form :model="queryParams" class="search-form" inline>
      <el-form-item label="数据集名称">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入数据集名称"
          clearable
          @clear="handleQuery"
          style="width: 220px"
        />
      </el-form-item>
      
      <el-form-item label="数据集类型">
        <el-select
          v-model="queryParams.typeCode"
          placeholder="请选择数据集类型"
          clearable
          @clear="handleQuery"
          style="width: 220px"
        >
          <el-option
            v-for="item in datasetTypes"
            :key="item.code"
            :label="item.name"
            :value="item.code"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="产业链">
        <el-select
          v-model="queryParams.industryChainId"
          placeholder="请选择产业链"
          clearable
          @clear="handleQuery"
          style="width: 220px"
        >
          <el-option
            v-for="item in industryChains"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" :icon="Search" @click="handleQuery">查询</el-button>
        <el-button :icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 数据表格 -->
    <el-table
      v-loading="loading"
      :data="datasetList"
      border
      style="width: 100%"
    >
      <el-table-column
        prop="id"
        label="编号"
        width="80"
        align="center"
      />
      <el-table-column
        prop="name"
        label="数据集名称"
        min-width="200"
      />
      <el-table-column
        prop="dataPeriod"
        label="数据期间"
        width="120"
        align="center"
      >
        <template #default="{ row }">
          <el-tag 
            size="small"
            :type="getQuarterTagType(row.dataPeriod)"
          >
            {{ row.dataPeriod }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="typeName"
        label="数据类型"
        width="150"
        align="center"
      />
      <el-table-column
        prop="industryChainName"
        label="产业链"
        width="150"
        align="center"
      />
      <el-table-column
        label="操作"
        width="150"
        align="center"
      >
        <template #default="scope">
          <el-button
            type="primary"
            link
            size="small"
            @click="handleEdit(scope.row)"
          >
            编辑
          </el-button>
          <el-popconfirm
            title="确认删除该数据集吗？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            confirm-button-type="danger"
            @confirm="handleDelete(scope.row)"
          >
            <template #reference>
              <el-button
                type="danger"
                link
                size="small"
                :loading="scope.row.deleting"
              >
                删除
              </el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="queryParams.pageNum"
        v-model:page-size="queryParams.pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 编辑弹窗 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑数据集"
      width="500px"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="100px"
      >
        <el-form-item label="数据集名称" prop="name">
          <el-input
            v-model="editForm.name"
            placeholder="请输入数据集名称"
          />
        </el-form-item>

        <el-form-item label="数据集类型" prop="typeCode">
          <el-select
            v-model="editForm.typeCode"
            placeholder="请选择数据集类型"
            style="width: 100%"
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
            v-model="editForm.industryChainId"
            placeholder="请选择产业链"
            style="width: 100%"
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
              v-model="editYear"
              placeholder="选择年份"
              style="width: 120px"
              @change="updateEditDataPeriod"
            >
              <el-option
                v-for="year in years"
                :key="year"
                :label="year"
                :value="year"
              />
            </el-select>
            <el-select
              v-model="editQuarter"
              placeholder="选择季度"
              style="width: 120px"
              @change="updateEditDataPeriod"
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
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleEditSubmit" :loading="editLoading">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Refresh, Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { Dataset, DatasetQueryParams, DictDatasetType, IndustryChain } from '@/types/dataset'
import { getDatasetList, deleteDataset, updateDataset, getDatasetTypes, getIndustryChains } from '@/api/dataset'
import type { FormInstance } from 'element-plus'

// 查询参数
const queryParams = ref<DatasetQueryParams>({
  pageNum: 1,
  pageSize: 10,
  name: '',
  typeCode: '',
  industryChainId: undefined
})

// 数据列表
const datasetList = ref<Dataset[]>([])
const total = ref(0)
const loading = ref(false)

// 数据集类型选项（从后端动态获取）
const datasetTypes = ref<DictDatasetType[]>([])

// 产业链选项（从后端动态获取）
const industryChains = ref<IndustryChain[]>([])

// 获取数据集类型列表
const fetchDatasetTypes = async () => {
  try {
    const { data } = await getDatasetTypes()
    datasetTypes.value = data
    console.log('获取数据集类型列表:', datasetTypes.value)
  } catch (error) {
    console.error('获取数据集类型列表失败:', error)
    ElMessage.error('获取数据集类型列表失败')
  }
}

// 获取产业链列表
const fetchIndustryChains = async () => {
  try {
    const { data } = await getIndustryChains()
    industryChains.value = data
    console.log('获取产业链列表:', industryChains.value)
  } catch (error) {
    console.error('获取产业链列表失败:', error)
    ElMessage.error('获取产业链列表失败')
  }
}

// 编辑相关
const editDialogVisible = ref(false)
const editFormRef = ref<FormInstance>()
const editLoading = ref(false)
const editForm = ref<Partial<Dataset>>({})
const editYear = ref<number>()
const editQuarter = ref<string>()

// 编辑表单验证规则
const editRules = {
  name: [
    { required: true, message: '请输入数据集名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符之间', trigger: 'blur' }
  ],
  typeCode: [
    { required: true, message: '请选择数据集类型', trigger: 'change' }
  ],
  industryChainId: [
    { required: true, message: '请选择产业链', trigger: 'change' }
  ]
}

// 年份选项（从10年前到当前年份）
const currentYear = new Date().getFullYear()
const years = Array.from(
  { length: 11 },
  (_, i) => currentYear - 10 + i
).sort((a, b) => b - a)

// 季度选项
const quarters = [
  { value: 'Q1', label: '第一季度' },
  { value: 'Q2', label: '第二季度' },
  { value: 'Q3', label: '第三季度' },
  { value: 'Q4', label: '第四季度' }
]

// 查询方法
const handleQuery = async () => {
  queryParams.value.pageNum = 1  // 重置到第一页
  await fetchData()
}

// 重置查询
const resetQuery = () => {
  queryParams.value = {
    pageNum: 1,
    pageSize: 10,
    name: '',
    typeCode: '',
    industryChainId: undefined
  }
  fetchData()
}

// 获取数据列表
const fetchData = async () => {
  try {
    loading.value = true
    const { data } = await getDatasetList(queryParams.value)
    datasetList.value = data.records
    total.value = data.total
  } catch (error) {
    console.error('获取数据集列表失败:', error)
    ElMessage.error('获取数据集列表失败')
  } finally {
    loading.value = false
  }
}

// 处理编辑
const handleEdit = (row: Dataset) => {
  editForm.value = { ...row }
  if (row.dataPeriod) {
    editYear.value = parseInt(row.dataPeriod.slice(0, 4))
    editQuarter.value = row.dataPeriod.slice(4)
  }
  editDialogVisible.value = true
}

// 删除数据集
const handleDelete = async (row: Dataset) => {
  try {
    // 设置删除中状态
    row.deleting = true
    await deleteDataset(row.id)
    ElMessage.success('删除成功')
    // 如果当前页只有一条数据，且不是第一页，则删除后跳转到上一页
    if (datasetList.value.length === 1 && queryParams.value.pageNum > 1) {
      queryParams.value.pageNum--
    }
    // 重新加载数据
    await fetchData()
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败')
  } finally {
    // 清除删除中状态
    row.deleting = false
  }
}

// 处理分页大小改变
const handleSizeChange = (size: number) => {
  queryParams.value.pageSize = size
  queryParams.value.pageNum = 1
  fetchData()
}

// 处理页码改变
const handleCurrentChange = (page: number) => {
  queryParams.value.pageNum = page
  fetchData()
}

// 根据季度返回不同的标签类型
const getQuarterTagType = (dataPeriod: string): '' | 'success' | 'warning' | 'danger' => {
  if (!dataPeriod) return ''
  const quarter = dataPeriod.slice(-2) // 获取最后两个字符，如 "Q1"
  switch (quarter) {
    case 'Q1':
      return 'success'  // 绿色
    case 'Q2':
      return ''        // 默认蓝色
    case 'Q3':
      return 'warning' // 黄色
    case 'Q4':
      return 'danger'  // 红色
    default:
      return ''
  }
}

// 更新编辑表单的数据期间
const updateEditDataPeriod = () => {
  if (editYear.value && editQuarter.value) {
    editForm.value.dataPeriod = `${editYear.value}${editQuarter.value}`
  }
}

// 提交编辑
const handleEditSubmit = async () => {
  if (!editFormRef.value) return
  
  try {
    await editFormRef.value.validate()
    editLoading.value = true
    
    await updateDataset(editForm.value.id!, {
      name: editForm.value.name,
      typeCode: editForm.value.typeCode,
      industryChainId: editForm.value.industryChainId,
      dataPeriod: editForm.value.dataPeriod
    })
    
    ElMessage.success('更新成功')
    editDialogVisible.value = false
    await fetchData()
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error('更新失败')
  } finally {
    editLoading.value = false
  }
}

// 组件挂载时获取数据
onMounted(async () => {
  // 并行获取基础数据和数据列表
  await Promise.all([
    fetchDatasetTypes(),
    fetchIndustryChains(),
    fetchData()
  ])
})
</script>

<style scoped lang="scss">
.data-edit-container {
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      margin: 0;
    }
  }

  .search-form {
    background-color: #fff;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 4px;

    :deep(.el-form-item) {
      margin-bottom: 0;
      margin-right: 20px;
      
      &:last-child {
        margin-right: 0;
      }
    }
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  .period-select {
    display: flex;
    gap: 10px;
  }

  .dialog-footer {
    text-align: right;
  }
}
</style> 