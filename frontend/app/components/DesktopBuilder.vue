<template>
  <div class="desktop-builder">
    <!-- 桌面工具栏 -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold text-gray-800">我的桌面</h2>
      <div class="flex space-x-2">
        <button 
          @click="clearDesktop"
          class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
        >
          清空桌面
        </button>
        <button 
          @click="saveDesktop"
          class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
        >
          保存配置
        </button>
        <button 
          @click="downloadImage"
          class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
        >
          下载图片
        </button>
      </div>
    </div>

    <!-- 桌面画布容器 - 添加3D透视效果 -->
    <div class="perspective-container">
      <!-- 桌面画布 - 改为3D立体桌面 -->
      <div 
        ref="desktopCanvas"
        class="relative w-full h-[500px] rounded-lg border-2 border-gray-300 overflow-hidden shadow-xl"
        :style="getDesktopStyle()"
        @dragover="onDragOver"
        @drop="onDrop"
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
              <!-- 添加元素底部阴影，增强立体感 -->
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

    <!-- 操作提示 -->
    <div class="mt-4 text-sm text-gray-600">
      <p>💡 提示：拖拽元素到桌面，右键点击元素可进行旋转、缩放等操作</p>
    </div>

    <!-- 右键菜单 -->
    <div 
      v-if="contextMenu.visible"
      class="fixed bg-white shadow-lg rounded-lg py-2 z-50 min-w-32"
      :style="{ left: contextMenu.x + 'px', top: contextMenu.y + 'px' }"
    >
      <button 
        @click="deleteElement"
        class="w-full px-4 py-2 text-left text-red-600 hover:bg-red-50 flex items-center"
      >
        <span class="mr-2">🗑️</span> 删除元素
      </button>
      <button 
        @click="duplicateElement"
        class="w-full px-4 py-2 text-left text-blue-600 hover:bg-blue-50 flex items-center"
      >
        <span class="mr-2">📋</span> 复制元素
      </button>
      <div class="border-t my-1"></div>
      <button 
        @click="bringToFront"
        class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
      >
        <span class="mr-2">⬆️</span> 置顶
      </button>
      <button 
        @click="sendToBack"
        class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
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
  isCabinet?: boolean
  // 新增3D相关属性
  depth?: number
  rotationX?: number
  rotationY?: number
  material?: string
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

// 桌面元素
const elements = ref<DesktopElement[]>(props.initialElements)

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
    baseStyle.backgroundImage = `linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px), 
                               linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px)`,
    baseStyle.backgroundSize = '10px 10px'
  } else if (element.name.includes('电脑') || element.name.includes('手机')) {
    // 电子设备样式
    baseStyle.backgroundColor = '#2d3748'
    baseStyle.color = 'white'
    baseStyle.borderRadius = '6px'
    baseStyle.boxShadow = '0 8px 16px rgba(0,0,0,0.25)'
  } else if (element.name.includes('书本') || element.name.includes('笔记本')) {
    // 书本样式
    baseStyle.backgroundColor = '#f8f9fa'
    baseStyle.borderRadius = '2px'
    baseStyle.boxShadow = '0 3px 10px rgba(0,0,0,0.2)'
    baseStyle.borderLeft = '8px solid #3182ce'
  }
  
  return baseStyle
}

// 拖拽相关函数
const onDragStart = (event: DragEvent, element: DesktopElement) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('text/plain', JSON.stringify(element))
    event.dataTransfer.effectAllowed = 'copy'
  }
}

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
let dragOffset = { x: 0, y: 0 }

const startDrag = (element: DesktopElement, event: MouseEvent) => {
  isDragging = true
  selectedElement.value = element
  
  dragOffset.x = event.clientX - element.x
  dragOffset.y = event.clientY - element.y
  
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
  
  emit('elementSelected', element)
}

const onDrag = (event: MouseEvent) => {
  if (isDragging && selectedElement.value && desktopCanvas.value) {
    const rect = desktopCanvas.value.getBoundingClientRect()
    const x = event.clientX - dragOffset.x
    const y = event.clientY - dragOffset.y
    
    selectedElement.value.x = Math.max(0, Math.min(x, rect.width - 50))
    selectedElement.value.y = Math.max(0, Math.min(y, rect.height - 50))
    
    emit('update:elements', elements.value)
  }
}

