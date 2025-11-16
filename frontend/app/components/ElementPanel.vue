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

    <!-- 元素列表 - 主元素+变体结构 -->
    <div class="space-y-6 max-h-96 overflow-y-auto">
      <div 
        v-for="element in filteredElements" 
        :key="element.id"
        class="bg-gray-50 rounded-lg p-4 border-2 border-transparent hover:border-blue-300"
      >
        <!-- 主元素信息 -->
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 flex items-center justify-center text-2xl">
              {{ element.icon }}
            </div>
            <span class="font-medium text-gray-700">{{ element.name }}</span>
          </div>
          <span class="text-xs text-gray-500">{{ element.variants.length }}个变体</span>
        </div>
        
        <!-- 变体网格 -->
        <div class="grid grid-cols-4 gap-2">
          <div 
            v-for="variant in element.variants" 
            :key="variant.id"
            class="bg-white rounded-lg p-2 cursor-pointer hover:bg-blue-50 transition-colors border border-gray-200 hover:border-blue-300 flex flex-col items-center"
            draggable="true"
            @dragstart="onDragStart($event, getVariantElement(element, variant))"
            @dragend="onDragEnd"
            @click="onElementClick(getVariantElement(element, variant))"
          >
            <div class="text-xl mb-1">{{ variant.icon }}</div>
            <span class="text-xs text-gray-600">{{ variant.name }}</span>
          </div>
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
import { ref, computed } from 'vue'

// 定义变体接口
interface ElementVariant {
  id: number | string
  name: string
  icon: string
  size?: number
}

// 定义元素接口
interface DesktopElement {
  id: number | string
  name: string
  icon: string
  category: string
  variants: ElementVariant[]
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
  (e: 'dragStart', element: any, event: DragEvent): void
  (e: 'dragEnd'): void
  (e: 'elementClick', element: any): void
}

