<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 py-8">
    <div class="max-w-4xl mx-auto px-4">
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">
          双人特质匹配
        </h1>
        <p class="text-lg text-gray-600">
          输入两个4位唯一代码，查看双人特质匹配度
        </p>
      </div>

      <!-- 匹配界面 -->
      <div class="bg-white rounded-xl shadow-lg p-8">
        <div class="text-center">
          <div class="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-10 h-10 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
            </svg>
          </div>
          
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">
            输入特质代码
          </h2>
          <p class="text-gray-600 mb-6">
            请输入两个4位唯一代码，系统将分析你们的特质匹配度
          </p>

          <!-- 代码输入表单 -->
          <div class="max-w-md mx-auto">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2 text-left">
                  第一个代码
                </label>
                <input 
                  v-model="code1"
                  type="text" 
                  placeholder="请输入4位代码"
                  maxlength="4"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-center text-xl font-mono"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2 text-left">
                  第二个代码
                </label>
                <input 
                  v-model="code2"
                  type="text" 
                  placeholder="请输入4位代码"
                  maxlength="4"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-center text-xl font-mono"
                >
              </div>
            </div>
            
            <button 
              :disabled="!canMatch"
              :class="[
                'w-full mt-6 font-medium py-3 px-6 rounded-lg transition-colors duration-200',
                canMatch 
                  ? 'bg-purple-600 hover:bg-purple-700 text-white' 
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              ]"
              @click="matchTraits"
            >
              开始匹配
            </button>
          </div>
        </div>
      </div>

      <!-- 匹配结果 -->
      <div v-if="matchResult" class="bg-white rounded-xl shadow-lg p-8 mt-8">
        <div class="text-center">
          <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">
            匹配结果
          </h2>
          
          <!-- 匹配度展示 -->
          <div class="max-w-md mx-auto mb-6">
            <div class="bg-gradient-to-r from-green-400 to-blue-500 rounded-lg p-8 text-white">
              <div class="text-5xl font-bold mb-2">{{ matchResult.compatibility_score }}%</div>
              <div class="text-lg">特质匹配度</div>
            </div>
            
            <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div class="text-blue-800 font-medium text-center">
                {{ matchResult.match_analysis }}
              </div>
            </div>
          </div>
          
          <!-- 特质对比 -->
          <div class="mt-8">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">特质对比</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- 第一个人的特质 -->
              <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <h4 class="font-medium text-gray-800 mb-3">{{ matchResult.participant1_name || '用户1' }}</h4>
                <div class="space-y-2">
                  <div 
                    v-for="(trait, dimension) in matchResult.traits1" 
                    :key="dimension"
                    class="flex justify-between items-center"
                  >
                    <span class="text-sm text-gray-600">{{ dimension }}</span>
                    <span class="font-medium text-green-600">{{ trait }}</span>
                  </div>
                </div>
              </div>
              
              <!-- 第二个人的特质 -->
              <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <h4 class="font-medium text-gray-800 mb-3">{{ matchResult.participant2_name || '用户2' }}</h4>
                <div class="space-y-2">
                  <div 
                    v-for="(trait, dimension) in matchResult.traits2" 
                    :key="dimension"
                    class="flex justify-between items-center"
                  >
                    <span class="text-sm text-gray-600">{{ dimension }}</span>
                    <span class="font-medium text-green-600">{{ trait }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 操作按钮 -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center mt-8">
            <button 
              class="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors duration-200"
              @click="resetMatch"
            >
              重新匹配
            </button>
            <NuxtLink 
              to="/quiz"
              class="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors duration-200 text-center"
            >
              特质测试
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="bg-white rounded-xl shadow-lg p-8 mt-8">
        <div class="text-center">
          <div class="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-10 h-10 text-purple-600 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </div>
          <h2 class="text-xl font-semibold text-gray-800">正在分析特质匹配度...</h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import CONFIG from '../config/config'
const API_BASE_URL = CONFIG.apiBaseUrl

// 设置页面元信息
useSeoMeta({
  title: '双人特质匹配 - 宿舍文化节',
  description: '输入两个4位唯一代码，查看双人特质匹配度'
})

// 页面配置
definePageMeta({
  layout: false
})

// 匹配状态
const code1 = ref('')
const code2 = ref('')
const loading = ref(false)
const matchResult = ref<any>(null)

// 计算是否可以匹配
const canMatch = computed(() => {
  return code1.value.length === 4 && code2.value.length === 4
})

// 特质匹配
const matchTraits = async () => {
  if (!canMatch.value) return
  
  try {
    loading.value = true
    
    const response = await $fetch(`${API_BASE_URL}/api/quiz/match`, {
      method: 'POST',
      body: {
        code1: code1.value,
        code2: code2.value
      }
    })
    
    matchResult.value = response
  } catch (error) {
    console.error('匹配失败:', error)
    alert('匹配失败，请检查代码是否正确')
  } finally {
    loading.value = false
  }
}

// 重置匹配
const resetMatch = () => {
  code1.value = ''
  code2.value = ''
  matchResult.value = null
}
</script>

<style scoped>
/* 自定义样式 */
</style>