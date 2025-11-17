<template>
  <div class="desktop-builder min-h-screen bg-gray-50 p-6">
    <!-- 页面标题 -->
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">寝室桌面搭建</h1>
      <p class="text-gray-600">拖拽元素到桌面，打造你的专属学习空间</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
      <!-- 左侧：元素面板 -->
      <div class="lg:col-span-1">
        <!-- 内置元素面板组件 -->
        <div class="bg-white rounded-lg shadow-md border border-gray-200 p-4 h-full">
          <h3 class="text-lg font-semibold mb-4 text-gray-800">可选元素</h3>
          
          <!-- 元素分类 -->
          <div class="mb-4">
            <button 
              v-for="category in elementCategories" 
              :key="category.id"
              :class="[
                'px-3 py-1.5 rounded-md text-sm mb-2 mr-2 inline-block',
                activeCategory === category.id 
                  ? 'bg-blue-100 text-blue-700 font-medium' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
              @click="activeCategory = category.id"
            >
              {{ category.name }}
            </button>
          </div>
          
          <!-- 元素网格 -->
          <div class="grid grid-cols-2 gap-3">
            <div 
              v-for="element in getFilteredElements()" 
              :key="element.name"
              class="element-item p-3 bg-gray-50 rounded-lg border border-gray-200 cursor-move hover:border-blue-300 hover:bg-blue-50 transition-colors text-center"
              draggable="true"
              @dragstart="onElementDragStart(element, $event)"
              @click="onElementClick(element)"
            >
              <div class="text-2xl mb-1">{{ element.icon }}</div>
              <div class="text-xs text-gray-600">{{ element.name }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 中间：桌面构建区域 -->
      <div class="lg:col-span-3">
        <!-- 桌面工具栏 -->
        <div class="toolbar flex flex-wrap justify-between items-center bg-white rounded-lg shadow-sm p-4 mb-4">
          <h2 class="text-xl font-semibold text-gray-800 mb-2 sm:mb-0">我的桌面</h2>
          <div class="flex space-x-2">
            <button 
              class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
              @click="clearDesktop"
            >
              清空桌面
            </button>
            <button 
              class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
              @click="saveDesktop"
            >
              保存配置
            </button>
            <button 
              class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
              @click="downloadImage"
            >
              下载图片
            </button>
          </div>
        </div>

        <!-- 选中元素的编辑面板 -->
        <div v-if="selectedElement" class="bg-white rounded-lg shadow-sm p-4 mb-4">
          <h3 class="text-sm font-semibold text-gray-700 mb-2">编辑：{{ selectedElement.name }}</h3>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label class="block text-xs text-gray-500 mb-1">旋转</label>
              <input 
                type="range" 
                min="0" 
                max="360" 
                step="1" 
                :value="selectedElement.rotation" 
                @input="selectedElement.rotation = Number($event.target.value)"
                class="w-full"
              />
              <span class="text-xs text-gray-500">{{ selectedElement.rotation }}°</span>
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-1">缩放</label>
              <input 
                type="range" 
                min="0.5" 
                max="2" 
                step="0.1" 
                :value="selectedElement.scale" 
                @input="selectedElement.scale = Number($event.target.value)"
                class="w-full"
              />
              <span class="text-xs text-gray-500">{{ selectedElement.scale.toFixed(1) }}x</span>
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-1">大小</label>
              <input 
                type="range" 
                min="1" 
                max="4" 
                step="0.5" 
                :value="selectedElement.size || 2" 
                @input="selectedElement.size = Number($event.target.value)"
                class="w-full"
              />
              <span class="text-xs text-gray-500">{{ (selectedElement.size || 2) }}rem</span>
            </div>
          </div>
        </div>

        <!-- 桌面画布容器 - 添加3D透视效果 -->
        <div class="perspective-container">
          <div class="desktop-canvas-container" style="height: 500px;">
            <!-- 桌面画布 - 3D立体桌面 -->
            <div 
              ref="desktopCanvas"
              class="relative w-full h-full rounded-lg border-2 border-gray-300 overflow-hidden shadow-xl"
              :style="getDesktopStyle()"
              @dragover="onDragOver"
              @drop="onDrop"
              @click.self="deselectElement"
            >
              <!-- 桌面边缘装饰，增强立体感 -->
              <div class="desktop-edge"></div>
              <div class="desktop-legs"></div>
              
              <!-- 放置的元素 -->
              <div 
                v-for="element in elements" 
                :key="element.id"
                class="absolute cursor-move select-none transition-all duration-300"
                :style="{
                  left: element.x + 'px',
                  top: element.y + 'px',
                  transform: getElementTransform(element),
                  zIndex: element.zIndex,
                  perspective: '1000px'
                }"
                @mousedown="startDrag(element, $event)"
                @contextmenu.prevent="showContextMenu($event, element)"
                @mouseenter="elementHovered = element.id"
                @mouseleave="elementHovered = null"
              >
                <div 
                  :class="[
                    'p-2 rounded-lg transition-all duration-300',
                    selectedElement?.id === element.id 
                      ? 'border-blue-500 ring-2 ring-blue-200 shadow-xl' 
                      : 'border-transparent shadow-lg',
                    elementHovered === element.id ? 'transform hover-scale' : ''
                  ]"
                  :style="getElement3DStyle(element)"
                >
                  <div class="text-center">
                    <div 
                      class="transform transition-transform duration-300 hover:scale-110"
                      :style="{ fontSize: `${element.size || 2}rem` }"
                    >
                      {{ element.icon }}
                    </div>
                    <!-- 元素底部阴影，增强立体感 -->
                    <div class="element-base"></div>
                  </div>
                </div>
              </div>

              <!-- 空状态提示 -->
              <div 
                v-if="elements.length === 0"
                class="absolute inset-0 flex items-center justify-center text-gray-400"
              >
                <div class="text-center">
                  <div class="text-6xl mb-4">📱</div>
                  <p class="text-lg">拖拽元素到桌面上开始搭建</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 操作提示 -->
    <div class="mt-4 text-sm text-gray-600 text-center">
      <p>💡 提示：拖拽元素到桌面，右键点击元素并选择"编辑元素"进行属性调整</p>
    </div>

    <!-- 右键菜单 -->
    <div 
      v-if="contextMenu.visible"
      class="fixed bg-white shadow-lg rounded-lg py-2 z-50 min-w-32"
      :style="{ left: contextMenu.x + 'px', top: contextMenu.y + 'px' }"
      @click.stop
    >
      <button 
        class="w-full px-4 py-2 text-left text-green-600 hover:bg-green-50 flex items-center"
        @click="editElement"
      >
        <span class="mr-2">✏️</span> 编辑元素
      </button>
      <button 
        class="w-full px-4 py-2 text-left text-blue-600 hover:bg-blue-50 flex items-center"
        @click="duplicateElement"
      >
        <span class="mr-2">📋</span> 复制元素
      </button>
      <button 
        class="w-full px-4 py-2 text-left text-red-600 hover:bg-red-50 flex items-center"
        @click="deleteElement"
      >
        <span class="mr-2">🗑️</span> 删除元素
      </button>
      <div class="border-t my-1"></div>
      <button 
        class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
        @click="rotateElement(45)"
      >
        <span class="mr-2">↻</span> 顺时针旋转
      </button>
      <button 
        class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
        @click="rotateElement(-45)"
      >
        <span class="mr-2">↺</span> 逆时针旋转
      </button>
      <div class="border-t my-1"></div>
      <button 
        class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
        @click="bringToFront"
      >
        <span class="mr-2">⬆️</span> 置顶
      </button>
      <button 
        class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
        @click="sendToBack"
      >
        <span class="mr-2">⬇️</span> 置底
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'

