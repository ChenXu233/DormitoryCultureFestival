<template>
  <header class="event-header w-full bg-white/90 backdrop-blur border-b border-gray-200 sticky top-0 z-40">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 flex items-center gap-4 py-3">
      <div class="flex items-center gap-3">
        <div class="h-12 w-12 flex items-center justify-center rounded-md bg-gradient-to-br from-blue-500 to-indigo-600 overflow-hidden">
          <img
            v-if="logoExists"
            :src="branding.logoPath"
            :alt="branding.collegeName + ' logo'"
            class="h-full w-full object-contain"
            @error="onLogoError"
          />
          <span v-else class="text-white font-semibold text-lg select-none">院</span>
        </div>
        <div class="leading-tight">
          <h1 class="font-bold text-lg md:text-xl text-gray-900">{{ branding.collegeName }}</h1>
          <p class="text-xs md:text-sm text-gray-600" v-if="branding.slogan">{{ branding.slogan }}</p>
        </div>
      </div>
      <div class="ml-auto flex items-center gap-2">
        <slot name="actions" />
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { branding } from '../config/branding'

const logoExists = ref(true)
const onLogoError = () => { logoExists.value = false }
</script>

<style scoped>
.event-header {
  box-shadow: 0 2px 6px -2px rgba(0,0,0,0.05), 0 4px 12px -4px rgba(0,0,0,0.08);
}
</style>
