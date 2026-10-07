<template>
  <div class="active-session">
    <div class="active-session__glow" />
    <div class="active-session__inner">
      <!-- Header -->
      <div class="active-session__header">
        <div class="active-session__status">
          <span class="active-session__pulse-dot" />
          <span class="active-session__status-text">Active Parking Session</span>
        </div>
        <span class="active-session__live-tag">In Progress</span>
      </div>

      <!-- Main Info Row -->
      <div class="active-session__grid">
        <!-- Facility Info -->
        <div class="active-session__col">
          <span class="active-session__label">Facility</span>
          <h3 class="active-session__title">{{ session.lot_name || 'Parking Facility' }}</h3>
          <p class="active-session__meta">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
            {{ session.location || 'Location details' }}
          </p>
        </div>

        <!-- Vehicle & Bay -->
        <div class="active-session__col">
          <span class="active-session__label">Vehicle &amp; Stall</span>
          <div class="active-session__plate-wrap">
            <div class="license-plate">
              <span class="license-plate__country">IND</span>
              <span class="license-plate__num">{{ session.vehicle_number }}</span>
            </div>
            <span class="active-session__bay-badge">Bay #{{ session.spot_id }}</span>
          </div>
        </div>

        <!-- Live Timer & Fee -->
        <div class="active-session__col active-session__col--stats">
          <div class="active-session__stat-item">
            <span class="active-session__label">Elapsed Time</span>
            <div class="active-session__timer">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
              <span>{{ elapsedFormatted }}</span>
            </div>
          </div>

          <div class="active-session__stat-item">
            <span class="active-session__label">Current Accrual</span>
            <div class="active-session__amount">
              ₹{{ Number(calculatedCost).toFixed(0) }}
              <span class="active-session__rate">(₹{{ session.hourly_rate || 40 }}/hr)</span>
            </div>
          </div>
        </div>

        <!-- Action -->
        <div class="active-session__col active-session__col--action">
          <button
            type="button"
            class="active-session__checkout-btn"
            :disabled="loading"
            @click="$emit('park-out', session.id)"
          >
            <span v-if="loading" class="spinner" />
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            <span>Park Out &amp; Pay</span>
          </button>
          <span class="active-session__action-hint">Instant digital checkout</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActiveSessionCard',
  props: {
    session: {
      type: Object,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['park-out'],
  data() {
    return {
      now: new Date(),
      timerId: null
    };
  },
  mounted() {
    this.timerId = setInterval(() => {
      this.now = new Date();
    }, 1000);
  },
  beforeUnmount() {
    if (this.timerId) clearInterval(this.timerId);
  },
  computed: {
    startDate() {
      return this.session.parking_time ? new Date(this.session.parking_time) : new Date();
    },
    elapsedSeconds() {
      const diffMs = Math.max(0, this.now.getTime() - this.startDate.getTime());
      return Math.floor(diffMs / 1000);
    },
    elapsedFormatted() {
      const h = Math.floor(this.elapsedSeconds / 3600);
      const m = Math.floor((this.elapsedSeconds % 3600) / 60);
      const s = this.elapsedSeconds % 60;
      return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    },
    calculatedCost() {
      const hours = Math.ceil(Math.max(1, this.elapsedSeconds / 3600));
      const rate = this.session.hourly_rate || this.session.parking_cost || 40;
      return hours * rate;
    }
  }
};
</script>

<style scoped>
.active-session {
  position: relative;
  background: var(--color-navy-deep, #0B1220);
  border-radius: var(--radius-xl, 20px);
  color: #FFFFFF;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(11, 18, 32, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.active-session__glow {
  position: absolute;
  top: -60px;
  right: -60px;
  width: 220px;
  height: 220px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.4) 0%, rgba(37, 99, 235, 0) 70%);
  pointer-events: none;
}

.active-session__inner {
  position: relative;
  padding: var(--space-6, 24px);
  z-index: 1;
}

.active-session__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-5, 20px);
  padding-bottom: var(--space-3, 12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.active-session__status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.active-session__pulse-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--color-status-available, #16A34A);
  box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7);
  animation: pulse 1.8s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7); }
  70% { box-shadow: 0 0 0 8px rgba(22, 163, 74, 0); }
  100% { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0); }
}

.active-session__status-text {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #DCFCE7;
}

.active-session__live-tag {
  padding: 3px 10px;
  border-radius: var(--radius-pill, 9999px);
  background: rgba(37, 99, 235, 0.3);
  border: 1px solid rgba(37, 99, 235, 0.5);
  font-size: 11px;
  font-weight: 700;
  color: #93C5FD;
}

.active-session__grid {
  display: grid;
  grid-template-columns: 1.4fr 1.2fr 1.4fr 1.2fr;
  gap: var(--space-5, 20px);
  align-items: center;
}

.active-session__col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.active-session__label {
  font-size: 11px;
  font-weight: 600;
  color: #94A3B8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.active-session__title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #FFFFFF;
}

.active-session__meta {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #CBD5E1;
}

.active-session__meta svg {
  color: #60A5FA;
  flex-shrink: 0;
}

.active-session__plate-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 4px;
}

/* Authentic License Plate */
.license-plate {
  display: inline-flex;
  align-items: center;
  background: #F8FAFC;
  color: #0F172A;
  border: 2px solid #334155;
  border-radius: 6px;
  padding: 3px 8px;
  font-family: var(--font-family-mono, monospace);
  font-weight: 800;
  font-size: 13px;
  letter-spacing: 0.08em;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.license-plate__country {
  background: #2563EB;
  color: #FFFFFF;
  padding: 1px 4px;
  border-radius: 3px;
  font-size: 9px;
  margin-right: 6px;
  font-weight: 900;
}

.active-session__bay-badge {
  padding: 4px 10px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 12px;
  font-weight: 700;
  color: #E2E8F0;
}

.active-session__col--stats {
  display: flex;
  flex-direction: row;
  gap: 20px;
}

.active-session__stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.active-session__timer {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-family-mono, monospace);
  font-size: 18px;
  font-weight: 700;
  color: #67E8F9;
}

.active-session__timer svg {
  color: #22D3EE;
}

.active-session__amount {
  font-size: 18px;
  font-weight: 800;
  color: #4ADE80;
}

.active-session__rate {
  font-size: 11px;
  font-weight: 500;
  color: #94A3B8;
  margin-left: 2px;
}

.active-session__col--action {
  align-items: flex-end;
}

.active-session__checkout-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  background: #DC2626;
  color: #FFFFFF;
  border: none;
  border-radius: var(--radius-md, 12px);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background var(--transition-fast), transform var(--transition-fast);
  box-shadow: 0 4px 14px rgba(220, 38, 38, 0.35);
  width: 100%;
}

.active-session__checkout-btn:hover:not(:disabled) {
  background: #B91C1C;
  transform: translateY(-1px);
}

.active-session__checkout-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.active-session__action-hint {
  font-size: 11px;
  color: #94A3B8;
  margin-top: 4px;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #FFFFFF;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 1024px) {
  .active-session__grid {
    grid-template-columns: 1fr 1fr;
  }
  .active-session__col--action {
    grid-column: 1 / -1;
    align-items: stretch;
  }
}

@media (max-width: 640px) {
  .active-session__grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .active-session__col--stats {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