// 组件属性
const props = withDefaults(defineProps<Props>(), {
  categories: () => [
    { id: 'study', name: '学习用品' },
    { id: 'electronics', name: '电子设备' },
    { id: 'daily', name: '生活用品' },
    { id: 'decor', name: '装饰物品' },
    { id: 'furniture', name: '家具' } // 添加家具分类
  ],
  elements: () => [
    // 学习用品
    {
      id: 1, 
      name: '书本', 
      icon: '📚', 
      category: 'study',
      variants: [
        { id: 101, name: '教科书', icon: '📖', size: 2.2 },
        { id: 102, name: '小说', icon: '📓', size: 2 },
        { id: 103, name: '杂志', icon: '📰', size: 1.8 },
        { id: 104, name: '笔记本', icon: '📝', size: 1.6 }
      ]
    },
    {
      id: 2, 
      name: '文具', 
      icon: '✏️', 
      category: 'study',
      variants: [
        { id: 201, name: '钢笔', icon: '✒️', size: 1.3 },
        { id: 202, name: '铅笔', icon: '✏️', size: 1.2 },
        { id: 203, name: '荧光笔', icon: '🖊️', size: 1.3 },
        { id: 204, name: '橡皮擦', icon: '🧽', size: 1.1 }
      ]
    },
    {
      id: 3, 
      name: '计算器', 
      icon: '🧮', 
      category: 'study',
      variants: [
        { id: 301, name: '科学计算器', icon: '🧮', size: 1.5 },
        { id: 302, name: '普通计算器', icon: '🔢', size: 1.3 },
        { id: 303, name: '算盘', icon: '🟥', size: 1.4 },
        { id: 304, name: '函数计算器', icon: '🔣', size: 1.6 }
      ]
    },
    
    // 电子设备
    {
      id: 4, 
      name: '电脑', 
      icon: '💻', 
      category: 'electronics',
      variants: [
        { id: 401, name: '笔记本电脑', icon: '💻', size: 2.2 },
        { id: 402, name: '台式电脑', icon: '🖥️', size: 2.5 },
        { id: 403, name: '平板电脑', icon: '📟', size: 1.8 },
        { id: 404, name: '一体机', icon: '🖨️', size: 2.3 }
      ]
    },
    {
      id: 5, 
      name: '手机', 
      icon: '📱', 
      category: 'electronics',
      variants: [
        { id: 501, name: '智能手机', icon: '📱', size: 1.4 },
        { id: 502, name: '折叠手机', icon: '📲', size: 1.3 },
        { id: 503, name: '游戏手机', icon: '🎮', size: 1.5 },
        { id: 504, name: '复古手机', icon: '📞', size: 1.2 }
      ]
    },
    
    // 生活用品
    {
      id: 6, 
      name: '水杯', 
      icon: '🥤', 
      category: 'daily',
      variants: [
        { id: 601, name: '塑料杯', icon: '🥤', size: 1.5 },
        { id: 602, name: '保温杯', icon: '☕', size: 1.4 },
        { id: 603, name: '玻璃杯', icon: '🥃', size: 1.6 },
        { id: 604, name: '马克杯', icon: '🧋', size: 1.5 }
      ]
    },
    {
      id: 7, 
      name: '台灯', 
      icon: '💡', 
      category: 'daily',
      variants: [
        { id: 701, name: '护眼台灯', icon: '💡', size: 1.8 },
        { id: 702, name: '小夜灯', icon: '🌙', size: 1.5 },
        { id: 703, name: 'LED灯', icon: '🔦', size: 1.6 },
        { id: 704, name: '蜡烛灯', icon: '🕯️', size: 1.4 }
      ]
    },
    
    // 装饰物品
    {
      id: 8, 
      name: '相框', 
      icon: '🖼️', 
      category: 'decor',
      variants: [
        { id: 801, name: '方形相框', icon: '🖼️', size: 1.8 },
        { id: 802, name: '圆形相框', icon: '🎞️', size: 1.6 },
        { id: 803, name: '相册', icon: '📷', size: 1.7 },
        { id: 804, name: '照片墙', icon: '🏞️', size: 2 }
      ]
    },
    {
      id: 9, 
      name: '植物', 
      icon: '🌿', 
      category: 'decor',
      variants: [
        { id: 901, name: '多肉植物', icon: '🌱', size: 1.3 },
        { id: 902, name: '绿萝', icon: '🌿', size: 1.6 },
        { id: 903, name: '仙人掌', icon: '🌵', size: 1.5 },
        { id: 904, name: '花朵', icon: '🌸', size: 1.4 }
      ]
    },
    {
      id: 10, 
      name: '摆件', 
      icon: '🔮', 
      category: 'decor',
      variants: [
        { id: 1001, name: '水晶球', icon: '🔮', size: 1.3 },
        { id: 1002, name: '玩偶', icon: '🧸', size: 1.5 },
        { id: 1003, name: '时钟', icon: '⏰', size: 1.4 },
        { id: 1004, name: '香薰', icon: '🕯️', size: 1.2 }
      ]
    },
    
    // 添加家具分类 - 柜子
    {
      id: 11, 
      name: '柜子', 
      icon: '🗄️', 
      category: 'furniture',
      variants: [
        { id: 1101, name: '床头柜', icon: '🗄️', size: 2.5 },
        { id: 1102, name: '书柜', icon: '📚', size: 2.8 },
        { id: 1103, name: '储物柜', icon: '📦', size: 2.6 },
        { id: 1104, name: '抽屉柜', icon: '🗂️', size: 2.4 }
      ]
    },
    {
      id: 12, 
      name: '高级柜子', 
      icon: '🏬', 
      category: 'furniture',
      variants: [
        { id: 1201, name: '多层柜', icon: '🏬', size: 3 },
        { id: 1202, name: '玻璃柜', icon: '🪟', size: 2.9 },
        { id: 1203, name: '衣柜', icon: '👔', size: 3.2 },
        { id: 1204, name: '展示柜', icon: '🎁', size: 2.7 }
      ]
    }
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

// 获取变体元素数据
const getVariantElement = (element: DesktopElement, variant: ElementVariant) => {
  return {
    ...element,
    id: `${element.id}-${variant.id}`,
    name: `${element.name} - ${variant.name}`,
    icon: variant.icon,
    size: variant.size || 2,
    isCabinet: element.name.includes('柜子') // 标记为柜子
  }
}

// 拖拽相关函数
const onDragStart = (event: DragEvent, element: any) => {
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
const onElementClick = (element: any) => {
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
.space-y-6::-webkit-scrollbar {
  width: 6px;
}

.space-y-6::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.space-y-6::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.space-y-6::-webkit-scrollbar-thumb:hover {
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