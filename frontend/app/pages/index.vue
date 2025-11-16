<template>
  <div class="min-h-screen bg-white">
    <!-- 导航栏 -->
    <nav class="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
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
            <NuxtLink to="/match" class="text-gray-600 hover:text-blue-600 transition-colors duration-200">双人匹配</NuxtLink>
            <NuxtLink to="/team-match" class="text-gray-600 hover:text-blue-600 transition-colors duration-200">团队匹配</NuxtLink>
            <NuxtLink to="/word-cloud" class="text-gray-600 hover:text-blue-600 transition-colors duration-200">词云生成</NuxtLink>
            <NuxtLink to="/desktop-builder" class="text-gray-600 hover:text-blue-600 transition-colors duration-200">桌面搭建</NuxtLink>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- 标题区域 -->
      <div class="text-center mb-16">
        <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          宿舍文化节
        </h1>
        <p class="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          发现你的最佳室友特质，打造理想寝室环境
        </p>
      </div>

      <!-- 功能卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
        <!-- 特质测试卡片 -->
        <div class="bg-white border border-gray-200 rounded-xl p-8 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
          <div class="w-16 h-16 bg-blue-100 rounded-xl flex items-center justify-center mb-6">
            <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-3">特质测试</h3>
          <p class="text-gray-600 text-sm mb-6">
            通过答题推断个人特质，获得4位唯一代码
          </p>
          <NuxtLink 
            to="/quiz" 
            class="inline-flex items-center justify-center w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200"
          >
            开始测试
          </NuxtLink>
        </div>

        <!-- 双人匹配卡片 -->
        <div class="bg-white border border-gray-200 rounded-xl p-8 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
          <div class="w-16 h-16 bg-green-100 rounded-xl flex items-center justify-center mb-6">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-3">双人匹配</h3>
          <p class="text-gray-600 text-sm mb-6">
            输入两个4位代码，查看双人特质匹配度
          </p>
          <NuxtLink 
            to="/match" 
            class="inline-flex items-center justify-center w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200"
          >
            开始匹配
          </NuxtLink>
        </div>

        <!-- 团队匹配卡片 -->
        <div class="bg-white border border-gray-200 rounded-xl p-8 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
          <div class="w-16 h-16 bg-orange-100 rounded-xl flex items-center justify-center mb-6">
            <svg class="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-3">团队匹配</h3>
          <p class="text-gray-600 text-sm mb-6">
            输入四个4位代码，查看团队特质匹配度
          </p>
          <NuxtLink 
            to="/team-match" 
            class="inline-flex items-center justify-center w-full bg-orange-600 hover:bg-orange-700 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200"
          >
            开始匹配
          </NuxtLink>
        </div>

        <!-- 词云生成卡片 -->
        <div class="bg-white border border-gray-200 rounded-xl p-8 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
          <div class="w-16 h-16 bg-purple-100 rounded-xl flex items-center justify-center mb-6">
            <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-3">词云生成</h3>
          <p class="text-gray-600 text-sm mb-6">
            选择理想室友特质，生成非常好看的词云
          </p>
          <NuxtLink 
            to="/word-cloud" 
            class="inline-flex items-center justify-center w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200"
          >
            开始体验
          </NuxtLink>
        </div>

        <!-- 桌面搭建卡片 -->
        <div class="bg-white border border-gray-200 rounded-xl p-8 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
          <div class="w-16 h-16 bg-orange-100 rounded-xl flex items-center justify-center mb-6">
            <svg class="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-3">桌面搭建</h3>
          <p class="text-gray-600 text-sm mb-6">
            拖拽元素打造理想寝室桌面，支持旋转缩放
          </p>
          <NuxtLink 
            to="/desktop-builder" 
            class="inline-flex items-center justify-center w-full bg-orange-600 hover:bg-orange-700 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200"
          >
            开始搭建
          </NuxtLink>
        </div>
      </div>

      <!-- 功能特性 -->
      <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-12 mb-16">
        <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">功能特性</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">10+ 特质维度</h3>
            <p class="text-gray-600 text-sm">全面覆盖个人生活习惯和性格特点</p>
          </div>
          
          <div class="text-center">
            <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg class="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">4位唯一代码</h3>
            <p class="text-gray-600 text-sm">简洁易记，便于分享和匹配</p>
          </div>
          
          <div class="text-center">
            <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg class="w-6 h-6 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">智能匹配算法</h3>
            <p class="text-gray-600 text-sm">基于特质相似度计算匹配度</p>
          </div>
          
          <div class="text-center">
            <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg class="w-6 h-6 text-orange-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">可视化桌面</h3>
            <p class="text-gray-600 text-sm">拖拽式搭建，个性化寝室环境</p>
          </div>
        </div>
      </div>

      <!-- 行动号召 -->
      <div class="text-center bg-white rounded-2xl p-12 shadow-lg">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">立即开始探索</h2>
        <p class="text-gray-600 mb-8 text-lg max-w-2xl mx-auto">
          从特质测试到桌面搭建，全方位打造理想的宿舍生活体验
        </p>
        <div class="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6">
          <NuxtLink 
            to="/quiz" 
            class="inline-flex items-center px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition-all duration-200 transform hover:scale-105"
          >
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            开始特质测试
          </NuxtLink>
          
          <NuxtLink 
            to="/desktop-builder" 
            class="inline-flex items-center px-8 py-4 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-xl transition-all duration-200 transform hover:scale-105"
          >
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/>
            </svg>
            体验桌面搭建
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="bg-gray-50 border-t border-gray-200 mt-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="text-center text-gray-600">
          <p class="text-lg">© 2024 宿舍文化节特质匹配系统</p>
          <p class="text-sm mt-2">打造理想的宿舍生活体验</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// 设置页面元信息
useSeoMeta({
  title: '宿舍文化节 - 特质匹配与桌面搭建系统',
  description: '通过答题推断个人特质，获得4位唯一代码，与室友进行特质匹配，并体验拖拽式桌面搭建功能'
})

// 页面配置
definePageMeta({
  layout: false
})
</script>

<style scoped>
/* 平滑过渡效果 */
.transition-all {
  transition: all 0.3s ease-in-out;
}

/* 悬停效果增强 */
.hover\:shadow-lg:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 链接样式优化 */
.nuxt-link-active {
  color: #2563eb;
}
</style>