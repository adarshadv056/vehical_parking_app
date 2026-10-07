<script setup>
/* eslint-disable no-undef */
import { reactive, computed } from 'vue'
import AppToast from '@/components/ui/Toast.vue'

const state = reactive({
  toasts: [],
  idCounter: 0
})

const add = (options) => {
  const id = ++state.idCounter
  const toast = {
    id,
    message: options.message,
    type: options.type || 'info',
    duration: options.duration ?? 4000,
    closable: options.closable ?? true,
    action: options.action || null
  }
  state.toasts.push(toast)
  return id
}

const remove = (id) => {
  const index = state.toasts.findIndex(t => t.id === id)
  if (index > -1) {
    state.toasts.splice(index, 1)
  }
}

const shortcuts = {
  success: (message, opts = {}) => add({ ...opts, message, type: 'success' }),
  error: (message, opts = {}) => add({ ...opts, message, type: 'error' }),
  warning: (message, opts = {}) => add({ ...opts, message, type: 'warning' }),
  info: (message, opts = {}) => add({ ...opts, message, type: 'info' }),
  remove,
  clear: () => { state.toasts = [] }
}

defineExpose({
  // eslint-disable-next-line no-undef
  ...shortcuts,
  toasts: computed(() => state.toasts)
})
</script>

<template>
  <div class="app-toast-host" aria-live="polite" aria-atomic="true">
    <TransitionGroup name="app-toast-list" tag="div" class="app-toast-list">
      <AppToast
        v-for="toast in state.toasts"
        :key="toast.id"
        :id="toast.id"
        :message="toast.message"
        :type="toast.type"
        :duration="toast.duration"
        :closable="toast.closable"
        :action="toast.action"
        @close="remove"
      />
    </TransitionGroup>
  </div>
</template>

<style scoped>
.app-toast-host {
  position: fixed;
  top: var(--space-6, 24px);
  right: var(--space-6, 24px);
  z-index: var(--z-toast, 800);
  pointer-events: none;
  max-width: 420px;
}

.app-toast-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3, 12px);
}

.app-toast-list > * {
  pointer-events: auto;
}
</style>