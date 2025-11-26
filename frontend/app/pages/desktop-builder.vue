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
        <ElementPanel
          :categories="elementCategories"
          :elements="availableElements"
          :active-category="activeCategory"
          @category-change="activeCategory = $event"
          @element-drag-start="onElementDragStart"
          @element-click="onElementClick"
        />
      </div>

      <!-- 中间：桌面构建区域 -->
      <div class="lg:col-span-3">
        <!-- 桌面工具栏 -->
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
          :height="500"
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
  background: '#f8fafc',
  initialElements: () => []
})

// 组件事件
const emit = defineEmits<Emits>()

// 响应式数据
const desktopCanvasRef = ref<InstanceType<typeof DesktopCanvas>>()
const selectedElement = ref<DesktopElement | null>(null)
const elementHovered = ref<string | null>(null)
const draggingElement = ref<DesktopElement | null>(null)
const dragOffset = ref({ x: 0, y: 0 })
const background = ref(props.background)
const activeCategory = ref('all')
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
  { id: 'all', name: '全部' },
  { id: 'electronics', name: '电子设备' },
  { id: 'study', name: '学习资料' },
  { id: 'tools', name: '小工具' },
  { id: 'daily', name: '生活用品' }
]

// 预定义的可拖拽元素
const availableElements = [
  // 电子设备 - 电脑套装
  { name: '电脑', icon: '💻', category: 'electronics' },
  { name: '键盘', icon: '⌨️', category: 'electronics' },
  { name: '鼠标', icon: '🖱️', category: 'electronics' },
  
  // 电子设备 - 移动设备
  { name: '手机', icon: '📱', category: 'electronics' },
  { name: '平板', icon: '📟', category: 'electronics' },
  
  // 电子设备 - 音频设备
  { name: '耳机', icon: '🎧', category: 'electronics' },
  
  // 学习资料 - 书籍资料
  { name: '书籍', icon: '📚', category: 'study' },
  
  // 学习资料 - 书写工具
  { name: '草稿纸', icon: '📝', category: 'study' },
  { name: '笔', icon: '✏️', category: 'study' },
  
  // 学习资料 - 笔记用品
  { name: '便利贴', icon: '📋', category: 'study' },
  
  // 小工具 - 办公工具
  { name: '美工刀', icon: '🔪', category: 'tools' },
  { name: '订书机', icon: '🖇️', category: 'tools' },
  { name: '纸巾', icon: '🧻', category: 'tools' },
  
  // 小工具 - 存储设备
  { name: 'U盘', icon: '💾', category: 'tools' },
  
  // 小工具 - 时间工具
  { name: '计算器', icon: '🧮', category: 'tools' },
  { name: '时钟', icon: '⏰', category: 'tools' },
  
  // 生活用品 - 照明用品
  { name: '台灯', icon: '💡', category: 'daily' },
  
  // 生活用品 - 饮水用品
  { name: '水杯', icon: '🥤', category: 'daily' },
  
  // 生活用品 - 个人物品
  { name: '小零食', icon: '🍪', category: 'daily' },
  { name: '手办', icon: '🎎', category: 'daily' },
  { name: '镜子', icon: '🪞', category: 'daily' },
  { name: '化妆品', icon: '💄', category: 'daily' }
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
  if (desktopCanvasRef.value) {
    const canvas = desktopCanvasRef.value.getCanvas()
    if (canvas) {
      const rect = canvas.getBoundingClientRect()
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
  isDragging = true
  draggingElement.value = element
  
  dragOffset.value.x = event.clientX - element.x
  dragOffset.value.y = event.clientY - element.y
  
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}

const stopDrag = () => {
  isDragging = false
  draggingElement.value = null
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
      
      if (desktopCanvasRef.value) {
        const canvas = desktopCanvasRef.value.getCanvas()
        if (canvas) {
          const htmlCanvas = await html2canvas(canvas, {
            scale: 2, // 提高清晰度
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
.desktop-builder {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 响应式设计 */
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