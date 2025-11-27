<template>
  <div class="desktop-builder min-h-screen bg-gray-50 p-6">
    <!-- 页面标题 -->
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">寝室桌面搭建</h1>
      <p class="text-gray-600">拖拽元素到桌面，打造你的专属学习环境</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 max-w-full mx-auto">
      <!-- 左侧：元素面板 -->
      <div class="lg:col-span-1">
        <ElementPanel
          :categories="elementCategories"
          :elements="availableElements"
          :active-category="activeCategory"
          @category-change="activeCategory = $event"
          @element-drag-start="onElementDragStart"
          @element-click="onElementClick"
        />
      </div>

      <!-- 中间：桌面构建区 -->
      <div class="lg:col-span-3">
        <!-- 桌面工具 -->
        <Toolbar
          @clear="clearDesktop"
          @save="saveDesktop"
          @download="downloadImage"
        />

        <!-- 选中元素的编辑面板 -->
        <ElementEditor
          :element="selectedElement"
          @update:rotation="updateElementRotation"
          @update:size="updateElementSize"
        />

        <!-- 桌面画布 -->
        <DesktopCanvas
          :elements="elements"
          :background="background"
          :height="800"
          :selected-element-id="selectedElement?.id"
          :hovered-element-id="elementHovered"
          @drag-over="onDragOver"
          @drop="onDrop"
          @deselect-element="deselectElement"
          @element-drag-start="startDrag"
          @context-menu-show="showContextMenu"
          @element-hover="elementHovered = $event !== null ? String($event) : null"
          ref="desktopCanvasRef"
        />
      </div>
    </div>

    <!-- 操作提示 -->
    <div class="mt-4 text-sm text-gray-600 text-center">
      <p>💡 提示：拖拽元素到桌面，右键点击元素并选择"编辑元素"进行属性调整</p>
    </div>

    <!-- 右键菜单 -->
    <ContextMenu
      :visible="contextMenu.visible"
      :x="contextMenu.x"
      :y="contextMenu.y"
      @edit="editElement"
      @duplicate="duplicateElement"
      @delete="deleteElement"
      @rotate="rotateElement"
      @bring-to-front="bringToFront"
      @send-to-back="sendToBack"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import ElementPanel from '../components/ElementPanel.vue'
import DesktopCanvas from '../components/DesktopCanvas.vue'
import Toolbar from '../components/Toolbar.vue'
import ElementEditor from '../components/ElementEditor.vue'
import ContextMenu from '../components/ContextMenu.vue'
import type { DesktopElement, ElementCategory, DraggableElement, ContextMenuState, DesktopConfig } from '../components/types'

// 定义组件属�?
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
  background: '/桌面程序贴图/桌面/微信图片_20251117210350_46_979.jpg',
  initialElements: () => []
})

// 组件事件
const emit = defineEmits<Emits>()

// 响应式数�?
const desktopCanvasRef = ref<InstanceType<typeof DesktopCanvas>>()
const selectedElement = ref<DesktopElement | null>(null)
const elementHovered = ref<string | null>(null)
const draggingElement = ref<DesktopElement | null>(null)
const dragOffset = ref({ x: 0, y: 0 })
const background = ref(props.background)
const activeCategory = ref('electronics')
const contextMenu = reactive<ContextMenuState>({
  visible: false,
  x: 0,
  y: 0,
  element: null
})

// 桌面元素
const elements = ref<DesktopElement[]>(props.initialElements)

// 预定义的元素类别
const elementCategories: ElementCategory[] = [
  { id: 'electronics', name: '电子设备' },
  { id: 'study', name: '学习资料' },
  { id: 'tools', name: '小工具' },
  { id: 'daily', name: '生活用品' }
]

