<template>
  <div class="lot-card" :class="{ 'lot-card--full': isFull }">
    <!-- Image Header with Badges -->
    <div class="lot-card__media">
      <img
        :src="imageUrl"
        :alt="lot.name"
        class="lot-card__img"
        loading="lazy"
      />
      <div class="lot-card__scrim" />
      
      <div class="lot-card__badges">
        <span class="lot-card__badge" :class="isFull ? 'lot-card__badge--full' : 'lot-card__badge--avail'">
          <span class="lot-card__badge-dot" />
          {{ isFull ? 'Full' : `${availableSpots} Free` }}
        </span>
        <span class="lot-card__badge lot-card__badge--photos">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
            <circle cx="12" cy="13" r="4"/>
          </svg>
          {{ photoCount }}
        </span>
      </div>

      <div class="lot-card__price-tag">
        <span class="lot-card__price-val">₹{{ Number(lot.price).toFixed(0) }}</span>
        <span class="lot-card__price-unit">/hr</span>
      </div>
    </div>

    <!-- Card Content -->
    <div class="lot-card__body">
      <div class="lot-card__title-row">
        <h3 class="lot-card__name">{{ lot.name }}</h3>
      </div>

      <p class="lot-card__location">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
          <circle cx="12" cy="10" r="3" />
        </svg>
        <span>{{ lot.location }}</span>
        <span v-if="lot.pincode" class="lot-card__pin">{{ lot.pincode }}</span>
      </p>

      <!-- Facility Tags (Reference 5 & DESIGN_SYSTEM.md) -->
      <div class="lot-card__amenities">
        <span class="amenity-chip">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
          </svg>
          CCTV 24/7
        </span>
        <span class="amenity-chip">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
          </svg>
          EV Ready
        </span>
        <span class="amenity-chip">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.4-1.7-1.1-2.2l-2.4-1.8H5.5L3.1 10.8C2.4 11.3 2 12.1 2 13v3c0 .6.4 1 1 1h2" />
            <circle cx="7" cy="17" r="2" />
            <path d="M9 17h6" />
            <circle cx="17" cy="17" r="2" />
          </svg>
          Covered
        </span>
      </div>

      <!-- Capacity Progress Bar -->
      <div class="lot-card__capacity">
        <div class="lot-card__cap-head">
          <span class="lot-card__cap-label">Occupancy</span>
          <span class="lot-card__cap-stat">{{ occupiedSpots }} / {{ totalSpots }} bays</span>
        </div>
        <div class="lot-card__progress-track">
          <div
            class="lot-card__progress-fill"
            :class="progressColorClass"
            :style="{ width: `${occupancyPercent}%` }"
          />
        </div>
      </div>

      <!-- Action Footer -->
      <div class="lot-card__footer">
        <slot name="actions">
          <button
            type="button"
            class="lot-card__action-btn"
            :disabled="isFull"
            @click="$emit('book', lot)"
          >
            <span v-if="!isFull">Reserve Bay</span>
            <span v-else>Lot Full</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12" />
              <polyline points="12 5 19 12 12 19" />
            </svg>
          </button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
const LOT_IMAGES = [
  'https://images.unsplash.com/photo-1506521781263-d8422e82f27a?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1562619371-b67725b6fde2?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1573348722427-f1d6819fdf98?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'
];

export default {
  name: 'ParkingLotCard',
  props: {
    lot: {
      type: Object,
      required: true
    }
  },
  emits: ['book'],
  computed: {
    imageUrl() {
      const idx = (Number(this.lot.id) || 1) % LOT_IMAGES.length;
      return LOT_IMAGES[idx];
    },
    photoCount() {
      return 12 + (((this.lot.id || 1) * 3) % 15);
    },
    totalSpots() {
      return this.lot.capacity || this.lot.total_spots || 0;
    },
    occupiedSpots() {
      return this.lot.occupied_spots ?? 0;
    },
    availableSpots() {
      if (typeof this.lot.available_spots !== 'undefined') return this.lot.available_spots;
      return Math.max(0, this.totalSpots - this.occupiedSpots);
    },
    isFull() {
      return this.availableSpots <= 0;
    },
    occupancyPercent() {
      if (!this.totalSpots) return 0;
      return Math.min(100, Math.round((this.occupiedSpots / this.totalSpots) * 100));
    },
    progressColorClass() {
      if (this.occupancyPercent >= 90) return 'lot-card__progress-fill--danger';
      if (this.occupancyPercent >= 70) return 'lot-card__progress-fill--warning';
      return 'lot-card__progress-fill--success';
    }
  }
};
</script>

