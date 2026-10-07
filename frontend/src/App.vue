<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppShell from '@/components/layout/AppShell.vue'
import AppToastHost from '@/components/feedback/ToastHost.vue'

const route = useRoute()

const layoutVariant = computed(() => {
  if (['Login', 'Register'].includes(route.name)) return 'auth'
  if (route.name === 'Home') return 'landing'
  return 'app'
})
</script>

<template>
  <AppShell :variant="layoutVariant">
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </AppShell>
  <AppToastHost />
</template>

<style scoped>
/* Page transition */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>