<template>
  <div class="w-87 mx-auto">
    <div class="relative rounded-lg overflow-hidden border-2 border-dashed border-gray-300 bg-gray-100">
      <!-- 上传区域 -->
      <div v-if="!modelValue && !aiGeneratedImage" class="aspect-[4/3] flex flex-col items-center justify-center px-4">
        <input
          ref="fileInputRef"
          type="file"
          accept="image/*"
          @change="handleFileUpload"
          class="hidden"
        />
        <button
          @click="triggerFileUpload"
          :disabled="isUploading"
          class="flex flex-col items-center justify-center px-6 py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors duration-200 disabled:opacity-50"
        >
          <svg v-if="!isUploading" class="w-8 h-8 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          <svg v-else class="w-8 h-8 mb-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          <span class="text-lg font-medium">{{ isUploading ? '上传中...' : uploadButtonText }}</span>
        </button>
        <p class="text-sm text-gray-500 mt-2">{{ helpText }}</p>
        <p class="text-xs text-gray-400 mt-1">支持 JPG、PNG 等图片格式</p>
      </div>

      <!-- 原始图片预览 -->
      <div v-else-if="modelValue && !aiGeneratedImage" class="aspect-[4/3] relative">
        <img 
          :src="modelValue"
          class="w-full h-full object-cover"
          :alt="'已上传的图片'"
        />
        
        <!-- 加载遮罩 -->
        <div v-if="isGenerating" class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div class="text-center text-white">
            <svg class="w-8 h-8 animate-spin mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <p class="text-sm">AI 正在生成优化版本...</p>
          </div>
        </div>

        <div class="absolute top-2 right-2 flex gap-2">
          <AIStyleSelector 
            v-if="enableAI && !isGenerating"
            v-model="selectedStyle" 
            compact 
          />
          <button
            v-if="enableAI && !isGenerating"
            @click="handleAIGenerate"
            class="p-2 bg-purple-600 hover:bg-purple-700 text-white rounded-full transition-colors duration-200 shadow-lg"
            title="使用 AI 生成选中风格的图片"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
          </button>
          <button
            @click="removeImage"
            :disabled="isGenerating"
            class="p-2 bg-red-600 hover:bg-red-700 text-white rounded-full transition-colors duration-200 disabled:opacity-50 shadow-lg"
            title="删除图片"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- AI 生成的图片预览 -->
      <div v-if="aiGeneratedImage" class="aspect-[4/3] relative">
        <img 
          :src="aiGeneratedImage"
          class="w-full h-full object-cover"
          alt="AI 生成的团队合影"
        />
        <div class="absolute top-2 left-2 flex gap-2">
          <div class="px-2 py-1 bg-purple-600 text-white text-xs rounded flex items-center gap-1">
            <span>{{ currentStyleName }}</span>
          </div>
          <div class="px-2 py-1 bg-green-600 text-white text-xs rounded">
            AI 优化版
          </div>
        </div>
        <button
          @click="removeAIImage"
          class="absolute top-2 right-2 p-2 bg-red-600 hover:bg-red-700 text-white rounded-full transition-colors duration-200 shadow-lg"
          title="删除 AI 图片，返回原图"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getStylePresetById, getDefaultStylePreset } from '../config/ai-style-presets'

interface Props {
  modelValue: string | null
  uploadButtonText?: string
  helpText?: string
  enableAI?: boolean
  aiPrompt?: string
}

interface Emits {
  (e: 'update:modelValue', value: string | null): void
  (e: 'ai-generated', value: string): void
}

const props = withDefaults(defineProps<Props>(), {
  title: '图片上传',
  uploadButtonText: '上传图片',
  helpText: '点击上传图片',
  enableAI: false,
  aiPrompt: '将这张团队合影转换为温馨的插画风格，保持人物特征，添加温暖的色调和宿舍文化节的氛围'
})

const emit = defineEmits<Emits>()

const fileInputRef = ref<HTMLInputElement>()
const originalFile = ref<File | null>(null)
const uploadedImageUrl = ref<string | null>(null)
const aiGeneratedImage = ref<string | null>(null)
const selectedStyle = ref(getDefaultStylePreset().id)

const { uploading: isUploading, uploadImage } = useImageUpload()
const { generating: isGenerating, generateImage } = useAIImageGeneration()

// 当前选中风格的名称
const currentStyleName = computed(() => {
  const style = getStylePresetById(selectedStyle.value)
  return style ? `${style.icon} ${style.name}` : '未知风格'
})

// 触发文件上传
const triggerFileUpload = () => {
  fileInputRef.value?.click()
}

// 处理文件上传
const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file || !file.type.startsWith('image/')) {
    alert('请选择有效的图片文件')
    return
  }

  try {
    originalFile.value = file
    
    // 首先显示本地预览
    const reader = new FileReader()
    reader.onload = (e) => {
      emit('update:modelValue', e.target?.result as string)
    }
    reader.readAsDataURL(file)

    // 如果启用了 AI 功能，上传到图床
    if (props.enableAI) {
      try {
        const imageUrl = await uploadImage(file)
        uploadedImageUrl.value = imageUrl
      } catch (error) {
        console.error('图片上传失败:', error)
        // 上传失败不影响本地预览
      }
    }
  } catch (error) {
    console.error('文件处理失败:', error)
    alert('图片处理失败，请重试')
  }
}

// AI 生成图片
const handleAIGenerate = async () => {
  if (!uploadedImageUrl.value) {
    // 如果还没有上传到图床，先上传
    if (!originalFile.value) {
      alert('请先上传图片')
      return
    }

    try {
      const imageUrl = await uploadImage(originalFile.value)
      uploadedImageUrl.value = imageUrl
    } catch (error) {
      alert('图片上传失败，无法进行 AI 优化')
      return
    }
  }

  // 获取选中的风格预设
  const stylePreset = getStylePresetById(selectedStyle.value)
  if (!stylePreset) {
    alert('请选择一个生成风格')
    return
  }

  try {
    const generatedUrl = await generateImage({
      prompt: stylePreset.prompt,
      imageUrl: uploadedImageUrl.value,
      size: '2K',
      watermark: false
    })
    
    aiGeneratedImage.value = generatedUrl
    emit('ai-generated', generatedUrl)
  } catch (error) {
    console.error('AI 生成失败:', error)
    alert(error instanceof Error ? error.message : 'AI 图片生成失败，请重试')
  }
}

// 删除图片
const removeImage = () => {
  emit('update:modelValue', null)
  originalFile.value = null
  uploadedImageUrl.value = null
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}

// 删除 AI 生成的图片
const removeAIImage = () => {
  aiGeneratedImage.value = null
  // 保留原始图片
}
</script>