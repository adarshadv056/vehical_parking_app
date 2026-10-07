<script>
import AppButton from './Button.vue';

export default {
  name: 'AppModal',
  inheritAttrs: false,
  components: { AppButton },
  props: {
    modelValue: Boolean,
    title: String,
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg', 'xl', 'full'].includes(v)
    },
    closeOnOverlay: Boolean,
    closeOnEscape: Boolean,
    showClose: Boolean,
    hideFooter: Boolean
  },
  emits: ['update:modelValue', 'close', 'confirm'],
  data() {
    return {
      isOpen: this.modelValue,
      animating: false
    };
  },
  watch: {
    modelValue(val) {
      this.isOpen = val;
    },
    isOpen(val) {
      this.$emit('update:modelValue', val);
      if (val) {
        document.body.style.overflow = 'hidden';
        this.$nextTick(() => {
          const focusable = this.$refs.content?.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
          focusable?.focus();
        });
      } else {
        document.body.style.overflow = '';
      }
    }
  },
  mounted() {
    if (this.isOpen) {
      document.body.style.overflow = 'hidden';
    }
  },
  beforeUnmount() {
    document.body.style.overflow = '';
  },
  computed: {
    containerClasses() {
      return [
        'app-modal',
        `app-modal--${this.size}`,
        this.isOpen && !this.animating && 'app-modal--open',
        this.animating && 'app-modal--animating'
      ].filter(Boolean).join(' ');
    },
    contentClasses() {
      return ['app-modal__content', this.animating && 'app-modal__content--animating'].filter(Boolean).join(' ');
    }
  },
  methods: {
    onOverlayClick(event) {
      if (event.target === event.currentTarget && this.closeOnOverlay) {
        this.close();
      }
    },
    onKeyDown(event) {
      if (event.key === 'Escape' && this.closeOnEscape) {
        this.close();
      }
      if (event.key === 'Tab') {
        this.trapFocus(event);
      }
    },
    close() {
      this.animating = true;
      setTimeout(() => {
        this.isOpen = false;
        this.animating = false;
        this.$emit('close');
      }, 200);
    },
    confirm() {
      this.$emit('confirm');
      this.close();
    },
    trapFocus(event) {
      const focusable = this.$refs.content?.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      if (!focusable?.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  }
};
</script>

<template>
  <Transition name="app-modal">
    <div
      v-show="isOpen"
      :class="containerClasses"
      class="app-modal__overlay"
      @click="onOverlayClick"
      @keydown="onKeyDown"
      role="dialog"
      aria-modal="true"
      :aria-labelledby="title ? 'modal-title' : undefined"
    >
      <div ref="content" :class="contentClasses" class="app-modal__content">
        <div class="app-modal__header">
          <h2 v-if="title" id="modal-title" class="app-modal__title">{{ title }}</h2>
          <button
            v-if="showClose"
            type="button"
            class="app-modal__close"
            @click="close"
            aria-label="Close"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6L6 18M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <div class="app-modal__body">
          <slot />
        </div>
        <div v-if="!hideFooter" class="app-modal__footer">
          <slot name="footer">
            <AppButton variant="ghost" @click="close">Cancel</AppButton>
            <AppButton variant="primary" @click="confirm">Confirm</AppButton>
          </slot>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.app-modal {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal, 500);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4, 16px);
  overflow: auto;
}

.app-modal__overlay {
  background: rgba(11, 18, 32, 0.5);
  backdrop-filter: blur(4px);
  animation: app-modal-fade-in 0.2s ease;
}

@keyframes app-modal-fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.app-modal__content {
  background: var(--color-bg-white);
  border-radius: var(--radius-xl, 24px);
  box-shadow: var(--shadow-xl);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  animation: app-modal-slide-up 0.2s ease;
  width: 100%;
}

@keyframes app-modal-slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.app-modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-5, 20px) var(--space-6, 24px);
  border-bottom: 1px solid var(--color-border-default);
}

.app-modal__title {
  font-size: var(--font-size-lg, 18px);
  font-weight: var(--font-weight-bold, 700);
  color: var(--color-text-primary);
  margin: 0;
}

.app-modal__close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md, 12px);
  color: var(--color-text-muted);
  transition: color var(--transition-fast), background var(--transition-fast);
  flex-shrink: 0;
}

.app-modal__close:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-muted);
}

.app-modal__body {
  padding: var(--space-6, 24px);
  overflow-y: auto;
  flex: 1;
}

.app-modal__footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-3, 12px);
  padding: var(--space-4, 16px) var(--space-6, 24px);
  border-top: 1px solid var(--color-border-default);
}

.app-modal--sm .app-modal__content { max-width: 400px; }
.app-modal--md .app-modal__content { max-width: 520px; }
.app-modal--lg .app-modal__content { max-width: 720px; }
.app-modal--xl .app-modal__content { max-width: 960px; }
.app-modal--full .app-modal__content { max-width: 100%; max-height: 100vh; border-radius: 0; }
</style>