// 预定义的可拖拽元素
const availableElements = [
  // 电子设备 - 电脑套装
  { name: '电脑1', icon: '/桌面程序贴图/电子设备/电脑 (1).png', category: 'electronics' },
  { name: '电脑2', icon: '/桌面程序贴图/电子设备/电脑 (2).png', category: 'electronics' },
  { name: '电脑3', icon: '/桌面程序贴图/电子设备/电脑 (3).png', category: 'electronics' },
  { name: '键盘1', icon: '/桌面程序贴图/电子设备/键盘 (1).png', category: 'electronics' },
  { name: '键盘2', icon: '/桌面程序贴图/电子设备/键盘 (2).png', category: 'electronics' },
  { name: '键盘3', icon: '/桌面程序贴图/电子设备/键盘 (3).png', category: 'electronics' },
  { name: '键盘4', icon: '/桌面程序贴图/电子设备/键盘 (4).png', category: 'electronics' },
  { name: '键盘5', icon: '/桌面程序贴图/电子设备/键盘 (5).png', category: 'electronics' },
  { name: '键盘6', icon: '/桌面程序贴图/电子设备/键盘 (6).png', category: 'electronics' },
  { name: '鼠标1', icon: '/桌面程序贴图/电子设备/鼠标  (1).png', category: 'electronics' },
  { name: '鼠标2', icon: '/桌面程序贴图/电子设备/鼠标  (2).png', category: 'electronics' },
  { name: '鼠标3', icon: '/桌面程序贴图/电子设备/鼠标  (3).png', category: 'electronics' },
  { name: '鼠标4', icon: '/桌面程序贴图/电子设备/鼠标  (4).png', category: 'electronics' },
  { name: '鼠标5', icon: '/桌面程序贴图/电子设备/鼠标  (5).png', category: 'electronics' },
  { name: '鼠标6', icon: '/桌面程序贴图/电子设备/鼠标  (6).png', category: 'electronics' },
  
  // 电子设备 - 移动设备
  { name: '手机1', icon: '/桌面程序贴图/电子设备/手机 (1).png', category: 'electronics' },
  { name: '手机2', icon: '/桌面程序贴图/电子设备/手机 (2).png', category: 'electronics' },
  { name: '手机3', icon: '/桌面程序贴图/电子设备/手机 (3).png', category: 'electronics' },
  { name: '平板1', icon: '/桌面程序贴图/电子设备/平板 (1).png', category: 'electronics' },
  { name: '平板2', icon: '/桌面程序贴图/电子设备/平板 (2).png', category: 'electronics' },
  { name: '平板3', icon: '/桌面程序贴图/电子设备/平板 (3).png', category: 'electronics' },
  { name: '平板4', icon: '/桌面程序贴图/电子设备/平板 (4).png', category: 'electronics' },
  
  // 电子设备 - 音频设备
  { name: '耳机1', icon: '/桌面程序贴图/电子设备/耳机 (1).png', category: 'electronics' },
  { name: '耳机2', icon: '/桌面程序贴图/电子设备/耳机 (2).png', category: 'electronics' },
  { name: '耳机3', icon: '/桌面程序贴图/电子设备/耳机 (3).png', category: 'electronics' },
  { name: '耳机4', icon: '/桌面程序贴图/电子设备/耳机 (4).png', category: 'electronics' },
  { name: '耳机5', icon: '/桌面程序贴图/电子设备/耳机 (5).png', category: 'electronics' },
  { name: '耳机6', icon: '/桌面程序贴图/电子设备/耳机 (6).png', category: 'electronics' },
  
  // 学习资料 - 书籍资料
  { name: '书本1', icon: '/桌面程序贴图/学习用品/书本 (1).png', category: 'study' },
  { name: '书本2', icon: '/桌面程序贴图/学习用品/书本 (2).png', category: 'study' },
  { name: '书本3', icon: '/桌面程序贴图/学习用品/书本 (3).png', category: 'study' },
  
  // 学习资料 - 书写工具
  { name: '铅笔1', icon: '/桌面程序贴图/学习用品/铅笔 (1).png', category: 'study' },
  { name: '铅笔2', icon: '/桌面程序贴图/学习用品/铅笔 (2).png', category: 'study' },
  { name: '铅笔3', icon: '/桌面程序贴图/学习用品/铅笔 (3).png', category: 'study' },
  { name: '铅笔4', icon: '/桌面程序贴图/学习用品/铅笔 (4).png', category: 'study' },
  { name: '铅笔5', icon: '/桌面程序贴图/学习用品/铅笔 (5).png', category: 'study' },
  { name: '钢笔1', icon: '/桌面程序贴图/学习用品/钢笔 (1).png', category: 'study' },
  { name: '钢笔2', icon: '/桌面程序贴图/学习用品/钢笔 (2).png', category: 'study' },
  { name: '钢笔3', icon: '/桌面程序贴图/学习用品/钢笔 (3).png', category: 'study' },
  { name: '钢笔4', icon: '/桌面程序贴图/学习用品/钢笔 (4).png', category: 'study' },
  { name: '钢笔5', icon: '/桌面程序贴图/学习用品/钢笔 (5).png', category: 'study' },
  
  // 学习资料 - 笔记用品
  { name: '便利贴1', icon: '/桌面程序贴图/学习用品/便利贴(1).png', category: 'study' },
  { name: '便利贴2', icon: '/桌面程序贴图/学习用品/便利贴(2).png', category: 'study' },
  { name: '便利贴3', icon: '/桌面程序贴图/学习用品/便利贴(3).png', category: 'study' },
  { name: '便利贴4', icon: '/桌面程序贴图/学习用品/便利贴(4).png', category: 'study' },
  
  // 小工具 - 办公工具
  { name: '美工刀1', icon: '/桌面程序贴图/实用小物件/美工刀 (1).png', category: 'tools' },
  { name: '美工刀2', icon: '/桌面程序贴图/实用小物件/美工刀 (2).png', category: 'tools' },
  { name: '美工刀3', icon: '/桌面程序贴图/实用小物件/美工刀 (3).png', category: 'tools' },
  { name: '美工刀4', icon: '/桌面程序贴图/实用小物件/美工刀 (4).png', category: 'tools' },
  { name: '订书机1', icon: '/桌面程序贴图/实用小物件/订书机 (1).png', category: 'tools' },
  { name: '订书机2', icon: '/桌面程序贴图/实用小物件/订书机 (2).png', category: 'tools' },
  { name: '订书机3', icon: '/桌面程序贴图/实用小物件/订书机 (3).png', category: 'tools' },
  { name: '订书机4', icon: '/桌面程序贴图/实用小物件/订书机 (4).png', category: 'tools' },
  { name: '纸巾1', icon: '/桌面程序贴图/生活用品/纸巾 (1).png', category: 'tools' },
  { name: '纸巾2', icon: '/桌面程序贴图/生活用品/纸巾 (2).png', category: 'tools' },
  { name: '纸巾3', icon: '/桌面程序贴图/生活用品/纸巾 (3).png', category: 'tools' },
  { name: '纸巾4', icon: '/桌面程序贴图/生活用品/纸巾 (4).png', category: 'tools' },
  
  // 小工具 - 存储设备
  { name: 'U盘1', icon: '/桌面程序贴图/实用小物件/U盘 (1).png', category: 'tools' },
  { name: 'U盘2', icon: '/桌面程序贴图/实用小物件/U盘 (2).png', category: 'tools' },
  { name: 'U盘3', icon: '/桌面程序贴图/实用小物件/U盘 (3).png', category: 'tools' },
  { name: 'U盘4', icon: '/桌面程序贴图/实用小物件/U盘 (4).png', category: 'tools' },
  { name: 'U盘5', icon: '/桌面程序贴图/实用小物件/U盘 (5).png', category: 'tools' },

  // 小工具 - 时间工具
  { name: '计算器1', icon: '/桌面程序贴图/实用小物件/计算器 (1).png', category: 'tools' },
  { name: '计算器2', icon: '/桌面程序贴图/实用小物件/计算器 (2).png', category: 'tools' },
  { name: '计算器3', icon: '/桌面程序贴图/实用小物件/计算器 (3).png', category: 'tools' },
  { name: '计算器4', icon: '/桌面程序贴图/实用小物件/计算器 (4).png', category: 'tools' },
  { name: '计算器5', icon: '/桌面程序贴图/实用小物件/计算器 (5).png', category: 'tools' },
  { name: '闹钟1', icon: '/桌面程序贴图/实用小物件/闹钟 (1).png', category: 'tools' },
  { name: '闹钟2', icon: '/桌面程序贴图/实用小物件/闹钟 (2).png', category: 'tools' },
  { name: '闹钟3', icon: '/桌面程序贴图/实用小物件/闹钟 (3).png', category: 'tools' },
  { name: '闹钟4', icon: '/桌面程序贴图/实用小物件/闹钟 (4).png', category: 'tools' },
  { name: '闹钟5', icon: '/桌面程序贴图/实用小物件/闹钟 (5).png', category: 'tools' },
  { name: '闹钟6', icon: '/桌面程序贴图/实用小物件/闹钟 (6).png', category: 'tools' },
  { name: '闹钟7', icon: '/桌面程序贴图/实用小物件/闹钟 (7).png', category: 'tools' },
  
  // 生活用品 - 照明用品
  { name: '台灯1', icon: '/桌面程序贴图/生活用品/台灯 (1).png', category: 'daily' },
  { name: '台灯2', icon: '/桌面程序贴图/生活用品/台灯 (2).png', category: 'daily' },
  { name: '台灯3', icon: '/桌面程序贴图/生活用品/台灯 (3).png', category: 'daily' },
  { name: '台灯4', icon: '/桌面程序贴图/生活用品/台灯 (4).png', category: 'daily' },
  { name: '台灯5', icon: '/桌面程序贴图/生活用品/台灯（5）.png', category: 'daily' },
  
  // 生活用品 - 饮水用品
  { name: '水杯1', icon: '/桌面程序贴图/生活用品/水杯 (1).png', category: 'daily' },
  { name: '水杯2', icon: '/桌面程序贴图/生活用品/水杯 (2).png', category: 'daily' },
  { name: '水杯3', icon: '/桌面程序贴图/生活用品/水杯 (3).png', category: 'daily' },
  { name: '水杯4', icon: '/桌面程序贴图/生活用品/水杯 (4).png', category: 'daily' },
  
  // 生活用品 - 个人物品
  { name: '薯片1', icon: '/桌面程序贴图/生活用品/薯片 (1).png', category: 'daily' },
  { name: '薯片2', icon: '/桌面程序贴图/生活用品/薯片 (2).png', category: 'daily' },
  { name: '薯片3', icon: '/桌面程序贴图/生活用品/薯片 (3).png', category: 'daily' },
  { name: '蛋糕1', icon: '/桌面程序贴图/生活用品/蛋糕 (1).png', category: 'daily' },
  { name: '蛋糕2', icon: '/桌面程序贴图/生活用品/蛋糕 (2).png', category: 'daily' },
  { name: '蛋糕3', icon: '/桌面程序贴图/生活用品/蛋糕 (3).png', category: 'daily' },
  { name: '镜子1', icon: '/桌面程序贴图/生活用品/镜子 (1).png', category: 'daily' },
  { name: '镜子2', icon: '/桌面程序贴图/生活用品/镜子 (2).png', category: 'daily' },
  { name: '镜子3', icon: '/桌面程序贴图/生活用品/镜子 (3).png', category: 'daily' },
  { name: '镜子4', icon: '/桌面程序贴图/生活用品/镜子 (4).png', category: 'daily' },
  { name: '镜子5', icon: '/桌面程序贴图/生活用品/镜子 (5).png', category: 'daily' },
  { name: '镜子6', icon: '/桌面程序贴图/生活用品/镜子 (6).png', category: 'daily' },
  { name: '镜子7', icon: '/桌面程序贴图/生活用品/镜子 (7).png', category: 'daily' },
  { name: '口红1', icon: '/桌面程序贴图/生活用品/口红 (1).png', category: 'daily' },
  { name: '口红2', icon: '/桌面程序贴图/生活用品/口红 (2).png', category: 'daily' },
  { name: '口红3', icon: '/桌面程序贴图/生活用品/口红 (3).png', category: 'daily' },
  { name: '口红4', icon: '/桌面程序贴图/生活用品/口红 (4).png', category: 'daily' },
  { name: '口红5', icon: '/桌面程序贴图/生活用品/口红 (5).png', category: 'daily' },
  { name: '口红6', icon: '/桌面程序贴图/生活用品/口红 (6).png', category: 'daily' },
  { name: '口红7', icon: '/桌面程序贴图/生活用品/口红 (7).png', category: 'daily' },
  { name: '粉饼1', icon: '/桌面程序贴图/生活用品/粉饼 (1).png', category: 'daily' },
  { name: '粉饼2', icon: '/桌面程序贴图/生活用品/粉饼 (2).png', category: 'daily' },
  { name: '粉饼3', icon: '/桌面程序贴图/生活用品/粉饼 (3).png', category: 'daily' }
]

