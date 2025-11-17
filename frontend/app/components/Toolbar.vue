<template>
  <div class="toolbar flex flex-wrap justify-between items-center bg-white rounded-lg shadow-sm p-4 mb-4">
    <h2 class="text-xl font-semibold text-gray-800 mb-2 sm:mb-0">我的桌面</h2>
    <div class="flex space-x-2">
      <button 
        class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
        @click="$emit('clear')"
      >
        清空桌面
      </button>
      <button 
        class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
        @click="$emit('save')"
      >
        保存配置
      </button>
      <button 
        class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
        @click="$emit('download')"
      >
        下载图片
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
// 定义组件事件
interface Emits {
  (e: 'clear'): void
  (e: 'save'): void
  (e: 'download'): void
}

// 组件事件
const emit = defineEmits<Emits>()
</script>

<style scoped>
/* 工具栏样式 */
.toolbar {
  background-color: white;
  border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    gap: 12px;
  }
  
  .toolbar .flex.space-x-2 {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 480px) {
  .toolbar .flex.space-x-2 {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .toolbar .flex.space-x-2 button {
    flex: 1;
    min-width: calc(50% - 4px);
  }
}
</style>