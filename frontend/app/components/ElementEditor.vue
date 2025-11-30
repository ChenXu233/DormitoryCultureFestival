<template>
  <div v-if="element" class="bg-white rounded-lg shadow-sm p-4 mb-4">
    <h3 class="text-sm font-semibold text-gray-700 mb-2">编辑：{{ element.name }}</h3>
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div>
        <label class="block text-xs text-gray-500 mb-1">旋转</label>
        <input 
          type="range" 
          min="0" 
          max="360" 
          step="1" 
          :value="element.rotation" 
          @input="$emit('update:rotation', $event.target ? Number(($event.target as HTMLInputElement).value) : 0)"
          class="w-full"
        />
        <span class="text-xs text-gray-500">{{ element.rotation }}°</span>
      </div>
      <div>
        <label class="block text-xs text-gray-500 mb-1">大小</label>
        <input 
          type="range" 
          min="1" 
          max="6" 
          step="0.2" 
          :value="element.size || 2" 
          @input="$emit('update:size', $event.target ? Number(($event.target as HTMLInputElement).value) : 2)"
          class="w-full"
        />
        <span class="text-xs text-gray-500">{{ (element.size || 2) }}rem</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DesktopElement } from './types'

// 定义组件属性
interface Props {
  element: DesktopElement | null
}

// 定义组件事件
interface Emits {
  (e: 'update:rotation', rotation: number): void
  (e: 'update:scale', scale: number): void
  (e: 'update:size', size: number): void
}

// 组件属性
const props = defineProps<Props>()

// 组件事件
const emit = defineEmits<Emits>()
</script>

<style scoped>
/* 输入滑块样式 */
input[type="range"] {
  appearance: none;
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
</style>