const stopDrag = () => {
  isDragging = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 右键菜单
const showContextMenu = (event: MouseEvent, element: DesktopElement) => {
  event.preventDefault()
  contextMenu.visible = true
  contextMenu.x = event.clientX
  contextMenu.y = event.clientY
  contextMenu.element = element
  selectedElement.value = element
  
  emit('elementSelected', element)
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

// 层级控制
const bringToFront = () => {
  if (selectedElement.value) {
    const maxZIndex = Math.max(...elements.value.map(el => el.zIndex))
    selectedElement.value.zIndex = maxZIndex + 1
    contextMenu.visible = false
    emit('update:elements', elements.value)
  }
}

const sendToBack = () => {
  if (selectedElement.value) {
    const minZIndex = Math.min(...elements.value.map(el => el.zIndex))
    selectedElement.value.zIndex = Math.max(1, minZIndex - 1)
    contextMenu.visible = false
    emit('update:elements', elements.value)
  }
}

// 清空桌面
const clearDesktop = () => {
  elements.value = []
  selectedElement.value = null
  emit('update:elements', [])
  emit('elementSelected', null)
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
const downloadImage = () => {
  // 这里可以集成html2canvas等库来实现图片导出
  // 目前先提供一个简单的提示
  alert('导出图片功能需要集成html2canvas库，这里仅作演示。在实际项目中，可以使用html2canvas将画布内容转换为图片。')
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
</style>
<template>
  <div class="desktop-builder">
    <!-- 桌面工具栏 -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold text-gray-800">我的桌面</h2>
      <div class="flex space-x-2">
        <button 
          @click="clearDesktop"
          class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
        >
          清空桌面
        </button>
        <button 
          @click="saveDesktop"
          class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
        >
          保存配置
        </button>
        <button 
          @click="downloadImage"
          class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
        >
          下载图片
        </button>
      </div>
    </div>

    <!-- 桌面画布容器 - 添加3D透视效果 -->
    <div class="perspective-container">
      <!-- 桌面画布 - 改为3D立体桌面 -->
      <div 
        ref="desktopCanvas"
        class="relative w-full h-[500px] rounded-lg border-2 border-gray-300 overflow-hidden shadow-xl"
        :style="getDesktopStyle()"
        @dragover="onDragOver"
        @drop="onDrop"
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
              <!-- 添加元素底部阴影，增强立体感 -->
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

    <!-- 操作提示 -->
    <div class="mt-4 text-sm text-gray-600">
      <p>💡 提示：拖拽元素到桌面，右键点击元素可进行旋转、缩放等操作</p>
    </div>

    <!-- 右键菜单 -->
    <div 
      v-if="contextMenu.visible"
      class="fixed bg-white shadow-lg rounded-lg py-2 z-50 min-w-32"
      :style="{ left: contextMenu.x + 'px', top: contextMenu.y + 'px' }"
    >
      <button 
        @click="deleteElement"
        class="w-full px-4 py-2 text-left text-red-600 hover:bg-red-50 flex items-center"
      >
        <span class="mr-2">🗑️</span> 删除元素
      </button>
      <button 
        @click="duplicateElement"
        class="w-full px-4 py-2 text-left text-blue-600 hover:bg-blue-50 flex items-center"
      >
        <span class="mr-2">📋</span> 复制元素
      </button>
      <div class="border-t my-1"></div>
      <button 
        @click="bringToFront"
        class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
      >
        <span class="mr-2">⬆️</span> 置顶
      </button>
      <button 
        @click="sendToBack"
        class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
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
  isCabinet?: boolean
  // 新增3D相关属性
  depth?: number
  rotationX?: number
  rotationY?: number
  material?: string
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

// 桌面元素
const elements = ref<DesktopElement[]>(props.initialElements)

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
    baseStyle.backgroundImage = `linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px), 
                               linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px)`,
    baseStyle.backgroundSize = '10px 10px'
  } else if (element.name.includes('电脑') || element.name.includes('手机')) {
    // 电子设备样式
    baseStyle.backgroundColor = '#2d3748'
    baseStyle.color = 'white'
    baseStyle.borderRadius = '6px'
    baseStyle.boxShadow = '0 8px 16px rgba(0,0,0,0.25)'
  } else if (element.name.includes('书本') || element.name.includes('笔记本')) {
    // 书本样式
    baseStyle.backgroundColor = '#f8f9fa'
    baseStyle.borderRadius = '2px'
    baseStyle.boxShadow = '0 3px 10px rgba(0,0,0,0.2)'
    baseStyle.borderLeft = '8px solid #3182ce'
  }
  
  return baseStyle
}

// 拖拽相关函数
const onDragStart = (event: DragEvent, element: DesktopElement) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('text/plain', JSON.stringify(element))
    event.dataTransfer.effectAllowed = 'copy'
  }
}

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
let dragOffset = { x: 0, y: 0 }

