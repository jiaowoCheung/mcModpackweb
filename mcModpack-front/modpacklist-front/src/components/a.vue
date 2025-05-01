<template>
    <div class="search-container">
      <el-input
        ref="inputRef"
        v-model="projectName"
        class="w-50 m-2"
        @input="inputChange"
        @focus="inputFocusFn"
        @blur="inputBlurFn"
        @keydown.down="handleKeyDown"
        @keydown.up="handleKeyDown"
        @keydown.enter="handleEnter"
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
          @mouseenter="activeIndex = index"
          :class="['suggestion-item', { 'active': activeIndex === index }]"
        >
          {{ item.label }}
        </p>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, watch, nextTick } from 'vue'
  import type { PropType } from 'vue'
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
  
  const inputRef = ref()
  const projectName = ref<string>(props.modelValue)
  const isShow = ref<boolean>(false)
  const cityArr = ref<CityOption[]>([])
  const cityOptions = ref<CityOption[]>(props.options)
  const activeIndex = ref<number>(-1)
  
  // 添加监听
  watch(() => props.modelValue, (newVal) => {
    projectName.value = newVal
  })
  
  watch(() => props.options, (newOptions) => {
    cityOptions.value = newOptions
  }, { deep: true })
  
  const inputChange = (): void => {
    emit('update:modelValue', projectName.value)
    
    if (projectName.value === '') {
      isShow.value = false
      activeIndex.value = -1
    } else {
      cityArr.value = cityOptions.value.filter(item => 
        item.label.includes(projectName.value)
      )
      isShow.value = cityArr.value.length > 0
      activeIndex.value = -1
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
    activeIndex.value = -1
  }
  
  const handleKeyDown = (e: KeyboardEvent): void => {
    if (!isShow.value || cityArr.value.length === 0) return
  
    if (e.key === 'ArrowDown') {
      e.preventDefault()
      activeIndex.value = (activeIndex.value + 1) % cityArr.value.length
      scrollToActiveItem()
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      activeIndex.value = (activeIndex.value - 1 + cityArr.value.length) % cityArr.value.length
      scrollToActiveItem()
    }
  }
  
  const handleEnter = (e: KeyboardEvent): void => {
    if (activeIndex.value >= 0 && activeIndex.value < cityArr.value.length) {
      e.preventDefault()
      handleSelect(cityArr.value[activeIndex.value])
    }
  }
  
  const scrollToActiveItem = (): void => {
    nextTick(() => {
      const container = document.querySelector('.suggestion-box')
      const activeItem = document.querySelector('.suggestion-item.active')
      if (container && activeItem) {
        activeItem.scrollIntoView({
          block: 'nearest',
          behavior: 'smooth'
        })
      }
    })
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
  
  .suggestion-item:hover,
  .suggestion-item.active {
    background-color: #f5f7fa;
  }
  </style>