// 定义元素接口 - 扩展以支持3D属性
interface DesktopElement {
  id: number | string
  name: string
  icon: string
  x: number
  y: number
  rotation: number
  scale: number
  zIndex: number
  size?: number
  category?: string
  isCabinet?: boolean
  // 3D相关属性
  depth?: number
  rotationX?: number
  rotationY?: number
  material?: string
}

// 元素类别
interface ElementCategory {
  id: string
  name: string
}

// 定义组件属性
interface Props {
  background?: string
  initialElements?: DesktopElement[]
}

// 定义组件事件
interface Emits {
  (e: 'update:elements', elements: DesktopElement[]): void
  (e: 'elementSelected', element: DesktopElement | null): void
  (e: 'save', config: any): void
}

// 组件属性
const props = withDefaults(defineProps<Props>(), {
  background: '#f5deb3',
  initialElements: () => []
})

// 组件事件
const emit = defineEmits<Emits>()

// 响应式数据
const desktopCanvas = ref<HTMLElement>()
const selectedElement = ref<DesktopElement | null>(null)
const contextMenu = reactive({ 
  visible: false, 
  x: 0, 
  y: 0, 
  element: null as DesktopElement | null 
})
const background = ref(props.background)
const elementHovered = ref<number | string | null>(null)
const activeCategory = ref('all')

