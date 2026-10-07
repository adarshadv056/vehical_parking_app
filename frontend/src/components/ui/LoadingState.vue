<script>
export default {
  name: 'AppLoadingState',
  props: {
    type: {
      type: String,
      default: 'spinner',
      validator: (v) => ['spinner', 'skeleton', 'dots', 'pulse'].includes(v)
    },
    count: { type: Number, default: 3 },
    variant: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'card', 'table', 'list'].includes(v)
    },
    showLabel: Boolean,
    label: String
  },
  computed: {
    skeletonClasses() {
      return [
        'app-loading-skeleton',
        `app-loading-skeleton--${this.variant}`
      ].join(' ');
    }
  }
};
</script>

<template>
  <div v-if="type === 'spinner'" class="app-loading-spinner" role="status" aria-live="polite">
    <AppSpinner :size="size" :label="label" />
    <p v-if="showLabel && label" class="app-loading-spinner__label">{{ label }}</p>
  </div>
  <div v-else-if="type === 'dots'" class="app-loading-dots" role="status" aria-live="polite" aria-label="Loading">
    <span class="app-loading-dots__dot" style="animation-delay: 0ms"></span>
    <span class="app-loading-dots__dot" style="animation-delay: 150ms"></span>
    <span class="app-loading-dots__dot" style="animation-delay: 300ms"></span>
  </div>
  <div v-else-if="type === 'pulse'" class="app-loading-pulse" aria-hidden="true">
    <div class="app-loading-pulse__bar"></div>
    <div class="app-loading-pulse__bar"></div>
    <div class="app-loading-pulse__bar"></div>
    <div class="app-loading-pulse__bar"></div>
    <div class="app-loading-pulse__bar"></div>
  </div>
  <div v-else class="app-loading-skeleton-container" aria-hidden="true">
    <template v-for="i in count" :key="i">
      <div :class="skeletonClasses" />
    </template>
  </div>
</template>

<style scoped>
/* Spinner variant */
.app-loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-8, 32px);
  gap: var(--space-3, 12px);
}

.app-loading-spinner__label {
  margin: 0;
  font-size: var(--font-size-sm, 14px);
  color: var(--color-text-secondary);
  text-align: center;
}

/* Dots variant */
.app-loading-dots {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2, 8px);
  padding: var(--space-4, 16px);
}

.app-loading-dots__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-brand-primary);
  animation: app-loading-dots-bounce 1.4s ease-in-out infinite both;
}

.app-loading-dots__dot:nth-child(2) { animation-delay: 0.16s; }
.app-loading-dots__dot:nth-child(3) { animation-delay: 0.32s; }

@keyframes app-loading-dots-bounce {
  0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

/* Pulse variant */
.app-loading-pulse {
  display: flex;
  gap: var(--space-3, 12px);
  height: 20px;
}

.app-loading-pulse__bar {
  flex: 1;
  height: 100%;
  border-radius: var(--radius-pill, 9999px);
  background: linear-gradient(90deg, var(--color-bg-muted) 25%, var(--color-border-default) 50%, var(--color-bg-muted) 75%);
  background-size: 200% 100%;
  animation: app-loading-pulse-shimmer 1.5s ease-in-out infinite;
}

@keyframes app-loading-pulse-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Skeleton variants */
.app-loading-skeleton {
  background: linear-gradient(90deg, var(--color-bg-muted) 25%, var(--color-border-default) 50%, var(--color-bg-muted) 75%);
  background-size: 200% 100%;
  animation: app-loading-skeleton-shimmer 1.5s ease-in-out infinite;
  border-radius: var(--radius-md, 12px);
}

@keyframes app-loading-skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.app-loading-skeleton--default {
  height: 16px;
  width: 100%;
  border-radius: var(--radius-sm, 8px);
}

.app-loading-skeleton--card {
  height: 200px;
  width: 100%;
  border-radius: var(--radius-lg, 16px);
}

.app-loading-skeleton--table {
  height: 48px;
  width: 100%;
}

.app-loading-skeleton--list {
  height: 64px;
  width: 100%;
  border-radius: var(--radius-md, 12px);
}

.app-loading-skeleton-container {
  display: flex;
  flex-direction: column;
  gap: var(--space-4, 16px);
}
</style>