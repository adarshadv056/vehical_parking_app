<script>
export default {
  name: 'AppSpinner',
  props: {
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg', 'xl'].includes(v)
    },
    variant: {
      type: String,
      default: 'primary',
      validator: (v) => ['primary', 'white', 'current'].includes(v)
    },
    label: String
  },
  computed: {
    sizeClass() {
      return `app-spinner--${this.size}`;
    },
    variantClass() {
      return `app-spinner--${this.variant}`;
    },
    svgSize() {
      const map = { sm: 16, md: 24, lg: 36, xl: 48 };
      return map[this.size] || 24;
    },
    strokeWidth() {
      const map = { sm: 2, md: 3, lg: 4, xl: 5 };
      return map[this.size] || 3;
    }
  }
};
</script>

<template>
  <div
    :class="['app-spinner', sizeClass, variantClass]"
    role="status"
    :aria-label="label || 'Loading'"
  >
    <svg
      :width="svgSize"
      :height="svgSize"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        :stroke-width="strokeWidth"
        stroke-linecap="round"
        stroke-dasharray="31.4 31.4"
        class="app-spinner__track"
      />
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        :stroke-width="strokeWidth"
        stroke-linecap="round"
        stroke-dasharray="31.4 31.4"
        class="app-spinner__indicator"
        style="animation: app-spinner-spin 1s linear infinite"
      />
    </svg>
    <span v-if="label" class="app-spinner__label">{{ label }}</span>
  </div>
</template>

<style scoped>
.app-spinner {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3, 12px);
  color: var(--color-brand-primary);
}

.app-spinner--sm { --size: 16px; }
.app-spinner--md { --size: 24px; }
.app-spinner--lg { --size: 36px; }
.app-spinner--xl { --size: 48px; }

.app-spinner--primary { color: var(--color-brand-primary); }
.app-spinner--white { color: var(--color-text-inverse); }
.app-spinner--current { color: currentColor; }

.app-spinner svg {
  animation: app-spinner-rotate 1s linear infinite;
}

@keyframes app-spinner-rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.app-spinner__track {
  opacity: 0.2;
}

.app-spinner__indicator {
  stroke-dasharray: 31.4 31.4;
  stroke-dashoffset: 0;
  animation: app-spinner-dash 1.5s ease-in-out infinite;
}

@keyframes app-spinner-dash {
  0% { stroke-dasharray: 1, 31.4; stroke-dashoffset: 0; }
  50% { stroke-dasharray: 31.4, 31.4; stroke-dashoffset: -15.7; }
  100% { stroke-dasharray: 31.4, 31.4; stroke-dashoffset: -31.4; }
}

.app-spinner__label {
  font-size: var(--font-size-sm, 14px);
  color: var(--color-text-secondary);
  text-align: center;
  white-space: nowrap;
}
</style>