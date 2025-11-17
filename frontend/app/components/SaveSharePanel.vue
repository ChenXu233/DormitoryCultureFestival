<template>
  <div class="save-share-panel">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">保存与分享</h2>
    
    <!-- 保存功能 -->
    <div class="mb-6">
      <h3 class="font-medium text-gray-700 mb-3">保存桌面设计</h3>
      <div class="space-y-3">
        <div class="flex space-x-3">
          <button 
            :disabled="isSaving"
            class="flex-1 px-4 py-2 bg-green-500 hover:bg-green-600 disabled:bg-gray-300 text-white rounded-lg transition-colors flex items-center justify-center space-x-2"
            @click="saveDesign"
          >
            <svg v-if="isSaving" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/>
            </svg>
            <span>{{ isSaving ? '保存中...' : '保存设计' }}</span>
          </button>
        </div>
        
        <!-- 设计名称输入 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">设计名称</label>
          <input 
            v-model="designName" 
            type="text"
            placeholder="我的寝室桌面设计"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-blue-500 focus:border-blue-500"
          >
        </div>
        
        <!-- 保存的设计列表 -->
        <div v-if="savedDesigns.length > 0" class="mt-4">
          <h4 class="font-medium text-gray-700 mb-2">已保存的设计</h4>
          <div class="space-y-2 max-h-40 overflow-y-auto">
            <div 
              v-for="design in savedDesigns" 
              :key="design.id"
              class="flex items-center justify-between p-2 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer group"
              @click="loadDesign(design)"
            >
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 rounded bg-blue-100 flex items-center justify-center">
                  <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <div class="text-sm font-medium text-gray-800">{{ design.name }}</div>
                  <div class="text-xs text-gray-500">{{ formatDate(design.createdAt) }}</div>
                </div>
              </div>
              <button 
                class="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-500 transition-opacity"
                @click.stop="deleteDesign(design.id)"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 分享功能 -->
    <div class="border-t pt-6">
      <h3 class="font-medium text-gray-700 mb-3">分享设计</h3>
      <div class="space-y-4">
        <!-- 生成分享链接 -->
        <div>
          <button 
            :disabled="!hasDesignData"
            class="w-full px-4 py-2 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white rounded-lg transition-colors flex items-center justify-center space-x-2"
            @click="generateShareLink"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/>
            </svg>
            <span>生成分享链接</span>
          </button>
        </div>
        
        <!-- 分享链接显示 -->
        <div v-if="shareLink" class="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <div class="text-sm text-blue-800 mb-2">分享链接已生成：</div>
          <div class="flex items-center space-x-2">
            <input 
              type="text" 
              :value="shareLink" 
              readonly
              class="flex-1 px-3 py-1 bg-white border border-blue-300 rounded text-sm text-blue-700"
            >
            <button 
              class="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded text-sm transition-colors"
              @click="copyToClipboard"
            >
              复制
            </button>
          </div>
          <div class="text-xs text-blue-600 mt-1">链接有效期为7天</div>
        </div>
        
        <!-- 分享到社交媒体 -->
        <div v-if="shareLink" class="space-y-2">
          <div class="text-sm text-gray-700">分享到：</div>
          <div class="flex space-x-2">
            <button 
              class="flex-1 px-3 py-2 bg-green-500 hover:bg-green-600 text-white rounded text-sm transition-colors flex items-center justify-center space-x-1"
              @click="shareToWechat"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8.691 2.188C3.891 2.188 0 5.374 0 9.283c0 2.462 1.491 4.638 3.774 5.934-.105.38-.365 1.381-.42 1.603-.077.318-.246.384-.384.246-.246-.21-1.303-.945-1.845-1.429-.246-.21-.246-.21-.246-.42.105-.42.63-1.491.735-1.766C1.071 11.4.63 10.329.63 9.283c0-4.011 4.011-7.095 8.061-7.095s8.061 3.084 8.061 7.095-4.011 7.095-8.061 7.095c-.945 0-1.845-.21-2.73-.525l-2.625.945c-.21.105-.42.105-.525-.105-.105-.21-.105-.42.105-.63l1.26-1.575c-1.26-1.05-2.1-2.625-2.1-4.326 0-3.36 2.94-6.09 6.51-6.09s6.51 2.73 6.51 6.09-2.94 6.09-6.51 6.09c-.42 0-.84-.105-1.26-.21-.21 0-.42 0-.63.105l-.84.42c.315.42.735.84 1.155 1.155.63.525 1.365.945 2.205 1.26.84.315 1.68.42 2.625.42 4.011 0 7.095-3.084 7.095-7.095s-3.084-7.095-7.095-7.095z"/>
              </svg>
              <span>微信</span>
            </button>
            <button 
              class="flex-1 px-3 py-2 bg-blue-400 hover:bg-blue-500 text-white rounded text-sm transition-colors flex items-center justify-center space-x-1"
              @click="shareToQQ"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm-1.5 15.5h-3v-7h3v7zm6.5 0h-3v-7h3v7zm-3.25-9.5h-2.5c-.414 0-.75-.336-.75-.75s.336-.75.75-.75h2.5c.414 0 .75.336.75.75s-.336.75-.75.75z"/>
              </svg>
              <span>QQ</span>
            </button>
          </div>
        </div>
        
        <!-- 导出为图片 -->
        <div class="border-t pt-4">
          <button 
            :disabled="!hasDesignData"
            class="w-full px-4 py-2 bg-purple-500 hover:bg-purple-600 disabled:bg-gray-300 text-white rounded-lg transition-colors flex items-center justify-center space-x-2"
            @click="exportAsImage"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            <span>导出为图片</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- 操作提示 -->
    <div v-if="message" :class="['mt-4 p-3 rounded-lg text-sm', message.type === 'success' ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200']">
      {{ message.text }}
    </div>
  </div>
