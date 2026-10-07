<template>
  <div class="kpi-card" :class="`kpi-card--${variant}`">
    <div class="kpi-card__inner">
      <div class="kpi-card__content">
        <span class="kpi-card__label">{{ label }}</span>
        <div class="kpi-card__val-row">
          <span v-if="prefix" class="kpi-card__prefix">{{ prefix }}</span>
          <span class="kpi-card__val">{{ formattedValue }}</span>
          <span v-if="suffix" class="kpi-card__suffix">{{ suffix }}</span>
        </div>
        <p v-if="subtext" class="kpi-card__sub">{{ subtext }}</p>
      </div>

      <div v-if="resolvedIcon" class="kpi-card__icon-box">
        <component :is="resolvedIcon" class="kpi-card__icon" />
      </div>
    </div>
  </div>
</template>

<script>
import * as Icons from '@/components/icons';

export default {
  name: 'KpiCard',
  props: {
    label: { type: String, required: true },
    value: { type: [Number, String], required: true },
    prefix: { type: String, default: '' },
    suffix: { type: String, default: '' },
    subtext: { type: String, default: '' },
    icon: { type: [String, Object], default: null },
    variant: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'primary', 'success', 'warning', 'dark'].includes(v)
    }
  },
  computed: {
    formattedValue() {
      if (typeof this.value === 'number') {
        return this.value.toLocaleString('en-IN');
      }
      return this.value;
    },
    resolvedIcon() {
      if (!this.icon) return null;
      if (typeof this.icon === 'object') return this.icon;
      return Icons[this.icon] || this.icon;
    }
  }
};
</script>

<style scoped>
.kpi-card {
  background: var(--color-bg-card, #FFFFFF);
  border: 1px solid var(--color-border-default, #E5E7EB);
  border-radius: var(--radius-lg, 16px);
  padding: var(--space-5, 20px);
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md, 0 4px 12px rgba(15, 23, 42, 0.08));
}

.kpi-card__inner {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4, 16px);
}

.kpi-card__content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.kpi-card__label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-secondary, #64748B);
}

.kpi-card__val-row {
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.kpi-card__prefix {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.kpi-card__val {
  font-size: 30px;
  font-weight: 800;
  color: var(--color-text-primary, #111827);
  line-height: 1.1;
  font-feature-settings: 'tnum';
}

.kpi-card__suffix {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-secondary, #64748B);
  margin-left: 2px;
}

.kpi-card__sub {
  margin: 4px 0 0;
  font-size: 12px;
  color: var(--color-text-muted, #94A3B8);
}

.kpi-card__icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md, 12px);
  background: var(--color-brand-primary-light, #EAF2FF);
  color: var(--color-brand-primary, #2563EB);
  flex-shrink: 0;
}

.kpi-card__icon,
.kpi-card__icon-box :deep(svg) {
  width: 22px;
  height: 22px;
  display: block;
}

/* Variants */
.kpi-card--primary .kpi-card__icon-box {
  background: var(--color-brand-primary-light, #EAF2FF);
  color: var(--color-brand-primary, #2563EB);
}

.kpi-card--success .kpi-card__icon-box {
  background: var(--color-status-available-bg, #DCFCE7);
  color: var(--color-status-available, #16A34A);
}

.kpi-card--warning .kpi-card__icon-box {
  background: var(--color-status-warning-bg, #FEF3C7);
  color: var(--color-status-warning, #F59E0B);
}

.kpi-card--dark {
  background: var(--color-navy-deep, #0B1220);
  border-color: rgba(255, 255, 255, 0.1);
  color: #FFFFFF;
}

.kpi-card--dark .kpi-card__label { color: #94A3B8; }
.kpi-card--dark .kpi-card__val { color: #FFFFFF; }
.kpi-card--dark .kpi-card__prefix { color: #FFFFFF; }
.kpi-card--dark .kpi-card__sub { color: #CBD5E1; }
.kpi-card--dark .kpi-card__icon-box {
  background: rgba(37, 99, 235, 0.3);
  color: #93C5FD;
}
</style>
