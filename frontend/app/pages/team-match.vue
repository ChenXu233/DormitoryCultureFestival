<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-red-100 py-8">
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
      <div class="bg-white rounded-xl shadow-lg p-8">
        <div class="text-center">
          <div class="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-10 h-10 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
          </div>
          
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">
            输入团队特质代码
          </h2>
          <p class="text-gray-600 mb-6">
            请输入四个4位唯一代码，系统将分析团队特质匹配度并生成专属评语
          </p>

          <!-- 代码输入表单 -->
          <div class="max-w-2xl mx-auto">
            <div class="grid grid-cols-2 gap-4">
              <div v-for="i in 4" :key="i">
                <label class="block text-sm font-medium text-gray-700 mb-2 text-left">
                  成员{{ i }}代码
                </label>
                <input 
                  v-model="codes[i-1]"
                  type="text" 
                  :placeholder="`请输入成员${i}的4位代码`"
                  maxlength="4"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-center text-xl font-mono"
                >
              </div>
            </div>
            
            <button 
              :disabled="!canMatch"
              :class="[
                'w-full mt-6 font-medium py-3 px-6 rounded-lg transition-colors duration-200',
                canMatch 
                  ? 'bg-orange-600 hover:bg-orange-700 text-white' 
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              ]"
              @click="matchTeamTraits"
            >
              开始团队匹配
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
            团队匹配结果
          </h2>
          
          <!-- 匹配度展示 -->
          <div class="max-w-md mx-auto mb-6">
            <div class="bg-gradient-to-r from-green-400 to-blue-500 rounded-lg p-8 text-white">
              <div class="text-5xl font-bold mb-2">{{ matchResult.team_compatibility_score }}%</div>
              <div class="text-lg">团队特质匹配度</div>
            </div>
            
            <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div class="text-blue-800 font-medium text-center">
                <div class="text-lg font-bold mb-2">{{ matchResult.team_commentary?.title || '团队特质分析' }}</div>
                <div class="text-sm">{{ matchResult.team_commentary?.commentary || matchResult.team_commentary }}</div>
              </div>
            </div>
          </div>
          
          <!-- 特质分析 -->
          <div class="mt-8">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">团队特质分析</h3>
            <div class="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-6">
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div
v-for="(traitInfo, dimension) in matchResult.team_trait_analysis?.dominant_traits" :key="dimension"
                     class="text-center">
                  <div class="text-sm text-gray-600 mb-1">{{ dimension }}</div>
                  <div class="font-medium text-green-600">{{ traitInfo.trait }}</div>
                  <div class="text-xs text-gray-500">{{ traitInfo.count }}/4人</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 成员特质展示 -->
          <div class="mt-8">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">成员特质详情</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div
v-for="member in matchResult.participants" :key="member.code" 
                   class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <h4 class="font-medium text-gray-800 mb-3">{{ member.name || `成员${member.code}` }}</h4>
                <div class="space-y-2">
                  <div 
                    v-for="(trait, dimension) in member.primary_traits" 
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
              class="px-6 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg transition-colors duration-200"
              @click="resetMatch"
            >
              重新匹配
            </button>
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
            <NuxtLink 
              to="/"
              class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200 text-center"
            >
              返回首页
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="bg-white rounded-xl shadow-lg p-8 mt-8">
        <div class="text-center">
          <div class="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-10 h-10 text-orange-600 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </div>
          <h2 class="text-xl font-semibold text-gray-800">正在分析团队特质匹配度...</h2>
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
  title: '四人团队特质匹配 - 宿舍文化节',
  description: '输入四个4位唯一代码，查看团队特质匹配度和评语'
})

// 页面配置
definePageMeta({
  layout: false
})

// 匹配状态
const codes = ref(['', '', '', ''])
const loading = ref(false)
const matchResult = ref<any>(null)

// 计算是否可以匹配
const canMatch = computed(() => {
  return codes.value.every(code => code.length === 4)
})

// 团队匹配函数
const matchTeamTraits = async () => {
  if (!canMatch.value) return
  
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

// 重置匹配
const resetMatch = () => {
  codes.value = ['', '', '', '']
  matchResult.value = null
}
</script>