const startDrag = (element: DesktopElement, event: MouseEvent) => {
  isDragging = true
  selectedElement.value = element
  
  dragOffset.x = event.clientX - element.x
  dragOffset.y = event.clientY - element.y
  
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
  
  emit('elementSelected', element)
}

const onDrag = (event: MouseEvent) => {
  if (isDragging && selectedElement.value && desktopCanvas.value) {
    const rect = desktopCanvas.value.getBoundingClientRect()
    const x = event.clientX - dragOffset.x
    const y = event.clientY - dragOffset.y
    
    selectedElement.value.x = Math.max(0, Math.min(x, rect.width - 50))
    selectedElement.value.y = Math.max(0, Math.min(y, rect.height - 50))
    
    emit('update:elements', elements.value)
  }
}

const stopDrag = () => {
  isDragging = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 右键菜单
const showContextMenu = (event: MouseEvent, element: DesktopElement) => {
  event.preventDefault()
  contextMenu.visible = true
  contextMenu.x = event.clientX
  contextMenu.y = event.clientY
  contextMenu.element = element
  selectedElement.value = element
  
  emit('elementSelected', element)
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

// 层级控制
const bringToFront = () => {
  if (selectedElement.value) {
    const maxZIndex = Math.max(...elements.value.map(el => el.zIndex))
    selectedElement.value.zIndex = maxZIndex + 1
    contextMenu.visible = false
    emit('update:elements', elements.value)
  }
}

const sendToBack = () => {
  if (selectedElement.value) {
    const minZIndex = Math.min(...elements.value.map(el => el.zIndex))
    selectedElement.value.zIndex = Math.max(1, minZIndex - 1)
    contextMenu.visible = false
    emit('update:elements', elements.value)
  }
}

// 清空桌面
const clearDesktop = () => {
  elements.value = []
  selectedElement.value = null
  emit('update:elements', [])
  emit('elementSelected', null)
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
const downloadImage = () => {
  // 这里可以集成html2canvas等库来实现图片导出
  // 目前先提供一个简单的提示
  alert('导出图片功能需要集成html2canvas库，这里仅作演示。在实际项目中，可以使用html2canvas将画布内容转换为图片。')
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
</style>
<template>
  <div class="desktop-builder">
    <!-- 桌面工具栏 -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold text-gray-800">我的桌面</h2>
      <div class="flex space-x-2">
        <button 
          @click="clearDesktop"
          class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
        >
          清空桌面
        </button>
        <button 
          @click="saveDesktop"
          class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
        >
          保存配置
        </button>
        <button 
          @click="downloadImage"
          class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
        >
          下载图片
        </button>
      </div>
    </div>

    <!-- 桌面画布容器 - 添加3D透视效果 -->
    <div class="perspective-container">
      <!-- 桌面画布 - 改为3D立体桌面 -->
      <div 
        ref="desktopCanvas"
        class="relative w-full h-[500px] rounded-lg border-2 border-gray-300 overflow-hidden shadow-xl"
        :style="getDesktopStyle()"
        @dragover="onDragOver"
        @drop="onDrop"
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
              <!-- 添加元素底部阴影，增强立体感 -->
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

    <!-- 操作提示 -->
    <div class="mt-4 text-sm text-gray-600">
      <p>💡 提示：拖拽元素到桌面，右键点击元素可进行旋转、缩放等操作</p>
    </div>

    <!-- 右键菜单 -->
    <div 
      v-if="contextMenu.visible"
      class="fixed bg-white shadow-lg rounded-lg py-2 z-50 min-w-32"
      :style="{ left: contextMenu.x + 'px', top: contextMenu.y + 'px' }"
    >
      <button 
        @click="deleteElement"
        class="w-full px-4 py-2 text-left text-red-600 hover:bg-red-50 flex items-center"
      >
        <span class="mr-2">🗑️</span> 删除元素
      </button>
      <button 
        @click="duplicateElement"
        class="w-full px-4 py-2 text-left text-blue-600 hover:bg-blue-50 flex items-center"
      >
        <span class="mr-2">📋</span> 复制元素
      </button>
      <div class="border-t my-1"></div>
      <button 
        @click="bringToFront"
        class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
      >
        <span class="mr-2">⬆️</span> 置顶
      </button>
      <button 
        @click="sendToBack"
        class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
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
  isCabinet?: boolean
  // 新增3D相关属性
  depth?: number
  rotationX?: number
  rotationY?: number
  material?: string
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

// 桌面元素
const elements = ref<DesktopElement[]>(props.initialElements)

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
    baseStyle.backgroundImage = `linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px), 
                               linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px)`,
    baseStyle.backgroundSize = '10px 10px'
  } else if (element.name.includes('电脑') || element.name.includes('手机')) {
    // 电子设备样式
    baseStyle.backgroundColor = '#2d3748'
    baseStyle.color = 'white'
    baseStyle.borderRadius = '6px'
    baseStyle.boxShadow = '0 8px 16px rgba(0,0,0,0.25)'
  } else if (element.name.includes('书本') || element.name.includes('笔记本')) {
    // 书本样式
    baseStyle.backgroundColor = '#f8f9fa'
    baseStyle.borderRadius = '2px'
    baseStyle.boxShadow = '0 3px 10px rgba(0,0,0,0.2)'
    baseStyle.borderLeft = '8px solid #3182ce'
  }
  
  return baseStyle
}

// 拖拽相关函数
const onDragStart = (event: DragEvent, element: DesktopElement) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('text/plain', JSON.stringify(element))
    event.dataTransfer.effectAllowed = 'copy'
  }
}

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
let dragOffset = { x: 0, y: 0 }

