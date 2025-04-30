<!-- src/components/ProjectSearch.vue -->
<template>
  <div class="search-container">
    <el-input
      v-model="projectName"
      class="w-50 m-2"
      @input="inputChange"
      @focus="inputFocusFn"
      @blur="inputBlurFn"
      placeholder="请输入项目名称"
      clearable
    >
      <template #suffix>
        <el-icon class="el-input__icon">
          <search />
        </el-icon>
      </template>
    </el-input>
    <!-- 搜索候选框 -->
    <div v-show="isShow" class="suggestion-box">
      <p 
        v-for="(item, index) in cityArr" 
        :key="index" 
        @click="handleSelect(item)"
        class="suggestion-item"
      >
        {{ item.label }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { PropType } from 'vue' // 使用 type-only 导入
import { Search } from '@element-plus/icons-vue'

interface CityOption {
  id: number | string
  label: string
  [key: string]: any
}

const props = defineProps({
  options: {
    type: Array as PropType<CityOption[]>,
    default: () => []
  },
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'select'])

const projectName = ref<string>(props.modelValue)
const isShow = ref<boolean>(false)
const cityArr = ref<CityOption[]>([])
const cityOptions = ref<CityOption[]>(props.options)

const inputChange = (): void => {
  emit('update:modelValue', projectName.value)
  
  if (projectName.value === '') {
    isShow.value = false
  } else {
    cityArr.value = cityOptions.value.filter(item => 
      item.label.includes(projectName.value)
    )
    isShow.value = cityArr.value.length > 0
  }
}

const inputFocusFn = (): void => { 
  isShow.value = projectName.value !== '' && cityArr.value.length > 0
}

const inputBlurFn = (): void => { 
  setTimeout(() => {
    isShow.value = false
  }, 200)
}

const handleSelect = (item: CityOption): void => {
  projectName.value = item.label
  emit('update:modelValue', item.label)
  emit('select', item)
  isShow.value = false
}
</script>

<style scoped>
.search-container {
  position: relative;
  width: 100%;
}

.suggestion-box {
  position: absolute;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  background: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 1000;
  margin-top: 4px;
}

.suggestion-item {
  padding: 8px 16px;
  margin: 0;
  line-height: 1.5;
  cursor: pointer;
}

.suggestion-item:hover {
  background-color: #f5f7fa;
}
</style>