// 获取过滤后的元素列表
const getFilteredElements = () => {
  if (activeCategory.value === 'all') {
    return availableElements
  }
  return availableElements.filter(el => el.category === activeCategory.value)
}

// 元素面板相关函数
const onElementDragStart = (element: any, event: DragEvent) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('text/plain', JSON.stringify(element))
    event.dataTransfer.effectAllowed = 'copy'
  }
}

const onElementClick = (element: any) => {
  // 点击元素面板中的元素时，自动添加到桌面中间
  if (desktopCanvasRef.value) {
    const canvas = desktopCanvasRef.value.getCanvas()
    if (canvas) {
      const rect = canvas.getBoundingClientRect()
      const x = rect.width / 2 - 50
      const y = rect.height / 2 - 50
      
      const newElement: DesktopElement = {
        ...element,
        id: Date.now(),
        x: Math.max(0, Math.min(x, rect.width - 100)),
        y: Math.max(0, Math.min(y, rect.height - 100)),
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
    
    if (desktopCanvasRef.value) {
      const canvas = desktopCanvasRef.value.getCanvas()
      if (canvas) {
        const rect = canvas.getBoundingClientRect()
        const x = event.clientX - rect.left - 50
        const y = event.clientY - rect.top - 50
        
        // 创建新元素实例
        const newElement: DesktopElement = {
          ...elementData,
          id: Date.now(),
          x: Math.max(0, Math.min(x, rect.width - 100)),
          y: Math.max(0, Math.min(y, rect.height - 100)),
          rotation: 0,
          scale: 1,
          zIndex: elements.value.length + 1,
          size: elementData.size || 2,
          // 初始深度根据是否是柜子设定
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
}

// 元素拖拽
let isDragging = false

const onDrag = (event: MouseEvent) => {
  if (isDragging && draggingElement.value && desktopCanvasRef.value) {
    const canvas = desktopCanvasRef.value.getCanvas()
    if (canvas) {
      const rect = canvas.getBoundingClientRect()
      const x = event.clientX - dragOffset.value.x
      const y = event.clientY - dragOffset.value.y
      
      draggingElement.value.x = Math.max(0, Math.min(x, rect.width - 50))
      draggingElement.value.y = Math.max(0, Math.min(y, rect.height - 50))
      
      emit('update:elements', elements.value)
    }
  }
}

const startDrag = (element: DesktopElement, event: MouseEvent) => {
  event.preventDefault()
  isDragging = true
  draggingElement.value = element
  
  dragOffset.value.x = event.clientX - element.x
  dragOffset.value.y = event.clientY - element.y
  
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
  window.addEventListener('mouseleave', stopDrag)
}

const stopDrag = () => {
  isDragging = false
  draggingElement.value = null
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  window.removeEventListener('mouseleave', stopDrag)
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
      // 复制3D属�?
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
  if (confirm('确定要清空桌面吗？此操作不可撤销！')) {
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
      
      if (desktopCanvasRef.value) {
        const canvas = desktopCanvasRef.value.getCanvas()
        if (canvas) {
          const htmlCanvas = await html2canvas(canvas, {
            scale: 2, // 提高清晰�?
            useCORS: true,
            allowTaint: true,
            logging: false
          });
          
          // 创建下载链接
          const link = document.createElement('a');
          link.download = `桌面设计_${new Date().toLocaleDateString()}.png`;
          link.href = htmlCanvas.toDataURL('image/png');
          link.click();
        }
      }
    } catch (error) {
      console.error('下载图片失败:', error);
      alert('导出图片失败，请确保已安装html2canvas库！');
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
  
  // 加载保存的配�?
  const savedConfig = localStorage.getItem('desktop-config')
  if (savedConfig) {
    try {
      const config = JSON.parse(savedConfig)
      elements.value = config.elements || []
      // 为已保存的元素添�?D属�?
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

// 处理元素旋转更新
const updateElementRotation = (rotation: number) => {
  if (selectedElement.value) {
    selectedElement.value.rotation = rotation
    emit('update:elements', elements.value)
  }
}

// 处理元素尺寸更新
const updateElementSize = (size: number) => {
  if (selectedElement.value) {
    selectedElement.value.size = size
    emit('update:elements', elements.value)
  }
}

// 监听属性变�?
watch(() => props.initialElements, (newElements) => {
  elements.value = newElements
  // 为初始元素添�?D属�?
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
.desktop-builder {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 响应式设�?*/
@media (max-width: 1024px) {
  .desktop-builder {
    padding: 1rem;
  }
}

@media (max-width: 768px) {
  .desktop-builder {
    padding: 0.5rem;
  }
}
</style>
