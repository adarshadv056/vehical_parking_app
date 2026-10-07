<script>
import { userApi, auth } from '@/api/client';
import { AppPageHeader, AppButton } from '@/components/ui';

const GARAGE_IMAGES = [
  'https://images.unsplash.com/photo-1506521781263-d8422e82f27a?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1562619371-b67725b6fde2?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1573348722427-f1d6819fdf98?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'
];

export default {
  name: 'BookSpot',
  components: { AppPageHeader, AppButton },
  data() {
    return {
      formData: {
        lotId: null,
        spotId: null,
        userId: null,
        vehicleNo: 'NY 482-EVX'
      },
      lotDetails: {
        name: 'City Center Garage',
        location: '120 Broadway, Lower Manhattan, New York',
        price: 40.0
      },
      quickPlates: ['NY 482-EVX', 'CA 883-TES', 'MH 12 AB 4410', 'DL 01 CX 9021'],
      message: '',
      loading: false,
      fetchingSpot: true
    };
  },
  computed: {
    garageImage() {
      const idx = (Number(this.formData.lotId) || 1) % GARAGE_IMAGES.length;
      return GARAGE_IMAGES[idx];
    },
    currentTimeFormatted() {
      return new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
    }
  },
  mounted() {
    document.title = 'Reserve Bay — ParkSync';
    const q = this.$route.query;
    this.formData.lotId = q.lotId || 1;
    if (q.name) this.lotDetails.name = q.name;
    if (q.location) this.lotDetails.location = q.location;
    if (q.price) this.lotDetails.price = Number(q.price);

    this.fetchUserInfo();
    this.fetchAvailableSpot();
  },
  methods: {
    goBack() {
      this.$router.push('/user');
    },
    async fetchUserInfo() {
      const payload = auth.getPayload();
      this.formData.userId = payload?.sub || payload?.user_id || payload?.id;
    },
    async fetchAvailableSpot() {
      try {
        this.fetchingSpot = true;
        const { data, error } = await userApi.getFirstSpot(this.formData.lotId);
        if (error) throw new Error(error.message);
        this.formData.spotId = data.parking_spot.id;
      } catch (error) {
        console.error('Error fetching spot details:', error);
        this.message = 'No bays currently available in this facility. Please select another garage.';
      } finally {
        this.fetchingSpot = false;
      }
    },
    setPlate(p) {
      this.formData.vehicleNo = p;
    },
    async bookParkingSpot() {
      if (!this.formData.spotId) {
        this.message = 'No spot allocated. Please try again.';
        return;
      }
      if (!this.formData.vehicleNo.trim()) {
        this.message = 'Please provide a valid vehicle number plate.';
        return;
      }

      try {
        this.loading = true;
        const { data, error } = await userApi.bookSpot(this.formData.spotId, this.formData.vehicleNo.trim());
        if (error) {
          this.message = error.message;
          return;
        }
        localStorage.setItem('message', data?.message || 'Parking spot reserved successfully!');
        this.$router.push('/user');
      } catch (error) {
        console.error('Error booking parking spot:', error);
        this.message = 'Unable to complete reservation. Spot may have just been occupied.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<template>
  <div class="book-page">
    <AppPageHeader
      title="Reserve Parking Bay"
      subtitle="Confirm your vehicle registration to issue your digital entry ticket"
      :backRoute="{ name: 'UserDashboard' }"
    />

    <div class="book-page__container">
      <!-- Error Alert -->
      <div v-if="message" class="book-page__alert" role="alert">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <span>{{ message }}</span>
      </div>

      <!-- Mobility Ticket Card (Reference 1) -->
      <div class="ticket-card">
        <!-- Top Media Header -->
        <div class="ticket-card__header">
          <img :src="garageImage" alt="Parking facility" class="ticket-card__img" />
          <div class="ticket-card__scrim" />
          <div class="ticket-card__header-content">
            <span class="ticket-card__badge">24/7 Monitored Access</span>
            <h2 class="ticket-card__lot-name">{{ lotDetails.name }}</h2>
            <p class="ticket-card__lot-loc">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
                <circle cx="12" cy="10" r="3" />
              </svg>
              {{ lotDetails.location }}
            </p>
          </div>
        </div>

        <!-- Ticket Body -->
        <div class="ticket-card__body">
          <!-- Reservation Schedule Row -->
          <div class="ticket-card__schedule">
            <div class="sched-box">
              <span class="sched-box__label">Check-in</span>
              <span class="sched-box__time">Today, {{ currentTimeFormatted }}</span>
              <span class="sched-box__hint">Immediate access</span>
            </div>
            <div class="sched-arrow">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </div>
            <div class="sched-box">
              <span class="sched-box__label">Designated Bay</span>
              <span v-if="!fetchingSpot" class="sched-box__time sched-box__time--stall">Bay P-{{ String(formData.spotId).padStart(2, '0') }}</span>
              <span v-else class="sched-box__time sched-box__time--allocating">Allocating...</span>
              <span class="sched-box__hint">Reserved stall</span>
            </div>
          </div>

          <!-- Vehicle Number Input -->
          <form @submit.prevent="bookParkingSpot" class="ticket-card__form">
            <div class="form-group">
              <label class="form-label" for="plateInput">
                <span>Vehicle Registration Plate</span>
                <span class="form-label__sub">Enter the number plate on your vehicle</span>
              </label>

              <!-- Styled License Plate Input -->
              <div class="plate-input-container">
                <span class="plate-country-badge">IND</span>
                <input
                  id="plateInput"
                  v-model="formData.vehicleNo"
                  type="text"
                  class="plate-text-input"
                  placeholder="e.g. MH 12 AB 4410"
                  required
                  autocomplete="off"
                />
              </div>

              <!-- Quick Plate Presets for Demo Evaluation -->
              <div class="quick-plates">
                <span class="quick-plates__hint">Quick demo plates:</span>
                <button
                  v-for="plate in quickPlates"
                  :key="plate"
                  type="button"
                  class="quick-plate-btn"
                  @click="setPlate(plate)"
                >
                  {{ plate }}
                </button>
              </div>
            </div>

            <!-- Price Breakdown Box -->
            <div class="price-breakdown">
              <div class="price-row">
                <span class="price-row__label">Hourly Rate</span>
                <span class="price-row__val">₹{{ Number(lotDetails.price).toFixed(0) }} / hour</span>
              </div>
              <div class="price-row">
                <span class="price-row__label">Digital Gate Pass</span>
                <span class="price-row__val price-row__val--free">Included (Free)</span>
              </div>
              <div class="price-divider" />
              <div class="price-row price-row--total">
                <span class="price-row__label">Estimated Initial Hour</span>
                <span class="price-row__val price-row__val--strong">₹{{ Number(lotDetails.price).toFixed(0) }}</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="ticket-card__actions">
              <AppButton variant="secondary" size="lg" type="button" @click="goBack">
                Cancel
              </AppButton>
              <AppButton
                variant="primary"
                size="lg"
                type="submit"
                :loading="loading"
                :disabled="!formData.spotId || fetchingSpot"
              >
                Confirm &amp; Reserve Bay
              </AppButton>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.book-page {
  width: 100%;
  max-width: 100%;
  padding: 24px 32px 48px 32px;
  box-sizing: border-box;
}

.book-page__container {
  max-width: 600px;
  margin: var(--space-6, 24px) auto 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-4, 16px);
}

.book-page__alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: var(--radius-md, 12px);
  background: var(--color-status-occupied-bg, #FEE2E2);
  border: 1px solid var(--color-status-occupied, #EF4444);
  color: var(--color-status-occupied, #EF4444);
  font-size: 13px;
  font-weight: 600;
}

/* Ticket Card Styling */
.ticket-card {
  background: var(--color-bg-card, #FFFFFF);
  border: 1px solid var(--color-border-default, #E5E7EB);
  border-radius: var(--radius-xl, 20px);
  overflow: hidden;
  box-shadow: var(--shadow-lg, 0 12px 24px rgba(15, 23, 42, 0.08));
}

.ticket-card__header {
  position: relative;
  width: 100%;
  height: 190px;
  overflow: hidden;
  background: var(--color-navy-deep, #0B1220);
}

.ticket-card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ticket-card__scrim {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(11, 18, 32, 0.3) 0%, rgba(11, 18, 32, 0.85) 100%);
}

.ticket-card__header-content {
  position: absolute;
  bottom: 16px;
  left: 20px;
  right: 20px;
  z-index: 2;
  color: #FFFFFF;
}

.ticket-card__badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: var(--radius-pill, 9999px);
  background: rgba(37, 99, 235, 0.8);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 6px;
}

.ticket-card__lot-name {
  margin: 0;
  font-size: 22px;
  font-weight: 800;
  color: #FFFFFF;
}

.ticket-card__lot-loc {
  margin: 4px 0 0;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: #CBD5E1;
}

.ticket-card__body {
  padding: var(--space-6, 24px);
  display: flex;
  flex-direction: column;
  gap: var(--space-6, 24px);
}

/* Schedule Row */
.ticket-card__schedule {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--color-bg-muted, #F8FAFC);
  border: 1px solid var(--color-border-default, #E5E7EB);
  border-radius: var(--radius-md, 12px);
  padding: var(--space-4, 16px);
}

.sched-box {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sched-box__label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--color-text-secondary, #64748B);
  letter-spacing: 0.05em;
}

.sched-box__time {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.sched-box__time--stall {
  color: var(--color-brand-primary, #2563EB);
  font-family: var(--font-family-mono, monospace);
  font-weight: 800;
}

.sched-box__time--allocating {
  color: var(--color-text-muted, #94A3B8);
  font-style: italic;
}

.sched-box__hint {
  font-size: 11px;
  color: var(--color-text-muted, #94A3B8);
}

.sched-arrow {
  color: var(--color-text-muted, #94A3B8);
}

/* Form */
.ticket-card__form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5, 20px);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.form-label__sub {
  font-size: 11px;
  font-weight: 500;
  color: var(--color-text-secondary, #64748B);
}

/* Plate Input */
.plate-input-container {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border: 2px solid #0F172A;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: border-color var(--transition-fast);
}

.plate-input-container:focus-within {
  border-color: var(--color-brand-primary, #2563EB);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
}

.plate-country-badge {
  background: #2563EB;
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 900;
  padding: 12px 14px;
  letter-spacing: 0.05em;
}

.plate-text-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 12px 14px;
  font-family: var(--font-family-mono, monospace);
  font-size: 17px;
  font-weight: 800;
  letter-spacing: 0.1em;
  color: #0F172A;
  outline: none;
  text-transform: uppercase;
}

.quick-plates {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 4px;
}

.quick-plates__hint {
  font-size: 11px;
  color: var(--color-text-muted, #94A3B8);
}

.quick-plate-btn {
  padding: 3px 8px;
  border-radius: 4px;
  background: var(--color-bg-muted, #F1F5F9);
  border: 1px solid var(--color-border-default, #E2E8F0);
  font-size: 11px;
  font-family: var(--font-family-mono, monospace);
  font-weight: 600;
  color: var(--color-text-secondary, #64748B);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.quick-plate-btn:hover {
  background: var(--color-brand-primary-light, #EAF2FF);
  color: var(--color-brand-primary, #2563EB);
  border-color: var(--color-brand-primary, #2563EB);
}

/* Price Breakdown */
.price-breakdown {
  background: var(--color-bg-muted, #F8FAFC);
  border: 1px solid var(--color-border-default, #E5E7EB);
  border-radius: var(--radius-md, 12px);
  padding: var(--space-4, 16px);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.price-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--color-text-secondary, #64748B);
}

.price-row__val {
  font-weight: 600;
  color: var(--color-text-primary, #111827);
}

.price-row__val--free {
  color: var(--color-status-available, #16A34A);
}

.price-divider {
  height: 1px;
  background: var(--color-border-default, #E5E7EB);
  margin: 4px 0;
}

.price-row--total {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.price-row__val--strong {
  font-size: 17px;
  font-weight: 800;
  color: var(--color-brand-primary, #2563EB);
}

/* Actions */
.ticket-card__actions {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: var(--space-3, 12px);
  margin-top: var(--space-2, 8px);
}

@media (max-width: 768px) {
  .book-page {
    padding: 16px 16px 36px 16px;
  }
}

@media (max-width: 480px) {
  .ticket-card__body {
    padding: 16px;
  }
  .ticket-card__actions {
    grid-template-columns: 1fr;
  }
}
</style>