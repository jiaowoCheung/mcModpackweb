<!-- src/components/searchplugin.vue -->
<template>
  <div class="search-container">
    <el-input
      v-model="projectName"
      class="w-50 m-2"
      ref="inputRef"
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
        :class="{
        'suggestion-item': true,
        'active': activeIndex === index
        }"
        >
        {{ item.label }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch ,nextTick} from 'vue'
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
const activeIndex = ref<number>(-1) // 用于高亮显示选中的候选项
const projectName = ref<string>(props.modelValue)
const isShow = ref<boolean>(false)
const cityArr = ref<CityOption[]>([])
const cityOptions = ref<CityOption[]>(props.options)

// 添加监听
watch(() => props.modelValue, (newVal) => {
  projectName.value = newVal
})

watch(() => props.options, (newOptions) => {
  cityOptions.value = newOptions
}, { deep: true })

const inputChange = (): void => {
  console.log('输入值:', projectName.value) 
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
/* 保持原有样式不变 */
.search-container {
  position: relative;
  width: 1000px;

}

.suggestion-box {
  position: absolute;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  background: rgba(146, 94, 236, 0.3);
  border: 0.5px solid rgba(146, 94, 236, 0.3);
  border-radius: 5px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 1000;
  margin-top: 4px;
}

.suggestion-item {
  padding: 6px 14px;
  margin: 0;
  line-height: 1.5;
  cursor: pointer;
  transition: background-color 0.3s ease; /* 添加过渡动画 */
  color: #3c3f45; /* 默认文字颜色 */
  background-color: rgba(255, 255, 255, 0.401);
}

.suggestion-item:hover {
  background-color: rgb(245, 247, 250); /* 悬停状态 */
}

.suggestion-item.active {
  background-color: rgba(146, 94, 236, 0.5) ; /* 选中状态 */
  color: white ;
}

</style>