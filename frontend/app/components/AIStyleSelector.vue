<template>
  <div :class="compact ? 'inline-block' : 'mb-6'">
    <!-- 触发按钮 (Compact Mode) -->
    <button 
      v-if="compact"
      @click="showSelectorModal = true"
      class="p-2 bg-white/90 hover:bg-white text-purple-600 rounded-full transition-all duration-200 shadow-lg flex items-center justify-center border border-purple-100 hover:border-purple-300"
      :title="selectedStylePreset?.name || '选择风格'"
    >
      <span class="text-xl leading-none">{{ selectedStylePreset?.icon || '🎨' }}</span>
    </button>

    <!-- 触发按钮 (Normal Mode) -->
    <button 
      v-else
      @click="showSelectorModal = true"
      class="w-full py-3 px-4 bg-white border-2 border-purple-200 hover:border-purple-400 hover:bg-purple-50 rounded-xl transition-all duration-200 flex items-center justify-between group shadow-sm"
    >
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center text-xl group-hover:scale-110 transition-transform">
          {{ selectedStylePreset?.icon || '🎨' }}
        </div>
        <div class="text-left">
          <div class="font-bold text-gray-800 group-hover:text-purple-700 transition-colors">
            {{ selectedStylePreset?.name || '选择 AI 生成风格' }}
          </div>
          <div class="text-xs text-gray-500">
            {{ selectedStylePreset ? '点击更换风格' : '点击选择风格以开始生成' }}
          </div>
        </div>
      </div>
      <svg class="w-5 h-5 text-gray-400 group-hover:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>

    <!-- 风格选择弹窗 -->
    <div v-if="showSelectorModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" @click.self="showSelectorModal = false">
      <div class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full h-[85vh] flex flex-col overflow-hidden animate-fade-in-up">
        <!-- 弹窗头部 -->
        <div class="p-5 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <div>
            <h3 class="text-xl font-bold text-gray-800">选择生成风格</h3>
            <p class="text-sm text-gray-500">选择一个最适合你们团队的艺术风格</p>
          </div>
          <button @click="showSelectorModal = false" class="text-gray-400 hover:text-gray-600 transition-colors p-2 rounded-full hover:bg-gray-200">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- 弹窗内容区 -->
        <div class="flex-1 overflow-hidden flex flex-col md:flex-row">
          <!-- 左侧：风格列表 -->
          <div class="flex-1 overflow-y-auto custom-scrollbar p-6 bg-gray-50/50">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <button
                v-for="style in styles"
                :key="style.id"
                :class="[
                  'relative p-4 rounded-xl border-2 transition-all duration-200 text-left hover:shadow-md',
                  selectedStyle === style.id
                    ? 'border-purple-500 bg-white ring-2 ring-purple-200 ring-offset-2'
                    : 'border-gray-200 bg-white hover:border-purple-300'
                ]"
                @click="selectStyle(style.id)"
              >
                <div class="flex items-start gap-3">
                  <div class="text-3xl flex-shrink-0">{{ style.icon }}</div>
                  <div class="flex-1 min-w-0">
                    <h5 class="font-bold text-gray-900 mb-1">{{ style.name }}</h5>
                    <p class="text-xs text-gray-500 line-clamp-2">{{ style.description }}</p>
                  </div>
                </div>
                <!-- 选中标记 -->
                <div v-if="selectedStyle === style.id" class="absolute top-3 right-3 text-purple-500">
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>
              </button>
            </div>
          </div>

          <!-- 右侧：详情预览 -->
          <div class="w-full md:w-80 bg-white border-l border-gray-100 flex flex-col overflow-y-auto custom-scrollbar">
            <div v-if="selectedStylePreset" class="p-6">
              <div class="text-center mb-6">
                <div class="w-20 h-20 mx-auto bg-purple-50 rounded-full flex items-center justify-center text-5xl mb-4 shadow-inner">
                  {{ selectedStylePreset.icon }}
                </div>
                <h4 class="text-xl font-bold text-gray-900">{{ selectedStylePreset.name }}</h4>
                <div class="flex flex-wrap gap-2 justify-center mt-3">
                  <span v-if="selectedStylePreset.aspectRatio" class="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded-full font-medium">
                    {{ selectedStylePreset.aspectRatio }}
                  </span>
                  <span v-if="selectedStylePreset.style" class="text-xs px-2 py-1 bg-purple-100 text-purple-600 rounded-full font-medium">
                    {{ selectedStylePreset.style }}
                  </span>
                </div>
              </div>

              <div class="space-y-6">
                <div>
                  <h5 class="text-sm font-bold text-gray-900 mb-2">风格描述</h5>
                  <p class="text-sm text-gray-600 leading-relaxed bg-gray-50 p-3 rounded-lg">
                    {{ selectedStylePreset.description }}
                  </p>
                </div>

                <div>
                  <h5 class="text-sm font-bold text-green-600 mb-2 flex items-center gap-1">
                    <span>✨</span> 正向提示词
                  </h5>
                  <div class="bg-green-50 p-3 rounded-lg border border-green-100 text-xs text-gray-700 font-mono leading-relaxed break-words max-h-32 overflow-y-auto custom-scrollbar">
                    {{ selectedStylePreset.prompt }}
                  </div>
                </div>

                <div>
                  <h5 class="text-sm font-bold text-red-500 mb-2 flex items-center gap-1">
                    <span>🚫</span> 负向提示词
                  </h5>
                  <div class="bg-red-50 p-3 rounded-lg border border-red-100 text-xs text-gray-700 font-mono leading-relaxed break-words max-h-32 overflow-y-auto custom-scrollbar">
                    {{ selectedStylePreset.negativePrompt }}
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="flex-1 flex items-center justify-center text-gray-400 p-6 text-center">
              <div>
                <svg class="w-12 h-12 mx-auto mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                </svg>
                <p>请在左侧选择一个风格以查看详情</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部确认栏 -->
        <div class="p-4 bg-white border-t border-gray-100 flex justify-end gap-3">
          <button 
            @click="showSelectorModal = false"
            class="px-6 py-2.5 border border-gray-300 text-gray-700 font-medium rounded-xl hover:bg-gray-50 transition-colors"
          >
            取消
          </button>
          <button 
            @click="confirmSelection"
            :disabled="!selectedStyle"
            class="px-6 py-2.5 bg-purple-600 text-white font-bold rounded-xl hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-purple-200"
          >
            确认选择
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { AI_STYLE_PRESETS, getStylePresetById, type AIStylePreset } from '../config/ai-style-presets'

interface Props {
  modelValue: string
  title?: string
  compact?: boolean
}

interface Emits {
  (e: 'update:modelValue', value: string): void
}

const props = withDefaults(defineProps<Props>(), {
  title: '选择生成风格',
  compact: false
})

const emit = defineEmits<Emits>()

const showSelectorModal = ref(false)

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

const confirmSelection = () => {
  showSelectorModal.value = false
}
</script>
