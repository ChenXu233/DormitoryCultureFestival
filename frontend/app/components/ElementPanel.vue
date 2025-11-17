<template>
  <div class="bg-white rounded-lg shadow-md border border-gray-200 p-4 h-full">
    <h3 class="text-lg font-semibold mb-4 text-gray-800">可选元素</h3>
    
    <!-- 分类按钮 - 田字排列 -->
    <div class="grid grid-cols-2 gap-3 mb-4">
      <button 
        v-for="category in categories" 
        :key="category.id"
        :class="[
          'category-btn h-20 rounded-lg border-2 font-medium transition-all duration-200 flex flex-col items-center justify-center',
          activeCategory === category.id 
            ? 'bg-blue-500 text-white border-blue-600 shadow-lg transform scale-105' 
            : 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200 hover:border-gray-400 hover:shadow-md'
        ]"
        @click="selectCategory(category.id)"
      >
        <div class="text-2xl mb-1">{{ getCategoryIcon(category.id) }}</div>
        <div class="text-sm">{{ category.name }}</div>
      </button>
    </div>
    
    <!-- 子分类区域 -->
    <div v-if="selectedCategory" class="mb-4">
      <!-- 子分类标题 -->
      <div class="flex items-center justify-between mb-3">
        <h4 class="font-medium text-gray-700">{{ getCurrentCategoryName() }} - 子分类</h4>
        <button 
          @click="selectedCategory = null"
          class="text-gray-500 hover:text-gray-700 text-sm"
        >
          返回
        </button>
      </div>
      
      <!-- 子分类按钮 - 田字排列 -->
      <div class="grid grid-cols-2 gap-2 mb-4">
        <button 
          v-for="subCategory in getSubCategories(selectedCategory)" 
          :key="subCategory.id"
          :class="[
            'subcategory-btn h-16 rounded-md border font-medium transition-all duration-200 flex flex-col items-center justify-center',
            activeSubCategory === subCategory.id 
              ? 'bg-blue-100 text-blue-700 border-blue-300 shadow-md' 
              : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50 hover:border-gray-300'
          ]"
          @click="selectSubCategory(subCategory.id)"
        >
          <div class="text-lg mb-1">{{ subCategory.icon }}</div>
          <div class="text-xs">{{ subCategory.name }}</div>
        </button>
      </div>
      
      <!-- 元素网格 -->
      <div class="grid grid-cols-3 gap-2">
        <div 
          v-for="element in getFilteredElements()" 
          :key="element.name"
          class="element-item p-2 bg-white rounded border border-gray-200 cursor-move hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 text-center"
          draggable="true"
          @dragstart="$emit('element-drag-start', element, $event)"
          @click="$emit('element-click', element)"
        >
          <div class="text-xl mb-1">{{ element.icon }}</div>
          <div class="text-xs text-gray-600">{{ element.name }}</div>
        </div>
      </div>
    </div>
    
    <!-- 默认显示全部元素 -->
    <div v-else class="grid grid-cols-3 gap-2">
      <div 
        v-for="element in getFilteredElements()" 
        :key="element.name"
        class="element-item p-2 bg-white rounded border border-gray-200 cursor-move hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 text-center"
        draggable="true"
        @dragstart="$emit('element-drag-start', element, $event)"
        @click="$emit('element-click', element)"
      >
        <div class="text-xl mb-1">{{ element.icon }}</div>
        <div class="text-xs text-gray-600">{{ element.name }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ElementCategory, DraggableElement } from './types'

// 定义组件属性
interface Props {
  categories: ElementCategory[]
  elements: DraggableElement[]
  activeCategory: string
}

// 定义组件事件
interface Emits {
  (e: 'category-change', categoryId: string): void
  (e: 'element-drag-start', element: DraggableElement, event: DragEvent): void
  (e: 'element-click', element: DraggableElement): void
}

// 定义子分类接口
interface SubCategory {
  id: string
  name: string
  icon: string
  parentCategory: string
}

