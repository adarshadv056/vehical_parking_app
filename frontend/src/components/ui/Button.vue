<script>
import * as Icons from '@/components/icons';

export default {
  name: 'AppButton',
  inheritAttrs: false,
  props: {
    variant: {
      type: String,
      default: 'primary',
      validator: (v) => ['primary', 'secondary', 'dark', 'ghost', 'danger'].includes(v)
    },
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg'].includes(v)
    },
    disabled: Boolean,
    loading: Boolean,
    fullWidth: Boolean,
    type: {
      type: String,
      default: 'button',
      validator: (v) => ['button', 'submit', 'reset'].includes(v)
    },
    pill: Boolean,
    icon: [String, Object],
    iconRight: Boolean
  },
  emits: ['click'],
  computed: {
    classes() {
      const base = 'app-btn';
      const variant = `app-btn--${this.variant}`;
      const size = `app-btn--${this.size}`;
      const states = [
        this.disabled && 'app-btn--disabled',
        this.loading && 'app-btn--loading',
        this.fullWidth && 'app-btn--full',
        this.pill && 'app-btn--pill'
      ].filter(Boolean);
      return [base, variant, size, ...states].join(' ');
    },
    buttonStyle() {
      const styles = {};
      if (this.fullWidth) styles.width = '100%';
      return styles;
    },
    resolvedIcon() {
      if (!this.icon) return null;
      if (typeof this.icon === 'object') return this.icon;
      return Icons[this.icon] || this.icon;
    }
  },
  methods: {
    onClick(event) {
      if (!this.disabled && !this.loading) {
        this.$emit('click', event);
      }
    }
  }
};
</script>

<template>
  <button
    :class="classes"
    :style="buttonStyle"
    :type="type"
    :disabled="disabled || loading"
    @click="onClick"
    v-bind="$attrs"
  >
    <span class="app-btn__content" :class="{ 'app-btn__content--loading': loading }">
      <span v-if="loading" class="app-btn__spinner" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" stroke-linecap="round"
            stroke-dasharray="31.4 31.4" style="animation: app-btn-spin 1s linear infinite" />
        </svg>
      </span>
      <span v-if="resolvedIcon && !iconRight && !loading" class="app-btn__icon" :class="{ 'app-btn__icon--right': iconRight }">
        <component :is="resolvedIcon" class="app-btn__icon-svg" />
      </span>
      <slot />
      <span v-if="resolvedIcon && iconRight && !loading" class="app-btn__icon" :class="{ 'app-btn__icon--right': iconRight }">
        <component :is="resolvedIcon" class="app-btn__icon-svg" />
      </span>
    </span>
  </button>
</template>

<style scoped>
@keyframes app-btn-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.app-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: inherit;
  font-weight: var(--btn-font-weight, 600);
  border: none;
  border-radius: var(--btn-radius, 12px);
  cursor: pointer;
  transition: var(--btn-transition, all 0.2s ease);
  white-space: nowrap;
  text-decoration: none;
  position: relative;
}

.app-btn:focus-visible {
  outline: 2px solid var(--color-brand-primary);
  outline-offset: 2px;
}

.app-btn--disabled,
.app-btn[disabled] {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.app-btn--full {
  width: 100%;
}

.app-btn--pill {
  border-radius: var(--radius-pill);
}

/* Sizes */
.app-btn--sm {
  height: var(--btn-height-sm, 36px);
  padding: 0 var(--btn-padding-x-sm, 16px);
  font-size: var(--font-size-xs, 12px);
  gap: var(--space-2, 8px);
}

.app-btn--md {
  height: var(--btn-height, 44px);
  padding: 0 var(--btn-padding-x, 20px);
  font-size: var(--font-size-sm, 14px);
  gap: var(--space-2, 8px);
}

.app-btn--lg {
  height: var(--btn-height-lg, 52px);
  padding: 0 var(--btn-padding-x-lg, 28px);
  font-size: var(--font-size-base, 16px);
  gap: var(--space-3, 12px);
}

.app-btn__content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2, 8px);
  width: 100%;
}

.app-btn__content--loading {
  color: transparent !important;
}

.app-btn__spinner {
  position: absolute;
  width: 20px;
  height: 20px;
  animation: app-btn-spin 1s linear infinite;
}

.app-btn__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.app-btn__icon--right {
  margin-left: var(--space-1, 4px);
}

.app-btn__icon-svg {
  width: 18px;
  height: 18px;
}

.app-btn--sm .app-btn__icon-svg { width: 14px; height: 14px; }
.app-btn--lg .app-btn__icon-svg { width: 20px; height: 20px; }

/* Variants */
.app-btn--primary {
  background: var(--color-brand-primary);
  color: var(--color-text-inverse);
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
}

.app-btn--primary:hover:not(:disabled) {
  background: var(--color-brand-primary-hover);
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.35);
  transform: translateY(-1px);
}

.app-btn--primary:active:not(:disabled) {
  transform: translateY(0);
}

.app-btn--secondary {
  background: var(--color-bg-white);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-default);
}

.app-btn--secondary:hover:not(:disabled) {
  background: var(--color-bg-muted);
  border-color: var(--color-border-strong);
}

.app-btn--dark {
  background: var(--color-navy-deep);
  color: var(--color-text-inverse);
}

.app-btn--dark:hover:not(:disabled) {
  background: #141c3a;
}

.app-btn--ghost {
  background: transparent;
  color: var(--color-brand-primary);
}

.app-btn--ghost:hover:not(:disabled) {
  background: var(--color-brand-primary-light);
}

.app-btn--danger {
  background: var(--color-status-occupied);
  color: var(--color-text-inverse);
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.25);
}

.app-btn--danger:hover:not(:disabled) {
  background: #dc2626;
  box-shadow: 0 4px 16px rgba(239, 68, 68, 0.35);
  transform: translateY(-1px);
}

/* Icon spacing */
.app-btn__icon + slot,
slot + .app-btn__icon {
  margin: 0 var(--space-1);
}
</style>