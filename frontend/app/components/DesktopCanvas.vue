<template>
  <div class="perspective-container">
    <div ref="containerRef" class="desktop-canvas-container" :style="containerStyle">
      <!-- 桌面画布 - 3D立体桌面 -->
      <div 
        ref="desktopCanvas"
        class="relative w-full h-full rounded-lg border-2 border-gray-300 overflow-hidden shadow-xl"
        :style="desktopStyle"
        @dragover="$emit('drag-over', $event)"
        @drop="$emit('drop', $event)"
        @click.self="$emit('deselect-element')"
      >
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
          @mousedown="$emit('element-drag-start', element, $event)"
          @contextmenu.prevent="$emit('context-menu-show', $event, element)"
          @mouseenter="$emit('element-hover', element.id)"
          @mouseleave="$emit('element-hover', null)"
        >
          <div 
            :class="[
              'rounded-lg transition-all duration-300',
              selectedElementId === element.id 
                ? 'border-blue-500 ring-2 ring-blue-200' 
                : 'border-transparent',
              hoveredElementId === element.id ? 'transform hover-scale' : ''
            ]"
            :style="getElement3DStyle(element)"
          >
            <div class="text-center">
              <div 
                class="transform transition-transform duration-300 flex items-center justify-center"
                :style="getElementContentStyle(element)"
              >
                <img v-if="isImageIcon(element.icon)" :src="element.icon" :alt="element.name" class="max-h-full max-w-full object-contain" />
                <div v-else :style="{ fontSize: `${element.size || 2}rem` }">{{ element.icon }}</div>
              </div>
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
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import type { DesktopElement } from './types'

// 定义组件属性
interface Props {
  elements: DesktopElement[]
  background: string
  height: number
  selectedElementId?: number | string | null
  hoveredElementId?: number | string | null
}

// 定义组件事件
interface Emits {
  (e: 'drag-over', event: DragEvent): void
  (e: 'drop', event: DragEvent): void
  (e: 'deselect-element'): void
  (e: 'element-drag-start', element: DesktopElement, event: MouseEvent): void
  (e: 'context-menu-show', event: MouseEvent, element: DesktopElement): void
  (e: 'element-hover', elementId: number | string | null): void
}

// 组件属性
const props = withDefaults(defineProps<Props>(), {
  height: 500,
  selectedElementId: null,
  hoveredElementId: null
})

// 组件事件
const emit = defineEmits<Emits>()

// 模板引用
const desktopCanvas = ref<HTMLElement>()
const containerRef = ref<HTMLElement | null>(null)

// 图片宽高比和容器高度管理
const aspectRatio = ref<number | null>(null)
const containerHeight = ref<number>(props.height || 500)

let resizeObserver: ResizeObserver | null = null

// 更新容器高度（基于图片宽高比或 props.height 作为回退）
const updateContainerSize = () => {
  const isImageBackground = props.background && (props.background.startsWith('/') || props.background.startsWith('http'))
  const containerEl = containerRef.value
  if (isImageBackground && aspectRatio.value && containerEl) {
    const width = containerEl.clientWidth || containerEl.getBoundingClientRect().width
    containerHeight.value = Math.max(1, Math.round(width / aspectRatio.value))
  } else {
    containerHeight.value = props.height || 500
  }
}

// 监听背景图片并加载以获取宽高比
const loadBackgroundImage = (src: string) => {
  aspectRatio.value = null
  if (!src) {
    updateContainerSize()
    return
  }

  const isImage = src.startsWith('/') || src.startsWith('http')
  if (!isImage) {
    updateContainerSize()
    return
  }

  const img = new Image()
  img.onload = () => {
    if (img.naturalHeight > 0) {
      aspectRatio.value = img.naturalWidth / img.naturalHeight
    }
    // update height after we have aspect
    nextTick(() => updateContainerSize())
  }
  img.onerror = () => {
    aspectRatio.value = null
    updateContainerSize()
  }
  img.src = src
}