<style scoped>
.lot-card {
  display: flex;
  flex-direction: column;
  background: var(--color-bg-card, #FFFFFF);
  border: 1px solid var(--color-border-default, #E5E7EB);
  border-radius: var(--radius-lg, 16px);
  overflow: hidden;
  transition: transform var(--transition-normal, 0.2s ease), box-shadow var(--transition-normal, 0.2s ease), border-color var(--transition-normal, 0.2s ease);
}

.lot-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg, 0 12px 24px rgba(15, 23, 42, 0.08));
  border-color: var(--color-border-strong, #CBD5E1);
}

/* Media Header */
.lot-card__media {
  position: relative;
  width: 100%;
  height: 170px;
  background: var(--color-navy-deep, #0B1220);
  overflow: hidden;
}

.lot-card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.lot-card:hover .lot-card__img {
  transform: scale(1.04);
}

.lot-card__scrim {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(11, 18, 32, 0.2) 0%, rgba(11, 18, 32, 0.7) 100%);
}

.lot-card__badges {
  position: absolute;
  top: 12px;
  left: 12px;
  right: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 2;
}

.lot-card__badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border-radius: var(--radius-pill, 9999px);
  font-size: 11px;
  font-weight: 700;
  backdrop-filter: blur(8px);
}

.lot-card__badge--avail {
  background: rgba(22, 163, 74, 0.9);
  color: #FFFFFF;
}

.lot-card__badge--full {
  background: rgba(239, 68, 68, 0.9);
  color: #FFFFFF;
}

.lot-card__badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #FFFFFF;
}

.lot-card__badge--photos {
  background: rgba(11, 18, 32, 0.65);
  color: #F8FAFC;
  font-weight: 600;
}

.lot-card__price-tag {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  padding: 4px 10px;
  border-radius: var(--radius-md, 10px);
  color: var(--color-navy-deep, #0B1220);
  display: flex;
  align-items: baseline;
  gap: 2px;
  box-shadow: var(--shadow-sm);
  z-index: 2;
}

.lot-card__price-val {
  font-size: 16px;
  font-weight: 800;
  color: var(--color-brand-primary, #2563EB);
}

.lot-card__price-unit {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-secondary, #64748B);
}

/* Card Body */
.lot-card__body {
  padding: var(--space-4, 16px);
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.lot-card__title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.lot-card__name {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
  line-height: 1.3;
}

.lot-card__location {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: var(--color-text-secondary, #64748B);
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.lot-card__location svg {
  flex-shrink: 0;
  color: var(--color-brand-primary, #2563EB);
}

.lot-card__pin {
  margin-left: 4px;
  padding: 1px 6px;
  border-radius: 4px;
  background: var(--color-bg-muted, #F8FAFC);
  font-size: 10px;
  font-weight: 600;
  color: var(--color-text-muted, #94A3B8);
}

/* Amenities */
.lot-card__amenities {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 2px;
}

.amenity-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  background: var(--color-bg-muted, #F8FAFC);
  border: 1px solid var(--color-border-default, #E5E7EB);
  border-radius: 6px;
  font-size: 11px;
  font-weight: 500;
  color: var(--color-text-secondary, #64748B);
}

.amenity-chip svg {
  color: var(--color-text-muted, #94A3B8);
}

/* Capacity Progress */
.lot-card__capacity {
  margin-top: 4px;
}

.lot-card__cap-head {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  margin-bottom: 5px;
}

.lot-card__cap-label {
  color: var(--color-text-muted, #94A3B8);
  font-weight: 500;
}

.lot-card__cap-stat {
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.lot-card__progress-track {
  width: 100%;
  height: 6px;
  background: var(--color-bg-muted, #F1F5F9);
  border-radius: var(--radius-pill, 9999px);
  overflow: hidden;
}

.lot-card__progress-fill {
  height: 100%;
  border-radius: var(--radius-pill, 9999px);
  transition: width 0.4s ease;
}

.lot-card__progress-fill--success {
  background: var(--color-status-available, #16A34A);
}

.lot-card__progress-fill--warning {
  background: var(--color-status-warning, #F59E0B);
}

.lot-card__progress-fill--danger {
  background: var(--color-status-occupied, #EF4444);
}

/* Footer / Actions */
.lot-card__footer {
  margin-top: auto;
  padding-top: 10px;
  border-top: 1px solid var(--color-border-default, #E5E7EB);
}

.lot-card__action-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--color-brand-primary, #2563EB);
  color: #FFFFFF;
  border: none;
  border-radius: var(--radius-md, 12px);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: background var(--transition-fast, 0.15s ease), transform var(--transition-fast, 0.15s ease);
}

.lot-card__action-btn:hover:not(:disabled) {
  background: var(--color-brand-primary-hover, #1D4ED8);
  transform: translateY(-1px);
}

.lot-card__action-btn:disabled {
  background: var(--color-bg-muted, #E2E8F0);
  color: var(--color-text-muted, #94A3B8);
  cursor: not-allowed;
}
</style>
