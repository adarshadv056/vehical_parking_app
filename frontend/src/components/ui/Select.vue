<script>
export default {
  name: 'AppSelect',
  inheritAttrs: false,
  props: {
    modelValue: [String, Number],
    options: {
      type: Array,
      default: () => [],
      // [{ label, value, disabled }]
    },
    placeholder: String,
    disabled: Boolean,
    required: Boolean,
    error: String,
    hint: String,
    label: String,
    clearable: Boolean,
    searchable: Boolean,
    multiple: Boolean
  },
  emits: ['update:modelValue', 'change', 'blur', 'focus', 'search'],
  data() {
    return {
      open: false,
      searchQuery: '',
      focusedIndex: -1,
      focused: false
    };
  },
  computed: {
    isMultiple() {
      return this.multiple;
    },
    filteredOptions() {
      if (!this.searchable || !this.searchQuery) return this.options;
      const query = this.searchQuery.toLowerCase();
      return this.options.filter(opt =>
        opt.label.toLowerCase().includes(query) ||
        String(opt.value).toLowerCase().includes(query)
      );
    },
    selectedOption() {
      if (this.isMultiple) {
        return this.modelValue?.map(v => this.options.find(o => o.value === v)).filter(Boolean) || [];
      }
      return this.options.find(o => o.value === this.modelValue);
    },
    displayValue() {
      if (this.isMultiple) {
        if (!this.modelValue?.length) return this.placeholder || 'Select...';
        return this.selectedOption.map(o => o.label).join(', ');
      }
      return this.selectedOption?.label || this.placeholder || 'Select...';
    },
    hasValue() {
      if (this.isMultiple) return this.modelValue?.length > 0;
      return this.modelValue !== undefined && this.modelValue !== null && this.modelValue !== '';
    },
    containerClasses() {
      return [
        'app-select-wrapper',
        this.focused && 'app-select-wrapper--focused',
        this.open && 'app-select-wrapper--open',
        this.error && 'app-select-wrapper--error',
        this.disabled && 'app-select-wrapper--disabled',
        this.hasValue && 'app-select-wrapper--has-value'
      ].filter(Boolean).join(' ');
    },
    dropdownId() {
      return this.$attrs.id ? `${this.$attrs.id}-dropdown` : `select-${this._uid}-dropdown`;
    }
  },
  watch: {
    open(val) {
      if (val) {
        this.focusedIndex = this.options.findIndex(o => o.value === this.modelValue);
        this.$nextTick(() => {
          this.$refs.dropdown?.focus();
        });
      } else {
        this.searchQuery = '';
        this.focusedIndex = -1;
      }
    }
  },
  methods: {
    onToggle() {
      if (this.disabled) return;
      this.open = !this.open;
    },
    onClose() {
      this.open = false;
    },
    onSelect(option) {
      if (option.disabled) return;
      if (this.isMultiple) {
        const values = [...(this.modelValue || [])];
        const index = values.indexOf(option.value);
        if (index > -1) {
          values.splice(index, 1);
        } else {
          values.push(option.value);
        }
        this.$emit('update:modelValue', values);
      } else {
        this.$emit('update:modelValue', option.value);
        this.close();
      }
      this.$emit('change', this.isMultiple ? [...(this.modelValue || []), option.value] : option.value);
    },
    onClear(event) {
      event.stopPropagation();
      this.$emit('update:modelValue', this.isMultiple ? [] : null);
      this.$emit('change', this.isMultiple ? [] : null);
    },
    onKeydown(event) {
      if (!this.open) {
        if (event.key === 'Enter' || event.key === ' ' || event.key === 'ArrowDown') {
          event.preventDefault();
          this.open = true;
        }
        return;
      }
      switch (event.key) {
        case 'Escape':
          this.close();
          break;
        case 'ArrowDown':
          event.preventDefault();
          this.focusNext();
          break;
        case 'ArrowUp':
          event.preventDefault();
          this.focusPrev();
          break;
        case 'Enter':
        case ' ':
          event.preventDefault();
          if (this.focusedIndex >= 0) {
            this.onSelect(this.filteredOptions[this.focusedIndex]);
          }
          break;
        case 'Tab':
          this.close();
          break;
      }
    },
    onSearchInput(event) {
      this.searchQuery = event.target.value;
      this.$emit('search', event.target.value);
    },
    focusNext() {
      let next = this.focusedIndex + 1;
      while (next < this.filteredOptions.length && this.filteredOptions[next].disabled) {
        next++;
      }
      if (next < this.filteredOptions.length) this.focusedIndex = next;
    },
    focusPrev() {
      let prev = this.focusedIndex - 1;
      while (prev >= 0 && this.filteredOptions[prev].disabled) {
        prev--;
      }
      if (prev >= 0) this.focusedIndex = prev;
    },
    onBlur(event) {
      if (!event.relatedTarget || !event.relatedTarget.closest('.app-select__dropdown')) {
        setTimeout(() => this.close(), 100);
      }
    },
    onFocus() {
      this.focused = true;
    },
    onFocusOut() {
      this.focused = false;
    }
  }
};
</script>

