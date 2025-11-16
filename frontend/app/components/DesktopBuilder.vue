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

    <!-- 桌面画布 -->
    <div 
      ref="desktopCanvas"
      class="relative w-full h-96 rounded-lg border-2 border-dashed border-gray-300 overflow-hidden"
      :style="{ background: background }"
      @dragover="onDragOver"
      @drop="onDrop"
    >
      <!-- 放置的元素 -->
      <div 
        v-for="element in elements" 
        :key="element.id"
        class="absolute cursor-move select-none"
        :style="{
          left: element.x + 'px',
          top: element.y + 'px',
          transform: `rotate(${element.rotation}deg) scale(${element.scale})`,
          zIndex: element.zIndex
        }"
        @mousedown="startDrag(element, $event)"
        @contextmenu.prevent="showContextMenu($event, element)"
      >
        <div 
          :class="[
            'p-2 rounded-lg shadow-lg border-2 transition-all',
            selectedElement?.id === element.id 
              ? 'border-blue-500 ring-2 ring-blue-200' 
              : 'border-blue-200'
          ]"
          :style="{ 
            fontSize: `${element.size || 2}rem`,
            backgroundColor: 'white'
          }"
        >
          {{ element.icon }}
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
// 定义元素接口
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

// 桌面元素
const elements = ref<DesktopElement[]>(props.initialElements)

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
        size: 2
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
      zIndex: elements.value.length + 1
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
      emit('update:elements', elements.value)
    } catch (error) {
      console.error('加载配置失败:', error)
    }
  }
})

onUnmounted(() => {
  document.removeEventListener('click', closeContextMenu)
})

// 监听属性变化
watch(() => props.initialElements, (newElements) => {
  elements.value = newElements
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
.cursor-move {
  cursor: move;
}

.cursor-move:active {
  cursor: grabbing;
}

/* 平滑过渡效果 */
.absolute {
  transition: transform 0.1s ease-out;
}
</style>