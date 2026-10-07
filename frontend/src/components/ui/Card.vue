<script>
export default {
  name: 'AppCard',
  inheritAttrs: false,
  props: {
    variant: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'elevated', 'outlined', 'filled'].includes(v)
    },
    padding: {
      type: String,
      default: 'md',
      validator: (v) => ['none', 'sm', 'md', 'lg'].includes(v)
    },
    hoverable: Boolean,
    clickable: Boolean
  },
  computed: {
    classes() {
      const base = 'app-card';
      const variant = `app-card--${this.variant}`;
      const padding = this.padding !== 'md' ? `app-card--p-${this.padding}` : '';
      const states = [
        this.hoverable && 'app-card--hoverable',
        this.clickable && 'app-card--clickable'
      ].filter(Boolean);
      return [base, variant, padding, ...states].join(' ');
    },
    paddingStyle() {
      if (this.padding === 'none') return { padding: 0 };
      const map = {
        sm: 'var(--card-padding-sm, 12px)',
        md: 'var(--card-padding, 24px)',
        lg: '32px'
      };
      return { padding: map[this.padding] };
    }
  }
};
</script>

<template>
  <div
    :class="classes"
    :style="paddingStyle"
    role="region"
    :tabindex="clickable ? 0 : undefined"
    @click="$emit('click', $event)"
    @keydown.enter="$emit('click', $event)"
    v-bind="$attrs"
  >
    <slot name="header" />
    <div class="app-card__body">
      <slot />
    </div>
    <slot name="footer" />
  </div>
</template>

<style scoped>
.app-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg, 16px);
  transition: box-shadow var(--transition-normal), transform var(--transition-fast);
  display: flex;
  flex-direction: column;
}

.app-card--default {
  border: 1px solid var(--color-border-default);
}

.app-card--elevated {
  border: none;
  box-shadow: var(--shadow-md);
}

.app-card--outlined {
  border: 2px solid var(--color-border-default);
}

.app-card--filled {
  background: var(--color-bg-muted);
  border: none;
}

.app-card--p-sm {
  padding: var(--card-padding-sm, 16px);
}

.app-card--p-lg {
  padding: 32px;
}

.app-card__body {
  flex: 1;
}

.app-card--hoverable:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.app-card--clickable {
  cursor: pointer;
}

.app-card--clickable:focus-visible {
  outline: 2px solid var(--color-brand-primary);
  outline-offset: 2px;
}

/* Header/Footer slots styling */
.app-card > :first-child:not(.app-card__body) {
  border-bottom: 1px solid var(--color-border-default);
  padding-bottom: var(--space-4);
  margin-bottom: var(--space-4);
}

.app-card > :last-child:not(.app-card__body) {
  border-top: 1px solid var(--color-border-default);
  padding-top: var(--space-4);
  margin-top: var(--space-4);
}
</style>