<template>
  <div class="min-h-screen bg-white">
    <!-- 导航栏 -->
    <nav class="bg-white border-b border-gray-200">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
              </svg>
            </div>
            <span class="text-xl font-bold text-gray-900">宿舍文化节</span>
          </div>
          <div class="hidden md:flex items-center space-x-8">
            <NuxtLink to="/quiz" class="text-gray-600 hover:text-blue-600 transition-colors duration-200">特质测试</NuxtLink>
            <NuxtLink to="/match" class="text-gray-600 hover:text-blue-600 transition-colors duration-200">特质匹配</NuxtLink>
            <NuxtLink to="/word-cloud" class="text-gray-600 hover:text-blue-600 transition-colors duration-200">词云生成</NuxtLink>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <!-- 标题区域 -->
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          宿舍文化节
        </h1>
        <p class="text-lg text-gray-600 mb-8">
          发现你的最佳室友特质
        </p>
      </div>

      <!-- 功能卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <!-- 特质测试卡片 -->
        <div class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-200">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">特质测试</h3>
          <p class="text-gray-600 text-sm mb-4">
            通过答题推断个人特质，获得4位唯一代码
          </p>
          <NuxtLink 
            to="/quiz" 
            class="inline-block w-full bg-blue-600 hover:bg-blue-700 text-white text-center py-2 px-4 rounded-md transition-colors duration-200"
          >
            开始测试
          </NuxtLink>
        </div>

        <!-- 特质匹配卡片 -->
        <div class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-200">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">特质匹配</h3>
          <p class="text-gray-600 text-sm mb-4">
            输入两个4位代码，查看特质匹配度
          </p>
          <NuxtLink 
            to="/match" 
            class="inline-block w-full bg-green-600 hover:bg-green-700 text-white text-center py-2 px-4 rounded-md transition-colors duration-200"
          >
            开始匹配
          </NuxtLink>
        </div>

        <!-- 词云生成卡片 -->
        <div class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-200">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">词云生成</h3>
          <p class="text-gray-600 text-sm mb-4">
            选择理想室友特质，生成专属词云
          </p>
          <NuxtLink 
            to="/word-cloud" 
            class="inline-block w-full bg-purple-600 hover:bg-purple-700 text-white text-center py-2 px-4 rounded-md transition-colors duration-200"
          >
            开始体验
          </NuxtLink>
        </div>
      </div>

      <!-- 功能特性 -->
      <div class="bg-gray-50 rounded-lg p-8 mb-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 text-center">功能特性</h2>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div class="flex items-center">
            <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
            10+ 特质维度
          </div>
          <div class="flex items-center">
            <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
            4位唯一代码
          </div>
          <div class="flex items-center">
            <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
            智能匹配算法
          </div>
          <div class="flex items-center">
            <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
            无需个人信息
          </div>
        </div>
      </div>

      <!-- 行动号召 -->
      <div class="text-center">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">立即开始特质测试</h2>
        <p class="text-gray-600 mb-6">
          通过简单的答题即可获得专属特质代码，与室友进行精准匹配
        </p>
        <div class="space-x-4">
          <NuxtLink 
            to="/quiz" 
            class="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            开始特质测试
          </NuxtLink>
          
          <NuxtLink 
            to="/match" 
            class="inline-flex items-center px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
            </svg>
            特质匹配
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="bg-gray-100 border-t border-gray-200 mt-16">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="text-center text-gray-600">
          <p>© 2024 宿舍文化节特质匹配系统</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// 设置页面元信息
useSeoMeta({
  title: '宿舍文化节 - 特质匹配系统',
  description: '通过答题推断个人特质，获得4位唯一代码，与室友进行特质匹配'
})

// 页面配置
definePageMeta({
  layout: false
})
</script>

<style scoped>
/* 自定义样式 */
</style>