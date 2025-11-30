<template>
  <div class="min-h-full bg-gradient-to-br from-orange-50 to-red-100 py-8">
    <div class="max-w-6xl mx-auto px-4">
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">
          四人团队特质匹配
        </h1>
        <p class="text-lg text-gray-600">
          输入四个4位唯一代码，查看团队特质匹配度和评语
        </p>
      </div>

      <!-- 匹配界面 -->
      <TeamCodeInput 
        v-model="codes"
        @submit="matchTeamTraits"
      />

      <!-- 匹配结果 -->
      <TeamMatchResult
        v-if="matchResult"
        :match-result="matchResult"
        @reset="resetMatch"
      >
        <template #image-upload>
          <ImageUploader
            v-model="uploadedImage"
            title="团队合影时刻"
            upload-button-text="上传团队合影"
            help-text="点击上传图片，记录团队合影时刻"
            :enable-a-i="true"
            @ai-generated="handleAIGenerated"
          />
        </template>
        
        <template #actions>
          <NuxtLink 
            to="/match"
            class="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors duration-200 text-center"
          >
            双人匹配
          </NuxtLink>
          <NuxtLink 
            to="/quiz"
            class="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors duration-200 text-center"
          >
            特质测试
          </NuxtLink>
        </template>
      </TeamMatchResult>

      <!-- 加载状态 -->
      <LoadingSpinner
        v-if="loading"
        message="正在分析团队特质匹配度..."
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import CONFIG from '../config/config'
const API_BASE_URL = CONFIG.apiBaseUrl

// 设置页面元信息
useSeoMeta({
  title: '四人团队特质匹配 - 宿舍文化节',
  description: '输入四个4位唯一代码，查看团队特质匹配度和评语'
})

// 页面配置
definePageMeta({
  layout: 'default'
})

// 匹配状态
const codes = ref(['', '', '', ''])
const loading = ref(false)
const matchResult = ref<any>(null)
const uploadedImage = ref<string | null>(null)
const aiGeneratedImage = ref<string | null>(null)

// 团队匹配函数
const matchTeamTraits = async () => {
  loading.value = true
  try {
    const response = await $fetch(`${API_BASE_URL}/api/quiz/team-match`, {
      method: 'POST',
      body: {
        codes: codes.value
      }
    })
    
    matchResult.value = response
  } catch (error) {
    console.error('团队匹配失败:', error)
    alert('团队匹配失败，请检查代码是否正确')
  } finally {
    loading.value = false
  }
}

// 处理 AI 生成的图片
const handleAIGenerated = (imageUrl: string) => {
  aiGeneratedImage.value = imageUrl
  console.log('AI 生成的图片:', imageUrl)
}

// 重置匹配
const resetMatch = () => {
  codes.value = ['', '', '', '']
  matchResult.value = null
  uploadedImage.value = null
  aiGeneratedImage.value = null
}
</script>
