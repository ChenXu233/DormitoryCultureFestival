<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <EventHeader />
    <main class="flex-1 flex w-full">
      <div class="min-h-full w-full">
        <NuxtPage />
      </div>
    </main>
    <footer class="text-center text-xs text-gray-500">
      © {{ new Date().getFullYear() }} 信息科学与工程学院 · CIC计算机信息交流协会
    </footer>
  </div>
</template>

<script setup lang="ts">
import EventHeader from '../components/EventHeader.vue'
</script>