// 组件挂载时设置 ResizeObserver
onMounted(() => {
  // start observing container width changes
  if (window && 'ResizeObserver' in window) {
    resizeObserver = new ResizeObserver(() => updateContainerSize())
    if (containerRef.value) resizeObserver.observe(containerRef.value)
  } else {
    // fallback: window resize
    window.addEventListener('resize', updateContainerSize)
  }
  // initial load
  loadBackgroundImage(props.background)
})

onUnmounted(() => {
  if (resizeObserver && containerRef.value) resizeObserver.unobserve(containerRef.value)
  resizeObserver = null
  if (window && !('ResizeObserver' in window)) {
    window.removeEventListener('resize', updateContainerSize)
  }
})

// 响应 background prop 变化
watch(() => props.background, (newBg) => {
  loadBackgroundImage(newBg)
})

// 计算传给模板的容器样式
const containerStyle = computed(() => ({ height: containerHeight.value + 'px' }))

// end container / image sizing

// 获取桌面的3D样式
const desktopStyle = computed(() => {
  const isImageBackground = props.background.startsWith('/') || props.background.startsWith('http')
  
  if (isImageBackground) {
    return {
      backgroundImage: `url(${props.background})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      boxShadow: '0 0 0 1px rgba(0,0,0,0.1)'
    }
  }
  
  return {
    background: props.background,
    boxShadow: '0 0 0 1px rgba(0,0,0,0.1)',
    backgroundImage: `linear-gradient(45deg, rgba(222, 184, 135, 0.1) 25%, transparent 25%), 
                      linear-gradient(-45deg, rgba(222, 184, 135, 0.1) 25%, transparent 25%), 
                      linear-gradient(45deg, transparent 75%, rgba(222, 184, 135, 0.1) 75%), 
                      linear-gradient(-45deg, transparent 75%, rgba(222, 184, 135, 0.1) 75%)`,
    backgroundSize: '20px 20px',
    backgroundPosition: '0 0, 0 10px, 10px -10px, -10px 0px'
  }
})

// 获取元素的3D变换
const getElementTransform = (element: DesktopElement) => {
  const rotation = element.rotation || 0
  const scale = element.scale || 1
  const rotationX = element.rotationX || 0
  const rotationY = element.rotationY || 0
  
  return `rotate(${rotation}deg) scale(${scale}) perspective(1000px) rotateX(${rotationX}deg) rotateY(${rotationY}deg)`
}

// 判断是否为图片图标
const isImageIcon = (icon: string) => {
  return icon.startsWith('/') || icon.startsWith('http')
}

// 获取元素内容样式
const getElementContentStyle = (element: DesktopElement) => {
  const size = element.size || 2
  const pixelSize = size * 50 // 将 rem 转换为像素大小
  return {
    width: `${pixelSize}px`,
    height: `${pixelSize}px`
  }
}

// 获取元素的3D样式
const getElement3DStyle = (element: DesktopElement) => {
  const isImage = isImageIcon(element.icon)
  const baseStyle: any = {
    backgroundColor: 'transparent',
    transformStyle: 'preserve-3d',
    transition: 'all 0.3s ease',
    padding: isImage ? '0' : '0.5rem'
  }
  
  if (element.isCabinet) {
    baseStyle.borderRadius = '8px'
    baseStyle.padding = '10px'
    baseStyle.border = '2px solid #bc8f8f'
    baseStyle.backgroundImage = `linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px), linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px)`
    baseStyle.backgroundSize = '10px 10px'
  } else if (element.category === 'electronics') {
    baseStyle.color = 'white'
    baseStyle.borderRadius = '6px'
  } else if (element.category === 'stationery') {
    baseStyle.borderRadius = '2px'
    baseStyle.borderLeft = '8px solid #3182ce'
  }
  
  return baseStyle
}

// 暴露方法给父组件
defineExpose({
  getCanvas: () => desktopCanvas.value
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

/* 悬停缩放效果 */
.hover-scale {
  transform: translateY(-5px) !important;
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

/* 响应式设计 */
@media (max-width: 1024px) {
  .perspective-container {
    perspective: 1000px;
  }
}

@media (max-width: 768px) {
  .perspective-container {
    perspective: 800px;
    margin: 10px 0;
  }
}
</style>