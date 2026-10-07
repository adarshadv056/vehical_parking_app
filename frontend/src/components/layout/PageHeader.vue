<script>
import AppButton from '@/components/ui/Button.vue';

export default {
  name: 'AppPageHeader',
  inheritAttrs: false,
  components: { AppButton },
  props: {
    title: { type: String, required: true },
    subtitle: String,
    breadcrumbs: { type: Array, default: () => [] },
    actions: { type: Array, default: () => [] },
    backRoute: { type: [String, Object], default: null }
  },
  computed: {
    hasBack() {
      return !!this.backRoute;
    }
  },
  methods: {
    goBack() {
      if (typeof this.backRoute === 'string') {
        this.$router.push(this.backRoute);
      } else {
        this.$router.push(this.backRoute);
      }
    }
  }
};
</script>

<template>
  <header class="app-page-header" v-bind="$attrs">
    <div class="app-page-header__breadcrumbs" v-if="breadcrumbs.length">
      <ol class="app-page-header__breadcrumb-list" aria-label="Breadcrumb">
        <li v-for="(crumb, index) in breadcrumbs" :key="index" class="app-page-header__breadcrumb-item">
          <router-link
            v-if="index < breadcrumbs.length - 1 && crumb.to"
            :to="crumb.to"
            class="app-page-header__breadcrumb-link"
          >
            {{ crumb.label }}
          </router-link>
          <span
            v-else
            class="app-page-header__breadcrumb-current"
            :aria-current="index === breadcrumbs.length - 1 ? 'page' : undefined"
          >
            {{ crumb.label }}
          </span>
          <svg
            v-if="index < breadcrumbs.length - 1"
            class="app-page-header__breadcrumb-separator"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            aria-hidden="true"
          >
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </li>
      </ol>
    </div>

    <div class="app-page-header__content">
      <div class="app-page-header__title-group">
        <button
          v-if="hasBack"
          type="button"
          class="app-page-header__back"
          @click="goBack"
          aria-label="Go back"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </button>
        <div>
          <h1 class="app-page-header__title">{{ title }}</h1>
          <p v-if="subtitle" class="app-page-header__subtitle">{{ subtitle }}</p>
        </div>
      </div>

      <div v-if="actions.length" class="app-page-header__actions">
        <slot name="actions">
          <template v-for="(action, index) in actions" :key="index">
            <AppButton
              :variant="action.variant || 'primary'"
              :size="action.size || 'md'"
              :icon="action.icon"
              :loading="action.loading"
              :disabled="action.disabled"
              @click="action.onClick"
            >
              {{ action.label }}
            </AppButton>
          </template>
        </slot>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-page-header {
  padding: 20px 32px;
  background: var(--color-bg-white);
  border-bottom: 1px solid var(--color-border-default);
  position: sticky;
  top: 0;
  z-index: 90;
}

@media (max-width: 1024px) {
  .app-page-header {
    top: 56px;
    padding: 16px 20px;
  }
}

.app-page-header__breadcrumbs {
  margin-bottom: var(--space-4, 16px);
}

.app-page-header__breadcrumb-list {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-2, 8px);
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: var(--font-size-sm, 14px);
}

.app-page-header__breadcrumb-item {
  display: flex;
  align-items: center;
}

.app-page-header__breadcrumb-link {
  color: var(--color-text-muted);
  font-weight: var(--font-weight-medium, 500);
  transition: color var(--transition-fast);
}

.app-page-header__breadcrumb-link:hover {
  color: var(--color-brand-primary);
}

.app-page-header__breadcrumb-current {
  color: var(--color-text-primary);
  font-weight: var(--font-weight-semibold, 600);
}

.app-page-header__breadcrumb-separator {
  color: var(--color-text-muted);
  flex-shrink: 0;
}

.app-page-header__content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-4, 16px);
}

.app-page-header__title-group {
  display: flex;
  align-items: baseline;
  gap: var(--space-3, 12px);
  flex: 1;
  min-width: 0;
}

.app-page-header__back {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md, 12px);
  color: var(--color-text-muted);
  background: transparent;
  transition: color var(--transition-fast), background var(--transition-fast);
  flex-shrink: 0;
}

.app-page-header__back:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-muted);
}

.app-page-header__title {
  margin: 0;
  font-size: var(--font-size-2xl, 28px);
  font-weight: var(--font-weight-bold, 700);
  color: var(--color-text-primary);
  line-height: var(--line-height-tight, 1.15);
}

.app-page-header__subtitle {
  margin: var(--space-1, 4px) 0 0;
  font-size: var(--font-size-sm, 14px);
  color: var(--color-text-secondary);
  line-height: var(--line-height-normal, 1.5);
}

.app-page-header__actions {
  display: flex;
  align-items: center;
  gap: var(--space-3, 12px);
  flex-wrap: wrap;
  flex-shrink: 0;
}

/* Mobile responsive */
@media (max-width: 640px) {
  .app-page-header {
    padding: var(--space-4, 16px);
  }

  .app-page-header__content {
    flex-direction: column;
    align-items: stretch;
  }

  .app-page-header__actions {
    width: 100%;
    justify-content: stretch;
  }

  .app-page-header__actions > * {
    flex: 1;
  }
}
</style>