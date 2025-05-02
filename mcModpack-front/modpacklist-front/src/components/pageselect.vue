<!-- src/components/PageSelect.vue -->
<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue'
import { ElPagination } from 'element-plus'

interface ImageItem {
  id: number
  title: string
  imgUrl: string
  engtitle: string
}

const props = defineProps<{
  data: ImageItem[]
  pageSize?: number
  itemsPerRow?: number
}>()

const emit = defineEmits(['page-change'])

const currentPage = ref(1)
const pageSize = ref(props.pageSize || 20)
const itemsPerRow = ref(props.itemsPerRow || 5)

const getCurrentPageData = () => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return props.data.slice(start, end)
}

watch(currentPage, (newVal) => {
  emit('page-change', newVal)
})


</script>

<template>
  <div class="page-select-container">
    <!-- 图片网格布局 -->
    <div class="image-grid">
      <div 
        v-for="item in getCurrentPageData()" 
        :key="item.id" 
        class="image-item"
      >
        <a :href="`/detail/${item.id}`">
          <img :src="item.imgUrl" :alt="item.title" width="200">
        </a>
        <h3 class="modpacktitle">{{ item.title }}</h3>
        <p class="modpackengtitle">{{ item.engtitle }}</p>
      </div>
    </div>
    
    <!-- Element Plus 分页 -->
    <el-pagination
      v-model:current-page="currentPage"
      :page-size="pageSize"
      :total="data.length"
      layout="total, prev, pager, next"
      small
      class="pagination"
    />
  </div>
</template>

<style scoped>
:deep(.el-pagination) {
  margin-top: 20px;
}

/* 修改页码按钮 */
:deep(.el-pagination .btn-prev),
:deep(.el-pagination .btn-next),
:deep(.el-pagination .number) {
  border-radius: 4px;
  margin: 0 3px;
  background-color: rgba(146, 94, 236, 0.3);
  color: rgba(132, 230, 52, 0.85);
  font-size: 12px;
}

:deep(.el-pagination__total) {
  font-size: 12px;
  color: rgba(132, 230, 52, 0.85);
  margin: 10px;
  font-weight: bold; 
}

/* 如果需要修改数字部分的样式 */
:deep(.el-pagination__total em) {
  color: #409eff; 
  font-style: normal; /* 取消斜体 */
}
/* 修改当前选中页 */
:deep(.el-pagination .number.is-active) {
  background-color: rgba(64, 160, 255, 0.8);
  color: white;
}

/* 修改每页条数选择器 */
:deep(.el-pagination .el-select .el-input) {
  width: 100px;
}
.image-grid {
  display: grid;
  grid-template-columns: repeat(v-bind(itemsPerRow), 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.image-item {
  background: rgba(146, 94, 236, 0.3);
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}

.image-item img {
  display: block;
  margin: 0 auto 10px;
  border-radius: 4px;
}

.pagination {
  justify-content: right;
}



.modpacktitle{
    font-size: 16px;
    font-weight: bold;
    margin: 5px;
    color: rgba(132, 230, 52, 0.85);
    text-align: left; 
    font-family: 'title-font';
}

.modpackengtitle{
    font-size: 14px;
    color: rgba(132, 230, 52, 0.85);
    text-align: left; 
    margin: 5px;
    font-family: 'engtitle-font';
}



@font-face {
  font-family: 'title-font';
  src: url('@/assets/fonts/ShipporiAntiqueB1-Regular-2.ttf') format('truetype');
}

@font-face {
  font-family: 'engtitle-font';
  src: url('@/assets/fonts/YouSheYuFeiTeJianKangTi-2.ttf') format('truetype');
}



</style>