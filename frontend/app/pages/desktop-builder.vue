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
import { watch } from 'vue'
import ElementPanel from '../components/ElementPanel.vue'
import DesktopCanvas from '../components/DesktopCanvas.vue'
import Toolbar from '../components/Toolbar.vue'
import ElementEditor from '../components/ElementEditor.vue'
import ContextMenu from '../components/ContextMenu.vue'
import type { DesktopElement, ElementCategory, ContextMenuState } from '../components/types'
import { elementCategories, availableElements } from '../config/desktop-elements'
import { useDesktopBuilder } from '../composables/useDesktopBuilder'

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
  background: '/桌面程序贴图/桌面/微信图片_20251117210350_46_979.jpg',
  initialElements: () => []
})

// 组件事件
const emit = defineEmits<Emits>()

// 使用组合式函数
const {
  desktopCanvasRef,
  elements,
  selectedElement,
  elementHovered,
  background,
  activeCategory,
  contextMenu,
  onElementDragStart,
  onElementClick,
  onDragOver,
  onDrop,
  startDrag,
  deselectElement,
  showContextMenu,
  editElement,
  deleteElement,
  duplicateElement,
  rotateElement,
  bringToFront,
  sendToBack,
  clearDesktop,
  saveDesktop: saveDesktopAction,
  downloadImage
} = useDesktopBuilder(props.initialElements, props.background)

// 监听状态变化并触发事件
watch(elements, (newElements) => {
  emit('update:elements', newElements)
}, { deep: true })

watch(selectedElement, (newElement) => {
  emit('elementSelected', newElement)
})

// 包装保存函数以触发事件
const saveDesktop = () => {
  const config = saveDesktopAction()
  emit('save', config)
}

// 更新元素属性的方法 (这些在 ElementEditor 中使用，但不在 composable 中)
const updateElementRotation = (rotation: number) => {
  if (selectedElement.value) {
    selectedElement.value.rotation = rotation
  }
}

const updateElementSize = (size: number) => {
  if (selectedElement.value) {
    selectedElement.value.size = size
  }
}
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