</template>

<script setup lang="ts">
// 定义设计数据接口
interface DesignData {
  elements: any[]
  background: any
  canvasSize: { width: number; height: number }
}

// 定义保存的设计接口
interface SavedDesign {
  id: string
  name: string
  data: DesignData
  createdAt: Date
  thumbnail?: string
}

// 定义组件属性
interface Props {
  designData?: DesignData
}

// 定义组件事件
interface Emits {
  (e: 'loadDesign', design: SavedDesign): void
  (e: 'exportImage'): void
}

// 组件属性
const props = defineProps<Props>()

// 组件事件
const emit = defineEmits<Emits>()

// 响应式数据
const designName = ref('我的寝室桌面设计')
const isSaving = ref(false)
const shareLink = ref('')
const savedDesigns = ref<SavedDesign[]>([])
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null)

// 计算属性
const hasDesignData = computed(() => {
  return props.designData && props.designData.elements && props.designData.elements.length > 0
})

// 保存设计
const saveDesign = async () => {
  if (!hasDesignData.value) {
    showMessage('请先添加一些元素到桌面', 'error')
    return
  }
  
  if (!designName.value.trim()) {
    showMessage('请输入设计名称', 'error')
    return
  }
  
  isSaving.value = true
  
  try {
    // 模拟保存过程
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const newDesign: SavedDesign = {
      id: Date.now().toString(),
      name: designName.value.trim(),
      data: JSON.parse(JSON.stringify(props.designData)), // 深拷贝
      createdAt: new Date()
    }
    
    // 检查是否已存在同名设计
    const existingIndex = savedDesigns.value.findIndex(d => d.name === newDesign.name)
    if (existingIndex >= 0) {
      savedDesigns.value[existingIndex] = newDesign
    } else {
      savedDesigns.value.unshift(newDesign)
    }
    
    // 保存到本地存储
    localStorage.setItem('savedDesktopDesigns', JSON.stringify(savedDesigns.value))
    
    showMessage('设计保存成功！', 'success')
    designName.value = '我的寝室桌面设计'
    
  } catch (error) {
    showMessage('保存失败，请重试', 'error')
  } finally {
    isSaving.value = false
  }
}

// 加载设计
const loadDesign = (design: SavedDesign) => {
  emit('loadDesign', design)
  showMessage(`已加载设计：${design.name}`, 'success')
}

// 删除设计
const deleteDesign = (id: string) => {
  savedDesigns.value = savedDesigns.value.filter(d => d.id !== id)
  localStorage.setItem('savedDesktopDesigns', JSON.stringify(savedDesigns.value))
  showMessage('设计已删除', 'success')
}

// 生成分享链接
const generateShareLink = () => {
  if (!hasDesignData.value) {
    showMessage('请先创建桌面设计', 'error')
    return
  }
  
  // 模拟生成分享链接
  const baseUrl = window.location.origin
  const shareId = btoa(JSON.stringify(props.designData)).substring(0, 20)
  shareLink.value = `${baseUrl}/share/desktop/${shareId}`
  
  showMessage('分享链接已生成，点击复制按钮分享给朋友', 'success')
}

// 复制到剪贴板
const copyToClipboard = async () => {
  if (!shareLink.value) return
  
  try {
    await navigator.clipboard.writeText(shareLink.value)
    showMessage('链接已复制到剪贴板', 'success')
  } catch (error) {
    // 降级方案
    const textArea = document.createElement('textarea')
    textArea.value = shareLink.value
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    showMessage('链接已复制到剪贴板', 'success')
  }
}

// 分享到微信
const shareToWechat = () => {
  if (!shareLink.value) return
  
  // 模拟微信分享
  const shareUrl = `https://wx.qq.com/sharer/sharer.php?u=${encodeURIComponent(shareLink.value)}`
  window.open(shareUrl, '_blank', 'width=600,height=400')
  showMessage('正在打开微信分享...', 'success')
}

// 分享到QQ
const shareToQQ = () => {
  if (!shareLink.value) return
  
  // 模拟QQ分享
  const shareUrl = `https://connect.qq.com/widget/shareqq/index.html?url=${encodeURIComponent(shareLink.value)}`
  window.open(shareUrl, '_blank', 'width=600,height=400')
  showMessage('正在打开QQ分享...', 'success')
}

// 导出为图片
const exportAsImage = () => {
  if (!hasDesignData.value) {
    showMessage('请先创建桌面设计', 'error')
    return
  }
  
  emit('exportImage')
  showMessage('正在生成图片...', 'success')
}

// 显示消息
const showMessage = (text: string, type: 'success' | 'error') => {
  message.value = { text, type }
  setTimeout(() => {
    message.value = null
  }, 3000)
}

// 格式化日期
const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

// 从本地存储加载保存的设计
onMounted(() => {
  try {
    const saved = localStorage.getItem('savedDesktopDesigns')
    if (saved) {
      savedDesigns.value = JSON.parse(saved).map((d: any) => ({
        ...d,
        createdAt: new Date(d.createdAt)
      }))
    }
  } catch (error) {
    console.error('加载保存的设计失败:', error)
  }
})

// 暴露方法给父组件
defineExpose({
  saveDesign,
  generateShareLink,
  exportAsImage
})
</script>

<style scoped>
/* 滚动条样式 */
.max-h-40::-webkit-scrollbar {
  width: 4px;
}

.max-h-40::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.max-h-40::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.max-h-40::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 动画效果 */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>