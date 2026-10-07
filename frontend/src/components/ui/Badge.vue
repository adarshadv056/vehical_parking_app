<script>
export default {
  name: 'AppBadge',
  props: {
    variant: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'available', 'occupied', 'warning', 'info', 'success', 'danger'].includes(v)
    },
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg'].includes(v)
    },
    dot: Boolean,
    removable: Boolean,
    text: String
  },
  emits: ['remove'],
  computed: {
    classes() {
      return [
        'app-badge',
        `app-badge--${this.variant}`,
        `app-badge--${this.size}`,
        this.dot && 'app-badge--dot',
        this.removable && 'app-badge--removable'
      ].join(' ');
    }
  },
  methods: {
    onRemove(event) {
      event.stopPropagation();
      this.$emit('remove');
    }
  }
};
</script>

<template>
  <span :class="classes" v-bind="$attrs">
    <span v-if="dot" class="app-badge__dot" :class="`app-badge__dot--${variant}`" aria-hidden="true" />
    <span class="app-badge__text">
      <template v-if="text">{{ text }}</template>
      <slot v-else />
    </span>
    <button
      v-if="removable"
      type="button"
      class="app-badge__remove"
      @click="onRemove"
      aria-label="Remove"
    >
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <path d="M18 6L6 18M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </span>
</template>

<style scoped>
.app-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1, 4px);
  font-weight: var(--font-weight-semibold, 600);
  border-radius: var(--radius-pill, 9999px);
  white-space: nowrap;
}

.app-badge--sm {
  padding: 2px var(--space-2, 8px);
  font-size: var(--font-size-xs, 11px);
  height: 20px;
}

.app-badge--md {
  padding: 4px var(--space-2, 8px);
  font-size: var(--font-size-xs, 12px);
  height: 24px;
}

.app-badge--lg {
  padding: 6px var(--space-3, 12px);
  font-size: var(--font-size-sm, 14px);
  height: 28px;
}

.app-badge__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.app-badge__dot--available { background: var(--color-status-available); }
.app-badge__dot--occupied { background: var(--color-status-occupied); }
.app-badge__dot--warning { background: var(--color-status-warning); }
.app-badge__dot--info { background: var(--color-status-info); }
.app-badge__dot--success { background: var(--color-status-available); }
.app-badge__dot--danger { background: var(--color-status-occupied); }
.app-badge__dot--default { background: var(--color-text-muted); }

.app-badge--removable {
  padding-right: var(--space-1, 4px);
}

.app-badge__remove {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  margin-left: var(--space-1, 4px);
  color: currentColor;
  opacity: 0.7;
  transition: opacity var(--transition-fast), background var(--transition-fast);
}

.app-badge__remove:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.1);
}

/* Variants */
.app-badge--available {
  background: var(--color-status-available-bg);
  color: var(--color-status-available);
}

.app-badge--occupied {
  background: var(--color-status-occupied-bg);
  color: var(--color-status-occupied);
}

.app-badge--warning {
  background: var(--color-status-warning-bg);
  color: var(--color-status-warning);
}

.app-badge--info {
  background: var(--color-status-info-bg);
  color: var(--color-status-info);
}

.app-badge--success {
  background: var(--color-status-available-bg);
  color: var(--color-status-available);
}

.app-badge--danger {
  background: var(--color-status-occupied-bg);
  color: var(--color-status-occupied);
}

.app-badge--default {
  background: var(--color-bg-muted);
  color: var(--color-text-secondary);
}
</style>