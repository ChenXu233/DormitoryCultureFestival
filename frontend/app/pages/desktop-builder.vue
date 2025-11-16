<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 页面头部 -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <NuxtLink to="/" class="text-blue-600 hover:text-blue-700">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
              </svg>
            </NuxtLink>
            <h1 class="text-2xl font-bold text-gray-900">寝室桌面搭建</h1>
          </div>
          <div class="flex items-center space-x-3">
            <button 
              @click="resetCanvas"
              class="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              重置
            </button>
            <button 
              @click="showSavePanel = true"
              class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
            >
              保存与分享
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="flex-1 flex">
      <!-- 左侧元素面板 -->
      <aside class="w-80 bg-white border-r h-[calc(100vh-80px)] overflow-y-auto">
        <div class="p-4">
          <!-- 背景选择面板 -->
          <BackgroundPanel 
            ref="backgroundPanelRef"
            @background-change="onBackgroundChange"
            class="mb-6"
          />
          
          <!-- 元素选择面板 -->
          <ElementPanel @element-select="onElementSelect" />
        </div>
      </aside>

      <!-- 中间画布区域 -->
      <div class="flex-1 flex flex-col">
        <!-- 工具栏 -->
        <div class="bg-white border-b p-4">
          <DesktopBuilderToolbar 
            :selected-element="selectedElement"
            @element-update="onElementUpdate"
            @delete-element="deleteElement"
          />
        </div>
        
        <!-- 画布 -->
        <div class="flex-1 p-8 overflow-auto">
          <DesktopBuilderCanvas 
            ref="canvasRef"
            :elements="elements"
            :background="currentBackground"
            :selected-element="selectedElement"
            @element-select="onElementSelect"
            @element-update="onElementUpdate"
            @element-add="addElement"
          />
        </div>
      </div>

      <!-- 右侧属性面板 -->
      <aside class="w-80 bg-white border-l h-[calc(100vh-80px)] overflow-y-auto">
        <div class="p-4">
          <h2 class="text-lg font-semibold text-gray-800 mb-4">属性设置</h2>
          <!-- 属性设置内容将在这里 -->
        </div>
      </aside>
    </main>

    <!-- 保存与分享面板模态框 -->
    <div 
      v-if="showSavePanel" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="showSavePanel = false"
    >
      <div 
        class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 max-h-[80vh] overflow-y-auto"
        @click.stop
      >
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-semibold text-gray-900">保存与分享</h3>
            <button 
              @click="showSavePanel = false"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          
          <SaveSharePanel 
            ref="saveSharePanelRef"
            :design-data="designData"
            @load-design="onLoadDesign"
            @export-image="onExportImage"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 设置页面元信息
useSeoMeta({
  title: '寝室桌面搭建 - 宿舍文化节',
  description: '拖拽元素到桌面上，打造你理想的寝室桌面，支持旋转、缩放、层级排序等操作'
})

// 页面配置
definePageMeta({
  layout: false
})

// 导入组件
import ElementPanel from '~/components/ElementPanel.vue'
import DesktopBuilderToolbar from '~/components/DesktopBuilder.vue'
import DesktopBuilderCanvas from '~/components/DesktopBuilder.vue'
import BackgroundPanel from '~/components/BackgroundPanel.vue'
import SaveSharePanel from '~/components/SaveSharePanel.vue'

// 响应式数据
const elements = ref<any[]>([])
const selectedElement = ref<any>(null)
const currentBackground = ref<any>({ id: 1, name: '木质桌面', color: '#f5deb3', type: 'solid' })
const showSavePanel = ref(false)

// 引用
const canvasRef = ref()
const backgroundPanelRef = ref()
const saveSharePanelRef = ref()

// 处理元素选择
const onElementSelect = (element: any) => {
  selectedElement.value = element
}

// 处理元素更新
const onElementUpdate = (updatedElement: any) => {
  const index = elements.value.findIndex(el => el.id === updatedElement.id)
  if (index !== -1) {
    elements.value[index] = { ...elements.value[index], ...updatedElement }
  }
}

// 添加元素
const addElement = (elementData: any) => {
  const newElement = {
    id: Date.now().toString(),
    ...elementData,
    x: 100,
    y: 100,
    rotation: 0,
    scale: 1,
    zIndex: elements.value.length + 1
  }
  elements.value.push(newElement)
  selectedElement.value = newElement
}

// 删除元素
const deleteElement = () => {
  if (selectedElement.value) {
    elements.value = elements.value.filter(el => el.id !== selectedElement.value.id)
    selectedElement.value = null
  }
}

// 重置画布
const resetCanvas = () => {
  elements.value = []
  selectedElement.value = null
  currentBackground.value = { id: 1, name: '木质桌面', color: '#f5deb3', type: 'solid' }
  
  // 重置背景面板
  if (backgroundPanelRef.value) {
    backgroundPanelRef.value.selectBackground(currentBackground.value)
  }
}

// 处理背景变化
const onBackgroundChange = (background: any) => {
  currentBackground.value = background
}

// 处理加载设计
const onLoadDesign = (design: any) => {
  if (design.data) {
    elements.value = design.data.elements || []
    currentBackground.value = design.data.background || currentBackground.value
    
    // 更新背景面板
    if (backgroundPanelRef.value) {
      backgroundPanelRef.value.selectBackground(currentBackground.value)
    }
    
    showSavePanel.value = false
  }
}

// 处理导出图片
const onExportImage = () => {
  if (canvasRef.value) {
    canvasRef.value.exportAsImage()
  }
  showSavePanel.value = false
}

// 计算设计数据
const designData = computed(() => ({
  elements: elements.value,
  background: currentBackground.value,
  canvasSize: { width: 800, height: 600 }
}))
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
.cursor-move {
  cursor: move;
}

.cursor-move:active {
  cursor: grabbing;
}
</style>