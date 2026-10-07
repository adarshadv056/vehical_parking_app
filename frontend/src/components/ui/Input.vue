<script>
export default {
  name: 'AppInput',
  inheritAttrs: false,
  props: {
    modelValue: [String, Number],
    label: String,
    placeholder: String,
    type: {
      type: String,
      default: 'text',
      validator: (v) => ['text', 'email', 'password', 'number', 'tel', 'url', 'search'].includes(v)
    },
    disabled: Boolean,
    readonly: Boolean,
    required: Boolean,
    error: String,
    hint: String,
    icon: String,
    iconRight: String,
    showPassword: Boolean,
    autocomplete: String
  },
  emits: ['update:modelValue', 'blur', 'focus', 'icon-click'],
  data() {
    return {
      showPasswordInternal: false,
      focused: false
    };
  },
  computed: {
    inputType() {
      if (this.type === 'password' && this.showPassword) {
        return this.showPasswordInternal ? 'text' : 'password';
      }
      return this.type;
    },
    containerClasses() {
      return [
        'app-input-wrapper',
        this.focused && 'app-input-wrapper--focused',
        this.error && 'app-input-wrapper--error',
        this.disabled && 'app-input-wrapper--disabled',
        this.required && 'app-input-wrapper--required'
      ].filter(Boolean).join(' ');
    },
    inputId() {
      return this.$attrs.id || `input-${this._uid}`;
    }
  },
  methods: {
    onInput(event) {
      this.$emit('update:modelValue', event.target.value);
    },
    onBlur(event) {
      this.focused = false;
      this.$emit('blur', event);
    },
    onFocus(event) {
      this.focused = true;
      this.$emit('focus', event);
    },
    togglePassword() {
      this.showPasswordInternal = !this.showPasswordInternal;
    },
    onIconClick(event) {
      this.$emit('icon-click', event);
    }
  }
};
</script>

<template>
  <div :class="containerClasses">
    <label v-if="label" :for="inputId" class="app-input__label">
      {{ label }}
      <span v-if="required" class="app-input__required" aria-hidden="true">*</span>
    </label>
    <div class="app-input__container">
      <span v-if="$slots.prefix || $attrs.icon" class="app-input__affix app-input__affix--prefix">
        <slot name="prefix" />
        <component v-if="$attrs.icon" :is="$attrs.icon" class="app-input__icon" />
      </span>
      <input
        :id="inputId"
        :type="inputType"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :aria-invalid="!!error"
        :aria-describedby="error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined"
        :autocomplete="autocomplete"
        class="app-input"
        @input="onInput"
        @blur="onBlur"
        @focus="onFocus"
        v-bind="$attrs"
      />
      <span v-if="$slots.suffix || iconRight || (type === 'password' && showPassword)" class="app-input__affix app-input__affix--suffix">
        <button
          v-if="type === 'password' && showPassword"
          type="button"
          class="app-input__toggle"
          @click="togglePassword"
          :aria-label="showPasswordInternal ? 'Hide password' : 'Show password'"
        >
          <component :is="showPasswordInternal ? 'EyeOffIcon' : 'EyeIcon'" class="app-input__icon" />
        </button>
        <button
          v-else-if="iconRight"
          type="button"
          class="app-input__icon-btn"
          @click="$emit('icon-click', $event)"
          :aria-label="iconRight"
        >
          <component :is="iconRight" class="app-input__icon" />
        </button>
        <slot name="suffix" />
      </span>
    </div>
    <div v-if="error" :id="`${inputId}-error`" class="app-input__message app-input__message--error" role="alert">
      {{ error }}
    </div>
    <div v-else-if="hint" :id="`${inputId}-hint`" class="app-input__message app-input__message--hint">
      {{ hint }}
    </div>
  </div>
</template>

<style scoped>
.app-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-1, 4px);
  width: 100%;
}

.app-input__label {
  font-size: var(--font-size-sm, 14px);
  font-weight: var(--font-weight-medium, 500);
  color: var(--color-text-primary);
}

.app-input__required {
  color: var(--color-status-occupied);
  margin-left: 2px;
}

.app-input__container {
  position: relative;
  display: flex;
  align-items: center;
  background: var(--color-bg-white);
  border: 1px solid var(--color-border-default);
  border-radius: var(--input-radius, 10px);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.app-input-wrapper--focused .app-input__container {
  border-color: var(--color-brand-primary);
  box-shadow: var(--shadow-focus);
}

.app-input-wrapper--error .app-input__container {
  border-color: var(--color-status-occupied);
}

.app-input-wrapper--error .app-input__container:focus-within {
  box-shadow: 0 0 0 3px var(--color-status-occupied-bg);
}

.app-input-wrapper--disabled .app-input__container {
  background: var(--color-bg-muted);
  border-color: var(--color-border-default);
  opacity: 0.6;
  cursor: not-allowed;
}

.app-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0 var(--input-padding-x, 16px);
  height: var(--input-height, 44px);
  font-family: inherit;
  font-size: var(--font-size-base, 16px);
  color: var(--color-text-primary);
  outline: none;
  min-width: 0;
}

.app-input::placeholder {
  color: var(--color-text-muted);
}

.app-input:disabled {
  color: var(--color-text-muted);
  cursor: not-allowed;
}

.app-input__affix {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 var(--space-3, 12px);
  color: var(--color-text-muted);
}

.app-input__affix--prefix {
  border-right: 1px solid var(--color-border-default);
}

.app-input__affix--suffix {
  border-left: 1px solid var(--color-border-default);
}

.app-input__icon {
  width: 20px;
  height: 20px;
  color: currentColor;
  flex-shrink: 0;
}

.app-input__toggle,
.app-input__icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-1, 4px);
  border-radius: var(--radius-sm, 8px);
  color: var(--color-text-muted);
  transition: color var(--transition-fast), background var(--transition-fast);
}

.app-input__toggle:hover,
.app-input__icon-btn:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-muted);
}

.app-input__icon {
  width: 20px;
  height: 20px;
}

.app-input__message {
  font-size: var(--font-size-xs, 12px);
  display: flex;
  align-items: center;
  gap: var(--space-1, 4px);
}

.app-input__message--error {
  color: var(--color-status-occupied);
}

.app-input__message--hint {
  color: var(--color-text-muted);
}
</style>