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
      <div class="bg-white rounded-xl shadow-lg p-8 mb-6">
        <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path>
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
      
      <!-- 功能特性 -->
      <div class="grid grid-cols-2 gap-4 text-sm text-gray-600">
        <div class="flex items-center justify-center">
          <svg class="w-4 h-4 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
          </svg>
          50+ 特质词汇
        </div>
        <div class="flex items-center justify-center">
          <svg class="w-4 h-4 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
          </svg>
          多主题选择
        </div>
        <div class="flex items-center justify-center">
          <svg class="w-4 h-4 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
          </svg>
          图片下载分享
        </div>
        <div class="flex items-center justify-center">
          <svg class="w-4 h-4 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
          </svg>
          偏好记录
        </div>
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