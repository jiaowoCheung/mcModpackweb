<script setup lang="ts">
import { defineProps ,ref,watch,onMounted} from 'vue'
defineProps<{ msg: string }>()
import background from '@/assets/picture/background.jpg'
import ProjectSearch from '@/components/searchplugin.vue'
import PageSelect from '@/components/PageSelect.vue'
// 搜索相关逻辑

const searchValue = ref('')
const searchOptions = ref([
  //backend返回的项目列表
  //backend未完成
  { id: 1, label: '项目A' },
  { id: 2, label: '项目B' },
  { id: 3, label: '项目C' } ,
  // 更多项目...
])

interface ImageItem {
  id: number
  title: string
  imgUrl: string
  engtitle: string
}
const imageData = ref<ImageItem[]>([])

watch(searchValue, (newVal) => {
  console.log('searchValue变化:', newVal) // 确认是否接收到更新
})

const fetchImages = async () => {
  // 这里模拟数据，实际替换为你的API调用
  const mockData: ImageItem[] = Array.from({ length: 100 }, (_, i) => ({
    id: i + 1,
    title: `图片标题 ${i + 1}`,
    imgUrl: `https://picsum.photos/200/150?random=${i}`,
    engtitle: `photo title`
  }))
  
  imageData.value = mockData
}


const handleProjectSelect = (project: { id: number | string; label: string }) => {
  console.log('选中项目:', project)
  
  // 这里可以添加选择项目后的逻辑
}

const handlePageChange = (page: number) => {
  console.log('当前页码:', page)
}
onMounted(() => {
  fetchImages()
})

</script>

<template>
 <div class="main-page">
    <!-- 背景图片 -->
    <div class="background-container" :style="{ backgroundImage: `url(${background})` }"></div>
    
    <!-- 主内容区 -->
    <div class="content">
      <h1 class="title-font">{{ msg }}</h1>
      
      <!-- 搜索框 -->
      <ProjectSearch
        v-model="searchValue"
        :options="searchOptions"
        @select="handleProjectSelect"
        class="search-box"
      />
      
      <!-- 分页组件 -->
      <PageSelect 
        :data="imageData" 
        @page-change="handlePageChange"
      />
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
  color:black;
  text-align: left;
}

@font-face {
  font-family: 'PangMenZhengDao';
  src: url('@/assets/fonts/PangMenZhengDaoBiaoTiTiMianFeiBan-2.ttf') format('truetype');
}

.title-font {
  font-family: 'PangMenZhengDao';
  color:rgba(132, 230, 52, 0.85);
  font-size: 60px;
}

</style>
