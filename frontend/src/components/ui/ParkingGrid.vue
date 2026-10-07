<template>
  <div class="parking-grid-wrap">
    <div class="parking-grid-head">
      <div class="parking-grid-legend">
        <span class="legend-item">
          <span class="legend-box legend-box--avail" /> Available
        </span>
        <span class="legend-item">
          <span class="legend-box legend-box--occ" /> Occupied
        </span>
      </div>
      <span class="parking-grid-count">
        {{ availableCount }} of {{ spots.length }} free
      </span>
    </div>

    <div class="parking-grid">
      <div
        v-for="(spot, index) in spots"
        :key="spot.id || index"
        class="stall"
        :class="{
          'stall--occupied': spot.is_occupied,
          'stall--available': !spot.is_occupied,
          'stall--interactive': interactive
        }"
        @click="onSpotClick(spot, index)"
      >
        <div class="stall__divider stall__divider--left" />
        <div class="stall__bay-content">
          <span class="stall__num">P-{{ String(index + 1).padStart(2, '0') }}</span>
          
          <div v-if="spot.is_occupied" class="stall__car" title="Occupied Bay">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.4-1.7-1.1-2.2l-2.4-1.8H5.5L3.1 10.8C2.4 11.3 2 12.1 2 13v3c0 .6.4 1 1 1h2" />
              <circle cx="7" cy="17" r="2" />
              <path d="M9 17h6" />
              <circle cx="17" cy="17" r="2" />
            </svg>
          </div>
          <div v-else class="stall__free-indicator">
            <span class="stall__free-dot" />
          </div>
        </div>
        <div class="stall__divider stall__divider--right" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ParkingGrid',
  props: {
    spots: {
      type: Array,
      default: () => []
    },
    interactive: {
      type: Boolean,
      default: true
    }
  },
  emits: ['spot-click'],
  computed: {
    availableCount() {
      return this.spots.filter(s => !s.is_occupied).length;
    }
  },
  methods: {
    onSpotClick(spot, index) {
      if (this.interactive) {
        this.$emit('spot-click', { spot, index });
      }
    }
  }
};
</script>

<style scoped>
.parking-grid-wrap {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.parking-grid-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
}

.parking-grid-legend {
  display: flex;
  align-items: center;
  gap: 14px;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--color-text-secondary, #64748B);
  font-weight: 500;
}

.legend-box {
  width: 10px;
  height: 10px;
  border-radius: 2px;
}

.legend-box--avail {
  background: var(--color-status-available-bg, #DCFCE7);
  border: 1px solid var(--color-status-available, #16A34A);
}

.legend-box--occ {
  background: var(--color-status-occupied-bg, #FEE2E2);
  border: 1px solid var(--color-status-occupied, #EF4444);
}

.parking-grid-count {
  font-weight: 700;
  color: var(--color-brand-primary, #2563EB);
}

.parking-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(54px, 1fr));
  gap: 8px;
  background: var(--color-bg-muted, #F8FAFC);
  padding: 12px;
  border-radius: var(--radius-md, 12px);
  border: 1px solid var(--color-border-default, #E5E7EB);
}

/* Individual Parking Bay */
.stall {
  position: relative;
  height: 64px;
  background: var(--color-bg-white, #FFFFFF);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed var(--color-border-strong, #CBD5E1);
  transition: all var(--transition-fast, 0.15s ease);
}

.stall--interactive {
  cursor: pointer;
}

.stall--available:hover {
  border-color: var(--color-brand-primary, #2563EB);
  background: var(--color-brand-primary-light, #EAF2FF);
  transform: translateY(-2px);
}

.stall--occupied {
  background: var(--color-status-occupied-bg, #FEE2E2);
  border-color: var(--color-status-occupied, #EF4444);
  border-style: solid;
}

.stall__bay-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}

.stall__num {
  font-size: 10px;
  font-weight: 800;
  font-family: var(--font-family-mono, monospace);
  color: var(--color-text-secondary, #64748B);
}

.stall--occupied .stall__num {
  color: var(--color-status-occupied, #DC2626);
}

.stall__car {
  width: 22px;
  height: 22px;
  color: var(--color-status-occupied, #DC2626);
}

.stall__car svg {
  width: 100%;
  height: 100%;
}

.stall__free-indicator {
  width: 14px;
  height: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stall__free-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-status-available, #16A34A);
}
</style>
