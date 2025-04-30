<script setup lang="ts">
import { defineProps ,ref} from 'vue'
defineProps<{ msg: string }>()
import background from '@/assets/picture/background.jpg'
import ProjectSearch from '@/components/searchplugin.vue'
// 搜索相关逻辑
const searchValue = ref('')
const searchOptions = ref([
  { id: 1, label: '项目A' },
  { id: 2, label: '项目B' },
  { id: 3, label: '项目C' },
  // 更多项目...
])

const handleProjectSelect = (project: { id: number | string; label: string }) => {
  console.log('选中项目:', project)
  // 这里可以添加选择项目后的逻辑
}
</script>

<template>
 <div class="main-page">
    <!-- 背景图片 -->
    <div class="background-container" :style="{ backgroundImage: `url(${background})` }"></div>
    
    <!-- 主内容区 -->
    <div class="content">
      <h1>{{ msg }}</h1>
      
      <!-- 使用封装的搜索框组件 -->
      <ProjectSearch
        v-model="searchValue"
        :options="searchOptions"
        @select="handleProjectSelect"
        class="search-box"
      />
      
      <!-- 其他页面内容 -->
    </div>
  </div>
</template>

<style scoped>
.main-page {
  position: relative;
  width: 100%;
  height: 100vh; /* 改用 min-height */
}

.background-container {
  position: fixed; /* 改为 fixed 定位 */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-size: cover;
  background-position: center;
  z-index: -1;
}

.content {
  position: relative;
  z-index: 1;
  padding: 20px;
  color: white; /* 根据背景图调整文字颜色 */
  text-align: center;
}

.search-box {
  max-width: 500px;
  margin: 20px auto;
}
</style>
