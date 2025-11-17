<template>
  <div 
    v-if="visible"
    class="fixed bg-white shadow-lg rounded-lg py-2 z-50 min-w-32"
    :style="{ left: x + 'px', top: y + 'px' }"
    @click.stop
  >
    <button 
      class="w-full px-4 py-2 text-left text-green-600 hover:bg-green-50 flex items-center"
      @click="$emit('edit')"
    >
      <span class="mr-2">✏️</span> 编辑元素
    </button>
    <button 
      class="w-full px-4 py-2 text-left text-blue-600 hover:bg-blue-50 flex items-center"
      @click="$emit('duplicate')"
    >
      <span class="mr-2">📋</span> 复制元素
    </button>
    <button 
      class="w-full px-4 py-2 text-left text-red-600 hover:bg-red-50 flex items-center"
      @click="$emit('delete')"
    >
      <span class="mr-2">🗑️</span> 删除元素
    </button>
    <div class="border-t my-1"></div>
    <button 
      class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
      @click="$emit('rotate', 45)"
    >
      <span class="mr-2">↻</span> 顺时针旋转
    </button>
    <button 
      class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
      @click="$emit('rotate', -45)"
    >
      <span class="mr-2">↺</span> 逆时针旋转
    </button>
    <div class="border-t my-1"></div>
    <button 
      class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
      @click="$emit('bring-to-front')"
    >
      <span class="mr-2">⬆️</span> 置顶
    </button>
    <button 
      class="w-full px-4 py-2 text-left text-purple-600 hover:bg-purple-50 flex items-center"
      @click="$emit('send-to-back')"
    >
      <span class="mr-2">⬇️</span> 置底
    </button>
  </div>
</template>

<script setup lang="ts">
// 定义组件属性
interface Props {
  visible: boolean
  x: number
  y: number
}

// 定义组件事件
interface Emits {
  (e: 'edit'): void
  (e: 'duplicate'): void
  (e: 'delete'): void
  (e: 'rotate', angle: number): void
  (e: 'bring-to-front'): void
  (e: 'send-to-back'): void
}

// 组件属性
const props = defineProps<Props>()

// 组件事件
const emit = defineEmits<Emits>()
</script>

<style scoped>
/* 右键菜单动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>