// 组件属性
const props = defineProps<Props>()

// 组件事件
const emit = defineEmits<Emits>()

// 状态管理
const selectedCategory = ref<string | null>(null)
const activeSubCategory = ref<string | null>(null)

// 子分类配置
const subCategories: SubCategory[] = [
  // 电子设备子分类
  { id: 'computer-set', name: '电脑套装', icon: '💻', parentCategory: 'electronics' },
  { id: 'mobile-devices', name: '移动设备', icon: '📱', parentCategory: 'electronics' },
  { id: 'audio-devices', name: '音频设备', icon: '🎧', parentCategory: 'electronics' },
  
  // 学习资料子分类
  { id: 'books', name: '书籍资料', icon: '📚', parentCategory: 'study' },
  { id: 'writing-tools', name: '书写工具', icon: '✏️', parentCategory: 'study' },
  { id: 'notes', name: '笔记用品', icon: '📋', parentCategory: 'study' },
  
  // 小工具子分类
  { id: 'office-tools', name: '办公工具', icon: '🖇️', parentCategory: 'tools' },
  { id: 'storage-devices', name: '存储设备', icon: '💾', parentCategory: 'tools' },
  { id: 'time-tools', name: '时间工具', icon: '⏰', parentCategory: 'tools' },
  
  // 生活用品子分类
  { id: 'lighting', name: '照明用品', icon: '💡', parentCategory: 'daily' },
  { id: 'drinkware', name: '饮水用品', icon: '🥤', parentCategory: 'daily' },
  { id: 'personal-items', name: '个人物品', icon: '💄', parentCategory: 'daily' }
]

// 选择主分类
const selectCategory = (categoryId: string) => {
  selectedCategory.value = categoryId
  activeSubCategory.value = null
  emit('category-change', categoryId)
}

// 选择子分类
const selectSubCategory = (subCategoryId: string) => {
  activeSubCategory.value = subCategoryId
}

// 获取分类图标
const getCategoryIcon = (categoryId: string) => {
  const icons: Record<string, string> = {
    'electronics': '💻',
    'study': '📚',
    'tools': '🔧',
    'daily': '🏠'
  }
  return icons[categoryId] || '📦'
}

// 获取当前分类名称
const getCurrentCategoryName = () => {
  const category = props.categories.find(cat => cat.id === selectedCategory.value)
  return category?.name || ''
}

// 获取指定主分类的子分类
const getSubCategories = (parentCategory: string) => {
  return subCategories.filter(sub => sub.parentCategory === parentCategory)
}

// 获取过滤后的元素列表
const getFilteredElements = () => {
  if (!selectedCategory.value) {
    // 显示全部元素
    return props.elements
  }
  
  if (!activeSubCategory.value) {
    // 显示主分类下的所有元素
    return props.elements.filter(el => el.category === selectedCategory.value)
  }
  
  // 根据子分类过滤元素
  const subCategoryElements: Record<string, string[]> = {
    // 电子设备子分类
    'computer-set': ['电脑', '键盘', '鼠标'],
    'mobile-devices': ['手机', '平板'],
    'audio-devices': ['耳机'],
    
    // 学习资料子分类
    'books': ['书籍'],
    'writing-tools': ['笔', '草稿纸'],
    'notes': ['便利贴'],
    
    // 小工具子分类
    'office-tools': ['订书机', '美工刀', '纸巾'],
    'storage-devices': ['U盘'],
    'time-tools': ['时钟', '计算器'],
    
    // 生活用品子分类
    'lighting': ['台灯'],
    'drinkware': ['水杯'],
    'personal-items': ['小零食', '手办', '镜子', '化妆品']
  }
  
  const elementNames = subCategoryElements[activeSubCategory.value] || []
  return props.elements.filter(el => 
    el.category === selectedCategory.value && 
    elementNames.includes(el.name)
  )
}
</script>

<style scoped>
.element-item {
  transition: all 0.2s ease;
}

.element-item:hover {
  transform: translateY(-2px);
}
</style>