// 桌面元素
const elements = ref<DesktopElement[]>(props.initialElements)

// 预定义的元素类别
const elementCategories: ElementCategory[] = [
  { id: 'all', name: '全部' },
  { id: 'electronics', name: '电子设备' },
  { id: 'furniture', name: '家具' },
  { id: 'stationery', name: '文具' },
  { id: 'decorations', name: '装饰品' }
]

// 预定义的可拖拽元素
const availableElements = [
  // 电子设备
  { name: '电脑', icon: '💻', category: 'electronics' },
  { name: '手机', icon: '📱', category: 'electronics' },
  { name: '平板', icon: '📟', category: 'electronics' },
  { name: '耳机', icon: '🎧', category: 'electronics' },
  { name: '相机', icon: '📷', category: 'electronics' },
  { name: '台灯', icon: '💡', category: 'electronics' },
  { name: '充电宝', icon: '🔋', category: 'electronics' },
  
  // 家具
  { name: '柜子', icon: '🗄️', category: 'furniture', isCabinet: true },
  { name: '抽屉', icon: '🗃️', category: 'furniture', isCabinet: true },
  { name: '书架', icon: '📚', category: 'furniture' },
  { name: '椅子', icon: '🪑', category: 'furniture' },
  
  // 文具
  { name: '笔记本', icon: '📓', category: 'stationery' },
  { name: '书本', icon: '📕', category: 'stationery' },
  { name: '铅笔', icon: '✏️', category: 'stationery' },
  { name: '钢笔', icon: '🖋️', category: 'stationery' },
  { name: '橡皮', icon: '🧽', category: 'stationery' },
  { name: '订书机', icon: '🖇️', category: 'stationery' },
  { name: '文件夹', icon: '📁', category: 'stationery' },
  
  // 装饰品
  { name: '绿植', icon: '🌱', category: 'decorations' },
  { name: '相框', icon: '🖼️', category: 'decorations' },
  { name: '时钟', icon: '⏰', category: 'decorations' },
  { name: '咖啡杯', icon: '☕', category: 'decorations' },
  { name: '水杯', icon: '🥤', category: 'decorations' },
  { name: '纸巾', icon: '🧻', category: 'decorations' },
  { name: '闹钟', icon: '⏱️', category: 'decorations' }
]

// 获取过滤后的元素列表
const getFilteredElements = () => {
  if (activeCategory.value === 'all') {
    return availableElements
  }
  return availableElements.filter(el => el.category === activeCategory.value)
}

// 获取桌面的3D样式
const getDesktopStyle = () => {
  return {
    background: background.value,
    // 桌面3D变换
    transform: 'perspective(1000px) rotateX(3deg) translateY(-20px)',
    // 添加深度和纹理
    boxShadow: '0 30px 40px rgba(0,0,0,0.2), 0 0 0 1px rgba(0,0,0,0.1)',
    // 木质纹理覆盖
    backgroundImage: `linear-gradient(45deg, rgba(222, 184, 135, 0.1) 25%, transparent 25%), 
                      linear-gradient(-45deg, rgba(222, 184, 135, 0.1) 25%, transparent 25%), 
                      linear-gradient(45deg, transparent 75%, rgba(222, 184, 135, 0.1) 75%), 
                      linear-gradient(-45deg, transparent 75%, rgba(222, 184, 135, 0.1) 75%)`,
    backgroundSize: '20px 20px',
    backgroundPosition: '0 0, 0 10px, 10px -10px, -10px 0px'
  }
}

// 获取元素的3D变换
const getElementTransform = (element: DesktopElement) => {
  const rotation = element.rotation || 0
  const scale = element.scale || 1
  const rotationX = element.rotationX || 0
  const rotationY = element.rotationY || 0
  
  return `rotate(${rotation}deg) scale(${scale}) perspective(1000px) rotateX(${rotationX}deg) rotateY(${rotationY}deg)`
}

