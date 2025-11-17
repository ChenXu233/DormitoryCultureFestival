<template>
  <div class="perspective-container">
    <div class="desktop-canvas-container" :style="{ height: height + 'px' }">
      <!-- 桌面画布 - 3D立体桌面 -->
      <div 
        ref="desktopCanvas"
        class="relative w-full h-full rounded-lg border-2 border-gray-300 overflow-hidden shadow-xl"
        :style="desktopStyle"
        @dragover="$emit('drag-over', $event)"
        @drop="$emit('drop', $event)"
        @click.self="$emit('deselect-element')"
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
          @mousedown="$emit('element-drag-start', element, $event)"
          @contextmenu.prevent="$emit('context-menu-show', $event, element)"
          @mouseenter="$emit('element-hover', element.id)"
          @mouseleave="$emit('element-hover', null)"
        >
          <div 
            :class="[
              'p-2 rounded-lg transition-all duration-300',
              selectedElementId === element.id 
                ? 'border-blue-500 ring-2 ring-blue-200 shadow-xl' 
                : 'border-transparent shadow-lg',
              hoveredElementId === element.id ? 'transform hover-scale' : ''
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
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
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

// 获取桌面的3D样式
const desktopStyle = computed(() => ({
  background: props.background,
  transform: 'perspective(1000px) rotateX(3deg) translateY(-20px)',
  boxShadow: '0 30px 40px rgba(0,0,0,0.2), 0 0 0 1px rgba(0,0,0,0.1)',
  backgroundImage: `linear-gradient(45deg, rgba(222, 184, 135, 0.1) 25%, transparent 25%), 
                    linear-gradient(-45deg, rgba(222, 184, 135, 0.1) 25%, transparent 25%), 
                    linear-gradient(45deg, transparent 75%, rgba(222, 184, 135, 0.1) 75%), 
                    linear-gradient(-45deg, transparent 75%, rgba(222, 184, 135, 0.1) 75%)`,
  backgroundSize: '20px 20px',
  backgroundPosition: '0 0, 0 10px, 10px -10px, -10px 0px'
}))

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
  const baseStyle: any = {
    backgroundColor: 'white',
    boxShadow: '0 5px 15px rgba(0,0,0,0.15), 0 0 0 1px rgba(0,0,0,0.05)',
    transformStyle: 'preserve-3d',
    transition: 'all 0.3s ease'
  }
  
  if (element.isCabinet) {
    baseStyle.backgroundColor = '#deb887'
    baseStyle.borderRadius = '8px'
    baseStyle.boxShadow = '0 10px 20px rgba(0,0,0,0.2), 0 0 0 1px rgba(0,0,0,0.1)'
    baseStyle.padding = '10px'
    baseStyle.border = '2px solid #bc8f8f'
    baseStyle.backgroundImage = `linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px), linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px)`
    baseStyle.backgroundSize = '10px 10px'
  } else if (element.category === 'electronics') {
    baseStyle.backgroundColor = '#2d3748'
    baseStyle.color = 'white'
    baseStyle.borderRadius = '6px'
    baseStyle.boxShadow = '0 8px 16px rgba(0,0,0,0.25)'
  } else if (element.category === 'stationery') {
    baseStyle.backgroundColor = '#f8f9fa'
    baseStyle.borderRadius = '2px'
    baseStyle.boxShadow = '0 3px 10px rgba(0,0,0,0.2)'
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