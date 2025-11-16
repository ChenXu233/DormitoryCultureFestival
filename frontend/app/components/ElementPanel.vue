<template>
  <div class="element-panel">
    <!-- 面板标题 -->
    <h2 class="text-xl font-semibold text-gray-800 mb-4">桌面元素</h2>
    
    <!-- 元素分类 -->
    <div class="mb-6">
      <div class="flex flex-wrap gap-2 mb-4">
        <button 
          v-for="category in categories" 
          :key="category.id"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap',
            selectedCategory === category.id 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          ]"
          @click="selectedCategory = category.id"
        >
          {{ category.name }}
        </button>
      </div>
    </div>

    <!-- 元素列表 -->
    <div class="grid grid-cols-2 gap-3 max-h-96 overflow-y-auto">
      <div 
        v-for="element in filteredElements" 
        :key="element.id"
        class="bg-gray-50 rounded-lg p-3 cursor-pointer hover:bg-gray-100 transition-colors border-2 border-transparent hover:border-blue-300 group"
        draggable="true"
        @dragstart="onDragStart($event, element)"
        @dragend="onDragEnd"
        @click="onElementClick(element)"
      >
        <div class="text-center">
          <div class="w-12 h-12 mx-auto mb-2 flex items-center justify-center text-2xl transition-transform group-hover:scale-110">
            {{ element.icon }}
          </div>
          <span class="text-sm font-medium text-gray-700">{{ element.name }}</span>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div 
      v-if="filteredElements.length === 0"
      class="text-center py-8 text-gray-500"
    >
      <div class="text-4xl mb-2">📦</div>
      <p class="text-sm">该分类暂无元素</p>
    </div>
  </div>
</template>

<script setup lang="ts">
// 定义元素接口
interface DesktopElement {
  id: number | string
  name: string
  icon: string
  category: string
  size?: number
}

// 定义分类接口
interface Category {
  id: string
  name: string
}

// 定义组件属性
interface Props {
  categories?: Category[]
  elements?: DesktopElement[]
}

// 定义组件事件
interface Emits {
  (e: 'dragStart', element: DesktopElement, event: DragEvent): void
  (e: 'dragEnd'): void
  (e: 'elementClick', element: DesktopElement): void
}

// 组件属性
const props = withDefaults(defineProps<Props>(), {
  categories: () => [
    { id: 'study', name: '学习用品' },
    { id: 'electronics', name: '电子设备' },
    { id: 'daily', name: '生活用品' },
    { id: 'decor', name: '装饰物品' }
  ],
  elements: () => [
    // 学习用品
    { id: 1, name: '书本', icon: '📚', category: 'study', size: 2 },
    { id: 2, name: '笔记本', icon: '📓', category: 'study', size: 1.8 },
    { id: 3, name: '笔筒', icon: '✏️', category: 'study', size: 1.5 },
    { id: 4, name: '计算器', icon: '🧮', category: 'study', size: 1.3 },
    { id: 5, name: '文件夹', icon: '📁', category: 'study', size: 1.6 },
    { id: 6, name: '便签', icon: '📝', category: 'study', size: 1.2 },
    
    // 电子设备
    { id: 7, name: '笔记本电脑', icon: '💻', category: 'electronics', size: 2.2 },
    { id: 8, name: '手机', icon: '📱', category: 'electronics', size: 1.4 },
    { id: 9, name: '平板', icon: '📟', category: 'electronics', size: 1.8 },
    { id: 10, name: '耳机', icon: '🎧', category: 'electronics', size: 1.3 },
    { id: 11, name: '键盘', icon: '⌨️', category: 'electronics', size: 1.7 },
    { id: 12, name: '鼠标', icon: '🖱️', category: 'electronics', size: 1.2 },
    
    // 生活用品
    { id: 13, name: '水杯', icon: '🥤', category: 'daily', size: 1.5 },
    { id: 14, name: '台灯', icon: '💡', category: 'daily', size: 1.8 },
    { id: 15, name: '闹钟', icon: '⏰', category: 'daily', size: 1.4 },
    { id: 16, name: '植物', icon: '🌿', category: 'daily', size: 1.6 },
    { id: 17, name: '纸巾', icon: '🧻', category: 'daily', size: 1.2 },
    { id: 18, name: '零食', icon: '🍿', category: 'daily', size: 1.3 },
    
    // 装饰物品
    { id: 19, name: '相框', icon: '🖼️', category: 'decor', size: 1.8 },
    { id: 20, name: '玩偶', icon: '🧸', category: 'decor', size: 1.5 },
    { id: 21, name: '小摆件', icon: '🔮', category: 'decor', size: 1.3 },
    { id: 22, name: '香薰', icon: '🕯️', category: 'decor', size: 1.2 },
    { id: 23, name: '挂画', icon: '🎨', category: 'decor', size: 2 },
    { id: 24, name: '花瓶', icon: '🏺', category: 'decor', size: 1.6 }
  ]
})

// 组件事件
const emit = defineEmits<Emits>()

// 响应式数据
const selectedCategory = ref(props.categories[0]?.id || 'study')

// 计算属性：过滤元素
const filteredElements = computed(() => {
  const category = props.categories.find(cat => cat.id === selectedCategory.value)
  if (!category) return []
  
  return props.elements.filter(el => el.category === category.id)
})

// 拖拽相关函数
const onDragStart = (event: DragEvent, element: DesktopElement) => {
  if (event.dataTransfer) {
    // 设置拖拽数据
    event.dataTransfer.setData('text/plain', JSON.stringify(element))
    event.dataTransfer.effectAllowed = 'copy'
    
    // 设置拖拽图片
    const dragIcon = document.createElement('div')
    dragIcon.textContent = element.icon
    dragIcon.style.fontSize = '2rem'
    dragIcon.style.opacity = '0'
    document.body.appendChild(dragIcon)
    
    event.dataTransfer.setDragImage(dragIcon, 0, 0)
    
    setTimeout(() => {
      document.body.removeChild(dragIcon)
    }, 0)
  }
  
  emit('dragStart', element, event)
}

const onDragEnd = () => {
  emit('dragEnd')
}

// 元素点击事件
const onElementClick = (element: DesktopElement) => {
  emit('elementClick', element)
}

// 暴露方法给父组件
defineExpose({
  selectedCategory,
  filteredElements
})
</script>

<style scoped>
/* 自定义滚动条 */
.grid::-webkit-scrollbar {
  width: 6px;
}

.grid::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.grid::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.grid::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 拖拽元素样式 */
.cursor-grab {
  cursor: grab;
}

.cursor-grab:active {
  cursor: grabbing;
}
</style>