// 获取元素的3D样式
const getElement3DStyle = (element: DesktopElement) => {
  // 基础样式
  const baseStyle: any = {
    backgroundColor: 'white',
    // 添加深度和阴影
    boxShadow: '0 5px 15px rgba(0,0,0,0.15), 0 0 0 1px rgba(0,0,0,0.05)',
    // 3D变换
    transformStyle: 'preserve-3d',
    transition: 'all 0.3s ease'
  }
  
  // 根据元素类型设置不同的3D效果
  if (element.isCabinet) {
    // 柜子特殊样式
    baseStyle.backgroundColor = '#deb887'
    baseStyle.borderRadius = '8px'
    baseStyle.boxShadow = '0 10px 20px rgba(0,0,0,0.2), 0 0 0 1px rgba(0,0,0,0.1)'
    baseStyle.padding = '10px'
    baseStyle.border = '2px solid #bc8f8f'
    // 柜子纹理
    baseStyle.backgroundImage = `linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px), linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px)`
    baseStyle.backgroundSize = '10px 10px'
  } else if (element.category === 'electronics') {
    // 电子设备样式
    baseStyle.backgroundColor = '#2d3748'
    baseStyle.color = 'white'
    baseStyle.borderRadius = '6px'
    baseStyle.boxShadow = '0 8px 16px rgba(0,0,0,0.25)'
  } else if (element.category === 'stationery') {
    // 书本样式
    baseStyle.backgroundColor = '#f8f9fa'
    baseStyle.borderRadius = '2px'
    baseStyle.boxShadow = '0 3px 10px rgba(0,0,0,0.2)'
    baseStyle.borderLeft = '8px solid #3182ce'
  }
  
  return baseStyle
}

// 元素面板相关函数
const onElementDragStart = (element: any, event: DragEvent) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('text/plain', JSON.stringify(element))
    event.dataTransfer.effectAllowed = 'copy'
  }
}

const onElementClick = (element: any) => {
  // 点击元素面板中的元素时，自动添加到桌面中央
  if (desktopCanvas.value) {
    const rect = desktopCanvas.value.getBoundingClientRect()
    const x = rect.width / 2 - 25
    const y = rect.height / 2 - 25
    
    const newElement: DesktopElement = {
      ...element,
      id: Date.now(),
      x: Math.max(0, Math.min(x, rect.width - 50)),
      y: Math.max(0, Math.min(y, rect.height - 50)),
      rotation: 0,
      scale: 1,
      zIndex: elements.value.length + 1,
      size: element.size || 2,
      depth: element.isCabinet ? 50 : 20,
      rotationX: 0,
      rotationY: 0,
      material: element.isCabinet ? 'wood' : 'plastic'
    }
    
    elements.value.push(newElement)
    emit('update:elements', elements.value)
  }
}

// 拖拽相关函数
const onDragOver = (event: DragEvent) => {
  event.preventDefault()
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = 'copy'
  }
}

const onDrop = (event: DragEvent) => {
  event.preventDefault()
  
  if (event.dataTransfer) {
    const elementData = JSON.parse(event.dataTransfer.getData('text/plain'))
    
    if (desktopCanvas.value) {
      const rect = desktopCanvas.value.getBoundingClientRect()
      const x = event.clientX - rect.left - 25
      const y = event.clientY - rect.top - 25
      
      // 创建新元素实例
      const newElement: DesktopElement = {
        ...elementData,
        id: Date.now(),
        x: Math.max(0, Math.min(x, rect.width - 50)),
        y: Math.max(0, Math.min(y, rect.height - 50)),
        rotation: 0,
        scale: 1,
        zIndex: elements.value.length + 1,
        size: elementData.size || 2,
        // 初始化3D属性
        depth: elementData.isCabinet ? 50 : 20,
        rotationX: 0,
        rotationY: 0,
        material: elementData.isCabinet ? 'wood' : 'plastic'
      }
      
      elements.value.push(newElement)
      emit('update:elements', elements.value)
    }
  }
}

// 元素拖拽
let isDragging = false
const dragOffset = { x: 0, y: 0 }

const startDrag = (element: DesktopElement, event: MouseEvent) => {
  isDragging = true
  
  // 拖拽时不选中元素，避免编辑面板出现
  const draggingElement = element
  
  dragOffset.x = event.clientX - element.x
  dragOffset.y = event.clientY - element.y
  
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
  
  // 拖拽时直接更新元素位置，不通过selectedElement
  function onDrag(event: MouseEvent) {
    if (isDragging && desktopCanvas.value) {
      const rect = desktopCanvas.value.getBoundingClientRect()
      const x = event.clientX - dragOffset.x
      const y = event.clientY - dragOffset.y
      
      draggingElement.x = Math.max(0, Math.min(x, rect.width - 50))
      draggingElement.y = Math.max(0, Math.min(y, rect.height - 50))
      
      emit('update:elements', elements.value)
    }
  }
}

