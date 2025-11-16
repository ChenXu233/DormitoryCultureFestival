<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
    <div class="max-w-md w-full text-center">
      <!-- 标题 -->
      <h1 class="text-4xl font-bold text-gray-800 mb-4">
        宿舍文化节
      </h1>
      <p class="text-lg text-gray-600 mb-8">
        发现你的最佳室友特质
      </p>
      
      <!-- 功能卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <!-- 词云功能卡片 -->
        <div class="bg-white rounded-xl shadow-lg p-8">
          <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/>
            </svg>
          </div>
          <h2 class="text-xl font-semibold text-gray-800 mb-2">
            最佳室友词云
          </h2>
          <p class="text-gray-600 mb-6">
            选择你心目中的理想室友特质，生成专属词云
          </p>
          
          <!-- 导航按钮 -->
          <NuxtLink 
            to="/word-cloud" 
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 inline-block"
          >
            开始体验
          </NuxtLink>
        </div>

        <!-- 答题功能卡片 -->
        <div class="bg-white rounded-xl shadow-lg p-8">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h2 class="text-xl font-semibold text-gray-800 mb-2">
            室友默契度答题
          </h2>
          <p class="text-gray-600 mb-6">
            测试你和室友的默契程度，看看你们有多了解彼此
          </p>
          
          <!-- 导航按钮 -->
          <NuxtLink 
            to="/quiz" 
            class="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 inline-block"
          >
            开始答题
          </NuxtLink>
        </div>

        <!-- 桌面搭建功能卡片 -->
        <div class="bg-white rounded-xl shadow-lg p-8">
          <div class="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"/>
            </svg>
          </div>
          <h2 class="text-xl font-semibold text-gray-800 mb-2">
            寝室桌面搭建
          </h2>
          <p class="text-gray-600 mb-6">
            拖拽元素到桌面上，打造你理想的寝室桌面
          </p>
          
          <!-- 导航按钮 -->
          <NuxtLink 
            to="/desktop-builder" 
            class="w-full bg-orange-600 hover:bg-orange-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 inline-block"
          >
            开始搭建
          </NuxtLink>
        </div>
      </div>
      
      <!-- 功能特性 -->
      <div class="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-6">
        <div class="flex items-center justify-center">
          <svg class="w-4 h-4 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
          50+ 特质词汇
        </div>
        <div class="flex items-center justify-center">
          <svg class="w-4 h-4 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
          多主题选择
        </div>
        <div class="flex items-center justify-center">
          <svg class="w-4 h-4 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
          图片下载分享
        </div>
        <div class="flex items-center justify-center">
          <svg class="w-4 h-4 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
          偏好记录
        </div>
      </div>

      <!-- 排行榜入口 -->
      <div class="text-center">
        <NuxtLink 
          to="/quiz-leaderboard" 
          class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-medium rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/>
          </svg>
          查看室友默契度排行榜
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 设置页面元信息
useSeoMeta({
  title: '宿舍文化节 - 最佳室友词云',
  description: '选择你心目中的理想室友特质，生成专属词云，发现最佳室友匹配度'
})

// 页面配置
definePageMeta({
  layout: false
})
</script>

<style scoped>
/* 自定义样式 */
</style>