<template>
  <div class="app-select-wrapper" :class="containerClasses" @click="onToggle" @keydown="onKeydown" tabindex="0" role="combobox" :aria-expanded="open" :aria-haspopup="listbox" :aria-controls="dropdownId" :aria-invalid="!!error" :aria-disabled="disabled" :aria-required="required" @focus="onFocus" @focusout="onFocusOut">
    <div class="app-select__trigger" ref="trigger">
      <span class="app-select__value" :class="{ 'app-select__value--placeholder': !hasValue }">
        {{ displayValue }}
      </span>
      <div class="app-select__actions">
        <button
          v-if="clearable && hasValue && !disabled"
          type="button"
          class="app-select__clear"
          @click.stop="onClear"
          aria-label="Clear selection"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
        <span class="app-select__caret" :class="{ 'app-select__caret--open': open }">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </span>
      </div>
    </div>

    <Transition name="app-select-dropdown">
      <div
        v-show="open"
        ref="dropdown"
        :id="dropdownId"
        class="app-select__dropdown"
        role="listbox"
        aria-label="Select options"
        tabindex="-1"
      >
        <div v-if="searchable" class="app-select__search">
          <input
            type="text"
            class="app-select__search-input"
            v-model="searchQuery"
            @input="onSearchInput"
            @click.stop
            :placeholder="placeholder || 'Search...'"
            aria-label="Search options"
            @keydown.esc="close"
          />
        </div>
        <div
          class="app-select__options"
          role="listbox"
          :aria-activedescendant="focusedIndex >= 0 ? `option-${focusedIndex}` : undefined"
        >
          <div
            v-for="(option, index) in filteredOptions"
            :key="option.value"
            :id="`option-${index}`"
            class="app-select__option"
            :class="{
              'app-select__option--selected': isSelected(option),
              'app-select__option--focused': focusedIndex === index,
              'app-select__option--disabled': option.disabled
            }"
            role="option"
            :aria-selected="isSelected(option)"
            :aria-disabled="option.disabled"
            @click="onSelect(option)"
            @mouseenter="focusedIndex = index"
          >
            <span v-if="isMultiple" class="app-select__checkbox">
              <input type="checkbox" :checked="isSelected(option)" disabled />
            </span>
            <span class="app-select__option-label">{{ option.label }}</span>
            <span v-if="option.disabled" class="app-select__option-disabled">Unavailable</span>
          </div>
          <div v-if="filteredOptions.length === 0" class="app-select__no-results">
            No options found
          </div>
        </div>
      </div>
    </Transition>

    <div v-if="error" class="app-select__message app-select__message--error" role="alert">
      {{ error }}
    </div>
    <div v-else-if="hint" class="app-select__message app-select__message--hint">
      {{ hint }}
    </div>
  </div>