const stopDrag = () => {
  isDragging = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 取消选择元素
const deselectElement = () => {
  selectedElement.value = null
  contextMenu.visible = false
  emit('elementSelected', null)
}

// 右键菜单
const showContextMenu = (event: MouseEvent, element: DesktopElement) => {
  event.preventDefault()
  contextMenu.visible = true
  contextMenu.x = event.clientX
  contextMenu.y = event.clientY
  contextMenu.element = element
  // 右键点击元素时不自动选中，只在选择编辑选项时才选中
}

// 编辑元素
const editElement = () => {
  if (contextMenu.element) {
    selectedElement.value = contextMenu.element
    contextMenu.visible = false
    emit('elementSelected', contextMenu.element)
  }
}

// 删除元素
const deleteElement = () => {
  if (contextMenu.element) {
    elements.value = elements.value.filter(
      el => el.id !== contextMenu.element!.id
    )
    contextMenu.visible = false
    selectedElement.value = null
    emit('update:elements', elements.value)
    emit('elementSelected', null)
  }
}

// 复制元素
const duplicateElement = () => {
  if (contextMenu.element) {
    const original = contextMenu.element
    const newElement: DesktopElement = {
      ...original,
      id: Date.now(),
      x: original.x + 20,
      y: original.y + 20,
      zIndex: elements.value.length + 1,
      // 复制3D属性
      depth: original.depth || 20,
      rotationX: original.rotationX || 0,
      rotationY: original.rotationY || 0,
      material: original.material || 'plastic'
    }
    elements.value.push(newElement)
    contextMenu.visible = false
    emit('update:elements', elements.value)
  }
}

// 旋转元素
const rotateElement = (angle: number) => {
  if (contextMenu.element) {
    contextMenu.element.rotation = (contextMenu.element.rotation + angle) % 360
    contextMenu.visible = false
    emit('update:elements', elements.value)
  }
}

// 层级控制
const bringToFront = () => {
  if (contextMenu.element) {
    const maxZIndex = Math.max(...elements.value.map(el => el.zIndex))
    contextMenu.element.zIndex = maxZIndex + 1
    contextMenu.visible = false
    emit('update:elements', elements.value)
  }
}

const sendToBack = () => {
  if (contextMenu.element) {
    const minZIndex = Math.min(...elements.value.map(el => el.zIndex))
    contextMenu.element.zIndex = Math.max(1, minZIndex - 1)
    contextMenu.visible = false
    emit('update:elements', elements.value)
  }
}

// 清空桌面
const clearDesktop = () => {
  if (confirm('确定要清空桌面吗？此操作不可撤销。')) {
    elements.value = []
    selectedElement.value = null
    contextMenu.visible = false
    emit('update:elements', [])
    emit('elementSelected', null)
  }
}

// 保存配置
const saveDesktop = () => {
  const config = {
    background: props.background,
    elements: elements.value,
    timestamp: new Date().toISOString()
  }
  
  localStorage.setItem('desktop-config', JSON.stringify(config))
  emit('save', config)
  
  // 显示成功提示
  alert('桌面配置已保存！')
}

// 下载图片
const downloadImage = async () => {
  if (typeof window !== 'undefined') {
    try {
      // 动态导入html2canvas
      const html2canvas = (await import('html2canvas')).default;
      
      if (desktopCanvas.value) {
        const canvas = await html2canvas(desktopCanvas.value, {
          scale: 2, // 提高清晰度
          useCORS: true,
          allowTaint: true,
          logging: false
        });
        
        // 创建下载链接
        const link = document.createElement('a');
        link.download = `桌面设计_${new Date().toLocaleDateString()}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
      }
    } catch (error) {
      console.error('下载图片失败:', error);
      alert('导出图片失败，请确保已安装html2canvas库。');
    }
  }
}

// 点击其他地方关闭右键菜单
const closeContextMenu = (event: MouseEvent) => {
  if (contextMenu.visible) {
    contextMenu.visible = false
  }
}

// 生命周期
onMounted(() => {
  document.addEventListener('click', closeContextMenu)
  
  // 加载保存的配置
  const savedConfig = localStorage.getItem('desktop-config')
  if (savedConfig) {
    try {
      const config = JSON.parse(savedConfig)
      elements.value = config.elements || []
      // 为已保存的元素添加3D属性
      elements.value.forEach(el => {
        if (!el.depth) el.depth = 20
        if (el.isCabinet && !el.depth) el.depth = 50
        if (el.rotationX === undefined) el.rotationX = 0
        if (el.rotationY === undefined) el.rotationY = 0
        if (!el.material) el.material = el.isCabinet ? 'wood' : 'plastic'
      })
      emit('update:elements', elements.value)
    } catch (error) {
      console.error('加载配置失败:', error)
    }
  }
})

onUnmounted(() => {
  document.removeEventListener('click', closeContextMenu)
})

// 处理背景变化
const onBackgroundChange = (newBackground: string) => {
  background.value = newBackground
}

// 监听属性变化
watch(() => props.initialElements, (newElements) => {
  elements.value = newElements
  // 为初始元素添加3D属性
  elements.value.forEach(el => {
    if (!el.depth) el.depth = 20
    if (el.isCabinet && !el.depth) el.depth = 50
    if (el.rotationX === undefined) el.rotationX = 0
    if (el.rotationY === undefined) el.rotationY = 0
    if (!el.material) el.material = el.isCabinet ? 'wood' : 'plastic'
  })
}, { immediate: true })

// 监听props中的背景变化
watch(() => props.background, (newBg) => {
  background.value = newBg
}, { immediate: true })

// 暴露方法给父组件
defineExpose({
  clearDesktop,
  saveDesktop,
  downloadImage,
  getElements: () => elements.value
})
</script>

<style scoped>
/* 3D透视容器 */
.perspective-container {
  perspective: 1500px;
  margin: 20px 0;
  width: 100%;
  height: auto;
}

/* 桌面样式增强 */
.desktop-edge {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 20px;
  background: #deb887;
  transform: translateY(100%) rotateX(90deg);
  transform-origin: top;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.desktop-legs {
  position: absolute;
  bottom: -20px;
  left: 50px;
  right: 50px;
  height: 50px;
  background: #8b4513;
  transform: translateY(100%);
  z-index: -1;
}

/* 元素底部底座，增强立体感 */
.element-base {
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%) rotateX(90deg);
  width: 80%;
  height: 10px;
  background: rgba(0,0,0,0.1);
  border-radius: 50%;
  z-index: -1;
}

/* 悬停缩放效果 */
.hover-scale {
  transform: translateY(-5px) !important;
  box-shadow: 0 15px 30px rgba(0,0,0,0.2) !important;
}

/* 鼠标样式 */
.cursor-move {
  cursor: move;
}

.cursor-move:active {
  cursor: grabbing;
}

/* 平滑过渡效果 */
.absolute {
  transition: transform 0.1s ease-out, z-index 0s linear 0.1s;
}

/* 3D变换支持 */
* {
  transform-style: preserve-3d;
}

/* 桌面画布样式增强 */
.desktop-canvas-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

/* 工具栏样式 */
.toolbar {
  background-color: white;
  border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 16px;
}

/* 元素项样式 */
.element-item {
  transition: all 0.2s ease;
}

.element-item:hover {
  transform: translateY(-2px);
}

/* 输入滑块样式 */
input[type="range"] {
  -webkit-appearance: none;
  height: 6px;
  border-radius: 3px;
  background: #e5e7eb;
  outline: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: none;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .desktop-builder {
    padding: 1rem;
  }
  
  .perspective-container {
    perspective: 1000px;
  }
  
  .desktop-canvas-container {
    height: 400px !important;
  }
}

@media (max-width: 768px) {
  .desktop-builder {
    padding: 0.5rem;
  }
  
  .grid {
    grid-template-columns: 1fr !important;
    gap: 16px;
  }
  
  .lg\:col-span-3,
  .lg\:col-span-1 {
    grid-column: span 1 !important;
  }
  
  .toolbar {
    flex-direction: column;
    gap: 12px;
  }
  
  .toolbar .flex.space-x-2 {
    width: 100%;
    justify-content: space-between;
  }
  
  .desktop-canvas-container {
    height: 350px !important;
  }
  
  .perspective-container {
    perspective: 800px;
    margin: 10px 0;
  }
}

@media (max-width: 480px) {
  .desktop-canvas-container {
    height: 300px !important;
  }
  
  .toolbar .flex.space-x-2 {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .toolbar .flex.space-x-2 button {
    flex: 1;
    min-width: calc(50% - 4px);
  }
  
  .grid.grid-cols-2 {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* 右键菜单动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>