const startDrag = (element: DesktopElement, event: MouseEvent) => {
  isDragging = true
  selectedElement.value = element
  
  dragOffset.x = event.clientX - element.x
  dragOffset.y = event.clientY - element.y
  
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
  
  emit('elementSelected', element)
}

const onDrag = (event: MouseEvent) => {
  if (isDragging && selectedElement.value && desktopCanvas.value) {
    const rect = desktopCanvas.value.getBoundingClientRect()
    const x = event.clientX - dragOffset.x
    const y = event.clientY - dragOffset.y
    
    selectedElement.value.x = Math.max(0, Math.min(x, rect.width - 50))
    selectedElement.value.y = Math.max(0, Math.min(y, rect.height - 50))
    
    emit('update:elements', elements.value)
  }
}

const stopDrag = () => {
  isDragging = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 右键菜单
const showContextMenu = (event: MouseEvent, element: DesktopElement) => {
  event.preventDefault()
  contextMenu.visible = true
  contextMenu.x = event.clientX
  contextMenu.y = event.clientY
  contextMenu.element = element
  selectedElement.value = element
  
  emit('elementSelected', element)
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

// 层级控制
const bringToFront = () => {
  if (selectedElement.value) {
    const maxZIndex = Math.max(...elements.value.map(el => el.zIndex))
    selectedElement.value.zIndex = maxZIndex + 1
    contextMenu.visible = false
    emit('update:elements', elements.value)
  }
}

const sendToBack = () => {
  if (selectedElement.value) {
    const minZIndex = Math.min(...elements.value.map(el => el.zIndex))
    selectedElement.value.zIndex = Math.max(1, minZIndex - 1)
    contextMenu.visible = false
    emit('update:elements', elements.value)
  }
}

// 清空桌面
const clearDesktop = () => {
  elements.value = []
  selectedElement.value = null
  emit('update:elements', [])
  emit('elementSelected', null)
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
const downloadImage = () => {
  // 这里可以集成html2canvas等库来实现图片导出
  // 目前先提供一个简单的提示
  alert('导出图片功能需要集成html2canvas库，这里仅作演示。在实际项目中，可以使用html2canvas将画布内容转换为图片。')
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
</style>