<template>
  <div class="mb-6">
    <h4 class="text-sm font-medium text-gray-700 mb-3">{{ title }}</h4>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
      <button
        v-for="style in styles"
        :key="style.id"
        :class="[
          'relative p-4 rounded-lg border-2 transition-all duration-200 text-left',
          selectedStyle === style.id
            ? 'border-purple-500 bg-purple-50 shadow-md'
            : 'border-gray-200 bg-white hover:border-purple-300 hover:shadow-sm'
        ]"
        @click="selectStyle(style.id)"
      >
        <!-- 选中标识 -->
        <div
          v-if="selectedStyle === style.id"
          class="absolute top-2 right-2 w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center"
        >
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        </div>

        <!-- 风格图标 -->
        <div class="flex items-start gap-3">
          <div class="text-3xl flex-shrink-0">{{ style.icon }}</div>
          <div class="flex-1 min-w-0">
            <h5 class="font-medium text-gray-900 mb-1">{{ style.name }}</h5>
            <p class="text-xs text-gray-600 line-clamp-2">{{ style.description }}</p>
          </div>
        </div>

        <!-- 风格标签 -->
        <div class="mt-2 flex flex-wrap gap-1">
          <span v-if="style.aspectRatio" class="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded">
            {{ style.aspectRatio }}
          </span>
          <span v-if="style.style" class="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded">
            {{ style.style }}
          </span>
        </div>
      </button>
    </div>

    <!-- 选中风格的详细信息 -->
    <div v-if="selectedStylePreset" class="mt-4 p-4 bg-purple-50 border border-purple-200 rounded-lg">
      <div class="flex items-start gap-3">
        <div class="text-2xl">{{ selectedStylePreset.icon }}</div>
        <div class="flex-1">
          <h5 class="font-medium text-purple-900 mb-1">已选择：{{ selectedStylePreset.name }}</h5>
          <p class="text-sm text-purple-700 mb-2">{{ selectedStylePreset.description }}</p>
          
          <!-- 高级信息（可折叠） -->
          <details class="text-xs text-purple-600">
            <summary class="cursor-pointer hover:text-purple-800">查看提示词详情</summary>
            <div class="mt-2 p-2 bg-white rounded border border-purple-200">
              <p class="mb-2"><strong>正向提示词：</strong></p>
              <p class="text-gray-700 mb-3">{{ selectedStylePreset.prompt }}</p>
              <p class="mb-2"><strong>负向提示词：</strong></p>
              <p class="text-gray-700">{{ selectedStylePreset.negativePrompt }}</p>
            </div>
          </details>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AI_STYLE_PRESETS, getStylePresetById, type AIStylePreset } from '../config/ai-style-presets'

interface Props {
  modelValue: string
  title?: string
}

interface Emits {
  (e: 'update:modelValue', value: string): void
}

const props = withDefaults(defineProps<Props>(), {
  title: '选择生成风格'
})

const emit = defineEmits<Emits>()

const styles = AI_STYLE_PRESETS
const selectedStyle = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const selectedStylePreset = computed<AIStylePreset | undefined>(() => {
  return getStylePresetById(selectedStyle.value)
})

const selectStyle = (styleId: string) => {
  selectedStyle.value = styleId
}
</script>
