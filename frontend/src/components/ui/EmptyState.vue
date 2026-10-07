<script>
import AppButton from './Button.vue';

export default {
  name: 'AppEmptyState',
  components: { AppButton },
  props: {
    icon: { type: String, default: 'InboxIcon' },
    title: { type: String, default: 'No data available' },
    description: { type: String, default: 'There is nothing to show here yet.' },
    action: { type: Object, default: null }, // { label, onClick, variant }
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg'].includes(v)
    }
  },
  computed: {
    classes() {
      return `app-empty-state app-empty-state--${this.size}`;
    }
  }
};
</script>

<template>
  <div :class="classes" class="app-empty-state" role="status" aria-live="polite">
    <div class="app-empty-state__icon">
      <component :is="icon" :class="['app-empty-state__icon-svg', `app-empty-state__icon-svg--${size}`]" />
    </div>
    <h3 class="app-empty-state__title">{{ title }}</h3>
    <p v-if="description" class="app-empty-state__description">{{ description }}</p>
    <div v-if="action" class="app-empty-state__action">
      <AppButton :variant="action.variant || 'primary'" @click="action.onClick">
        {{ action.label }}
      </AppButton>
    </div>
  </div>
</template>

<style scoped>
.app-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--space-8, 32px) var(--space-6, 24px);
  background: var(--color-bg-white);
  border-radius: var(--radius-lg, 16px);
  border: 1px solid var(--color-border-default);
}

.app-empty-state--sm { padding: var(--space-4, 16px); }
.app-empty-state--lg { padding: var(--space-12, 48px); }

.app-empty-state__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--color-bg-muted);
  color: var(--color-text-muted);
  margin: 0 auto var(--space-4, 16px);
}

.app-empty-state__icon-svg--sm { width: 24px; height: 24px; }
.app-empty-state__icon-svg--md { width: 32px; height: 32px; }
.app-empty-state__icon-svg--lg { width: 48px; height: 48px; }

.app-empty-state__icon-svg {
  width: 32px;
  height: 32px;
  color: var(--color-text-muted);
}

.app-empty-state__title {
  margin: 0 0 var(--space-2, 8px);
  font-size: var(--font-size-lg, 18px);
  font-weight: var(--font-weight-bold, 700);
  color: var(--color-text-primary);
}

.app-empty-state__description {
  margin: 0 0 var(--space-5, 20px);
  font-size: var(--font-size-sm, 14px);
  color: var(--color-text-secondary);
  max-width: 320px;
}

.app-empty-state__action {
  margin-top: var(--space-2, 8px);
}
</style>