</template>

<style scoped>
.app-select-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-1, 4px);
  width: 100%;
}

.app-select__trigger {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--color-bg-white);
  border: 1px solid var(--color-border-default);
  border-radius: var(--input-radius, 10px);
  padding: 0 var(--input-padding-x, 16px);
  height: var(--input-height, 44px);
  cursor: pointer;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.app-select-wrapper--focused .app-select__trigger {
  border-color: var(--color-brand-primary);
  box-shadow: var(--shadow-focus);
}

.app-select-wrapper--error .app-select__trigger {
  border-color: var(--color-status-occupied);
}

.app-select-wrapper--disabled .app-select__trigger {
  background: var(--color-bg-muted);
  border-color: var(--color-border-default);
  opacity: 0.6;
  cursor: not-allowed;
}

.app-select__value {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--color-text-primary);
}

.app-select__value--placeholder {
  color: var(--color-text-muted);
}

.app-select__actions {
  display: flex;
  align-items: center;
  gap: var(--space-1, 4px);
}

.app-select__clear {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm, 8px);
  color: var(--color-text-muted);
  transition: color var(--transition-fast), background var(--transition-fast);
}

.app-select__clear:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-muted);
}

.app-select__caret {
  color: var(--color-text-muted);
  transition: transform var(--transition-fast);
}

.app-select__caret--open {
  transform: rotate(180deg);
}

.app-select-wrapper--open .app-select__trigger {
  border-radius: var(--input-radius, 10px) var(--input-radius, 10px) 0 0;
  border-bottom-color: transparent;
}

.app-select__dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: var(--z-dropdown, 100);
  background: var(--color-bg-white);
  border: 1px solid var(--color-border-default);
  border-top: none;
  border-radius: 0 0 var(--radius-lg, 16px) var(--radius-lg, 16px);
  box-shadow: var(--shadow-xl);
  max-height: 280px;
  overflow: hidden;
  animation: app-select-dropdown-in 0.15s ease;
}

@keyframes app-select-dropdown-in {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.app-select__search {
  padding: var(--space-2, 8px);
  border-bottom: 1px solid var(--color-border-default);
}

.app-select__search-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: var(--space-2, 8px) var(--space-3, 12px);
  border-radius: var(--radius-sm, 8px);
  font-size: var(--font-size-sm, 14px);
  color: var(--color-text-primary);
  outline: none;
}

.app-select__search-input::placeholder {
  color: var(--color-text-muted);
}

.app-select__options {
  max-height: 240px;
  overflow-y: auto;
}

.app-select__option {
  display: flex;
  align-items: center;
  gap: var(--space-3, 12px);
  padding: var(--space-3, 12px) var(--space-4, 16px);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.app-select__option:hover:not(.app-select__option--disabled) {
  background: var(--color-bg-muted);
}

.app-select__option--focused {
  background: var(--color-brand-primary-light);
}

.app-select__option--selected {
  color: var(--color-brand-primary);
}

.app-select__option--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.app-select__option-label {
  flex: 1;
  font-size: var(--font-size-sm, 14px);
  color: var(--color-text-primary);
}

.app-select__option-disabled {
  font-size: var(--font-size-xs, 11px);
  color: var(--color-text-muted);
  text-transform: uppercase;
}

.app-select__no-results {
  padding: var(--space-4, 16px);
  text-align: center;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm, 14px);
}

.app-select__message {
  font-size: var(--font-size-xs, 12px);
  margin-top: var(--space-1, 4px);
}

.app-select__message--error {
  color: var(--color-status-occupied);
}

.app-select__message--hint {
  color: var(--color-text-muted);
}

/* Dropdown animation */
.app-select-dropdown-enter-active,
.app-select-dropdown-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.app-select-dropdown-enter-from,
.app-select-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Responsive */
@media (max-width: 640px) {
  .app-select__dropdown {
    left: -16px;
    right: -16px;
  }
}
</style>