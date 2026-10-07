<script>
export default {
  name: 'AppToast',
  props: {
    id: { type: [String, Number], required: true },
    message: { type: String, required: true },
    type: {
      type: String,
      default: 'info',
      validator: (v) => ['success', 'error', 'warning', 'info'].includes(v)
    },
    duration: { type: Number, default: 4000 },
    closable: { type: Boolean, default: true },
    action: { type: Object, default: null } // { label, onClick }
  },
  emits: ['close'],
  data() {
    return {
      visible: true,
      progress: 100
    };
  },
  mounted() {
    this.startTimer();
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
  computed: {
    classes() {
      return [
        'app-toast',
        `app-toast--${this.type}`,
        !this.visible && 'app-toast--hiding'
      ].join(' ');
    },
    iconComponent() {
      const map = {
        success: 'CheckCircleIcon',
        error: 'XCircleIcon',
        warning: 'AlertTriangleIcon',
        info: 'InfoIcon'
      };
      return map[this.type] || 'InfoIcon';
    }
  },
  methods: {
    startTimer() {
      if (this.duration <= 0) return;
      const start = Date.now();
      this.timer = setInterval(() => {
        const elapsed = Date.now() - start;
        this.progress = Math.max(0, 100 - (elapsed / this.duration) * 100);
        if (this.progress <= 0) {
          this.close();
        }
      }, 50);
    },
    close() {
      if (!this.visible) return;
      this.visible = false;
      setTimeout(() => this.$emit('close', this.id), 200);
    },
    onMouseEnter() {
      clearInterval(this.timer);
    },
    onMouseLeave() {
      this.startTimer();
    }
  }
};
</script>

<template>
  <Transition name="app-toast">
    <div
      v-show="visible"
      :class="classes"
      class="app-toast"
      role="alert"
      aria-live="polite"
      @mouseenter="onMouseEnter"
      @mouseleave="onMouseLeave"
    >
      <div class="app-toast__icon">
        <component :is="iconComponent" class="app-toast__icon-svg" />
      </div>
      <div class="app-toast__content">
        <p class="app-toast__message">{{ message }}</p>
        <button
          v-if="action"
          type="button"
          class="app-toast__action"
          @click="action.onClick"
        >
          {{ action.label }}
        </button>
      </div>
      <button
        v-if="closable"
        type="button"
        class="app-toast__close"
        @click="close"
        aria-label="Dismiss"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 6L6 18M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      <div
        class="app-toast__progress"
        :style="{ width: progress + '%' }"
        aria-hidden="true"
      />
    </div>
  </Transition>
</template>

<style scoped>
.app-toast {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3, 12px);
  padding: var(--space-4, 16px);
  background: var(--color-bg-white);
  border-radius: var(--radius-lg, 16px);
  box-shadow: var(--shadow-xl);
  border-left: 4px solid;
  min-width: 320px;
  max-width: 420px;
  animation: app-toast-slide-in 0.3s ease;
  position: relative;
  overflow: hidden;
}

@keyframes app-toast-slide-in {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.app-toast--hiding {
  animation: app-toast-slide-out 0.2s ease forwards;
}

@keyframes app-toast-slide-out {
  to {
    opacity: 0;
    transform: translateX(100%);
  }
}

.app-toast--success { border-color: var(--color-status-available); }
.app-toast--error { border-color: var(--color-status-occupied); }
.app-toast--warning { border-color: var(--color-status-warning); }
.app-toast--info { border-color: var(--color-status-info); }

.app-toast__icon {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  margin-top: 2px;
}

.app-toast__icon-svg {
  width: 22px;
  height: 22px;
}

.app-toast--success .app-toast__icon { color: var(--color-status-available); }
.app-toast--error .app-toast__icon { color: var(--color-status-occupied); }
.app-toast--warning .app-toast__icon { color: var(--color-status-warning); }
.app-toast--info .app-toast__icon { color: var(--color-status-info); }

.app-toast__content {
  flex: 1;
  min-width: 0;
}

.app-toast__message {
  margin: 0;
  font-size: var(--font-size-sm, 14px);
  line-height: var(--line-height-normal, 1.5);
  color: var(--color-text-primary);
}

.app-toast__action {
  margin-top: var(--space-2, 8px);
  padding: var(--space-1, 4px) var(--space-3, 12px);
  font-size: var(--font-size-xs, 12px);
  font-weight: var(--font-weight-semibold, 600);
  color: var(--color-brand-primary);
  background: var(--color-brand-primary-light);
  border-radius: var(--radius-pill);
  transition: background var(--transition-fast);
}

.app-toast__action:hover {
  background: var(--color-brand-primary);
  color: white;
}

.app-toast__close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: var(--radius-md, 12px);
  color: var(--color-text-muted);
  flex-shrink: 0;
  margin-left: var(--space-2, 8px);
  transition: color var(--transition-fast), background var(--transition-fast);
}

.app-toast__close:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-muted);
}

.app-toast__progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: currentColor;
  opacity: 0.3;
  transition: width 50ms linear;
}
</style>