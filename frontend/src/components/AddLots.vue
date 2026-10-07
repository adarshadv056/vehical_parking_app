<script>
import { admin } from '@/api/client';
import { AppPageHeader, AppCard, AppButton, AppInput, ParkingLotCard } from '@/components/ui';

export default {
  name: 'AddLots',
  components: {
    AppPageHeader,
    AppCard,
    AppButton,
    AppInput,
    ParkingLotCard
  },
  data() {
    return {
      formData: {
        name: '',
        location: '',
        pincode: '',
        price: '',
        capacity: ''
      },
      tariffPresets: [15, 20, 25, 30, 40],
      capacityPresets: [8, 12, 16, 20, 24],
      message: '',
      messageType: 'error',
      loading: false
    };
  },
  computed: {
    numericCapacity() {
      const cap = Number(this.formData.capacity);
      return (cap > 0 && cap <= 200) ? cap : 12;
    },
    numericPrice() {
      const p = Number(this.formData.price);
      return p > 0 ? p : 25;
    },
    previewLot() {
      return {
        id: 'Preview',
        name: this.formData.name || 'New Executive Mobility Hub',
        location: this.formData.location || 'Metropolitan Commercial District',
        pincode: this.formData.pincode || '10001',
        price: this.numericPrice,
        capacity: this.numericCapacity,
        occupied_spots: 0,
        available_spots: this.numericCapacity
      };
    }
  },
  mounted() {
    document.title = 'Create Facility — ParkSync Admin';
  },
  methods: {
    goBack() {
      this.$router.push('/admin');
    },
    setPricePreset(val) {
      this.formData.price = String(val);
    },
    setCapacityPreset(val) {
      this.formData.capacity = String(val);
    },
    async addParkingLot() {
      if (!this.formData.name.trim() || !this.formData.location.trim() || !this.formData.price || !this.formData.capacity) {
        this.message = 'Please provide all required facility parameters';
        this.messageType = 'error';
        return;
      }

      try {
        this.loading = true;
        this.message = '';
        const { error } = await admin.addLot(this.formData);
        if (error) {
          this.message = error.message || 'Failed to create parking lot';
          this.messageType = 'error';
          return;
        }
        localStorage.setItem('message', `Facility "${this.formData.name}" created successfully with ${this.numericCapacity} allocated stalls.`);
        this.$router.push('/admin');
      } catch (err) {
        console.error('Error adding parking lot:', err);
        this.message = 'An unexpected error occurred while adding facility';
        this.messageType = 'error';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<template>
  <div class="add-lots-page">
    <AppPageHeader
      title="Create Parking Facility"
      subtitle="Provision a new parking garage, allocate bay stalls, and set real-time hourly tariffs"
      :backRoute="{ name: 'AdminDashboard' }"
      :actions="[
        { label: 'Cancel', variant: 'secondary', onClick: goBack },
        { label: 'Dashboard', variant: 'secondary', icon: 'DashboardIcon', onClick: () => $router.push('/admin') }
      ]"
    />

    <!-- Toast Notification Banner -->
    <transition name="fade">
      <div v-if="message" class="add-lots__alert" :class="`add-lots__alert--${messageType}`" role="alert">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <span>{{ message }}</span>
      </div>
    </transition>

    <div class="add-lots__content">
      <div class="add-lots__layout">
        <!-- Configuration Form Card -->
        <AppCard class="add-lots__form-card">
          <template #header>
            <div class="form-card-head">
              <div class="form-card-head__title-group">
                <div class="form-card-head__icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="5" x2="12" y2="19"/>
                    <line x1="5" y1="12" x2="19" y2="12"/>
                  </svg>
                </div>
                <div>
                  <h3 class="form-card-head__title">Facility Specifications</h3>
                  <p class="form-card-head__desc">Enter location details, hourly parking rates, and bay capacity</p>
                </div>
              </div>
            </div>
          </template>

          <form @submit.prevent="addParkingLot" class="add-lots__form">
            <!-- Section 1: Identity & Location -->
            <div class="form-section">
              <span class="form-section__label">Facility Identity &amp; Location</span>
              
              <div class="form-group">
                <AppInput
                  v-model="formData.name"
                  label="Facility Name"
                  placeholder="e.g. Midtown Executive Plaza Underground"
                  required
                  autocomplete="off"
                />
              </div>

              <div class="form-group">
                <AppInput
                  v-model="formData.location"
                  label="Street Address &amp; Neighborhood"
                  type="textarea"
                  placeholder="e.g. 100 Wall Street, Financial District, Manhattan, NY"
                  required
                  :rows="2"
                />
              </div>

              <div class="form-group">
                <AppInput
                  v-model="formData.pincode"
                  label="Postal / Zip Code"
                  placeholder="e.g. 10005"
                  required
                  autocomplete="off"
                />
              </div>
            </div>

            <!-- Section 2: Pricing & Capacity -->
            <div class="form-section">
              <span class="form-section__label">Tariff &amp; Bay Capacity</span>

              <!-- Hourly Tariff with Presets -->
              <div class="form-group">
                <div class="field-label-row">
                  <label class="field-label">Hourly Tariff (₹/hr)</label>
                  <div class="preset-pills">
                    <span class="preset-label">Quick select:</span>
                    <button
                      v-for="preset in tariffPresets"
                      :key="preset"
                      type="button"
                      class="preset-pill"
                      :class="{ 'preset-pill--active': formData.price === String(preset) }"
                      @click="setPricePreset(preset)"
                    >
                      ₹{{ preset }}
                    </button>
                  </div>
                </div>
                <AppInput
                  v-model="formData.price"
                  type="number"
                  placeholder="e.g. 25"
                  required
                  min="1"
                  step="1"
                />
              </div>

              <!-- Bay Stall Capacity with Presets -->
              <div class="form-group">
                <div class="field-label-row">
                  <label class="field-label">Total Bay Stalls (Capacity)</label>
                  <div class="preset-pills">
                    <span class="preset-label">Standard sizes:</span>
                    <button
                      v-for="preset in capacityPresets"
                      :key="preset"
                      type="button"
                      class="preset-pill"
                      :class="{ 'preset-pill--active': formData.capacity === String(preset) }"
                      @click="setCapacityPreset(preset)"
                    >
                      {{ preset }} bays
                    </button>
                  </div>
                </div>
                <AppInput
                  v-model="formData.capacity"
                  type="number"
                  placeholder="e.g. 16"
                  required
                  min="1"
                  max="200"
                  step="1"
                />
                <span class="field-hint">
                  The system will automatically allocate and index individual parking stalls (P-01 to P-{{ numericCapacity }}) for this facility.
                </span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="add-lots__actions">
              <AppButton variant="secondary" size="lg" type="button" @click="goBack">
                Discard Changes
              </AppButton>
              <AppButton variant="primary" size="lg" type="submit" :loading="loading">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                Deploy Facility &amp; Generate Bays
              </AppButton>
            </div>
          </form>
        </AppCard>

        <!-- Right Side: Live Driver Preview & Bay Layout -->
        <div class="add-lots__preview-column">
          <!-- Card Preview Header -->
          <div class="preview-panel-header">
            <div class="preview-panel-badge">
              <span class="live-dot"></span>
              Live Driver Discovery Preview
            </div>
            <span class="preview-panel-sub">Real-time driver card rendering</span>
          </div>

          <!-- Live Card -->
          <div class="preview-card-wrap">
            <ParkingLotCard :lot="previewLot" />
          </div>

          <!-- Bay Allocation Map Preview -->
          <AppCard class="bay-preview-card">
            <template #header>
              <div class="bay-preview-head">
                <span class="bay-preview-title">Automated Bay Allocation Map</span>
                <span class="bay-preview-count">{{ numericCapacity }} Stalls to be created</span>
              </div>
            </template>
            <div class="bay-grid-preview">
              <div
                v-for="n in Math.min(numericCapacity, 24)"
                :key="n"
                class="bay-chip"
              >
                <span class="bay-chip__code">P-{{ String(n).padStart(2, '0') }}</span>
                <span class="bay-chip__status">Available</span>
              </div>
              <div v-if="numericCapacity > 24" class="bay-chip bay-chip--more">
                +{{ numericCapacity - 24 }} more bays
              </div>
            </div>
            <p class="bay-preview-note">
              Upon submission, SQLite will instantiate each stall with ultrasonic sensor clearance and ready-to-book availability.
            </p>
          </AppCard>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.add-lots-page {
  width: 100%;
  max-width: 100%;
  padding: 24px 32px 48px 32px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.add-lots__content {
  width: 100%;
}

.add-lots__layout {
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 28px;
  align-items: start;
  width: 100%;
}

@media (max-width: 1100px) {
  .add-lots__layout {
    grid-template-columns: 1fr;
  }
}

/* Alert Notification */
.add-lots__alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  border-radius: var(--radius-md, 12px);
  font-size: 14px;
  font-weight: 600;
  width: 100%;
  box-sizing: border-box;
}

.add-lots__alert--error {
  background: var(--color-status-occupied-bg, #FEE2E2);
  color: var(--color-status-occupied, #EF4444);
  border: 1px solid var(--color-status-occupied, #EF4444);
}

.add-lots__alert--success {
  background: var(--color-status-available-bg, #DCFCE7);
  color: var(--color-status-available, #16A34A);
  border: 1px solid var(--color-status-available, #16A34A);
}

/* Form Card */
.form-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.form-card-head__title-group {
  display: flex;
  align-items: center;
  gap: 14px;
}

.form-card-head__icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--color-brand-primary-light, #EAF2FF);
  color: var(--color-brand-primary, #2563EB);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.form-card-head__title {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: var(--color-text-primary, #111827);
  line-height: 1.2;
}

.form-card-head__desc {
  margin: 3px 0 0 0;
  font-size: 13px;
  color: var(--color-text-secondary, #64748B);
}

/* Form Structure */
.add-lots__form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--color-border-default, #E2E8F0);
}

.form-section:last-of-type {
  border-bottom: none;
  padding-bottom: 0;
}

.form-section__label {
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-brand-primary, #2563EB);
  margin-bottom: 2px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.field-label {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.preset-pills {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.preset-label {
  font-size: 11px;
  color: var(--color-text-secondary, #64748B);
  font-weight: 600;
}

.preset-pill {
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  border: 1px solid var(--color-border-default, #E2E8F0);
  background: var(--color-bg-muted, #F8FAFC);
  color: var(--color-text-secondary, #64748B);
  cursor: pointer;
  transition: all 0.15s ease;
}

.preset-pill:hover {
  background: var(--color-bg-white, #FFFFFF);
  color: var(--color-text-primary, #111827);
  border-color: var(--color-border-strong, #CBD5E1);
}

.preset-pill--active {
  background: var(--color-brand-primary, #2563EB) !important;
  color: #FFFFFF !important;
  border-color: var(--color-brand-primary, #2563EB) !important;
}

.field-hint {
  font-size: 12px;
  color: var(--color-text-secondary, #64748B);
  line-height: 1.4;
  margin-top: 2px;
}

/* Actions */
.add-lots__actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border-default, #E2E8F0);
}

/* Right Column: Preview Panel */
.add-lots__preview-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 90px;
}

.preview-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.preview-panel-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--color-brand-primary, #2563EB);
}

.live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #16A34A;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.2);
}

.preview-panel-sub {
  font-size: 12px;
  color: var(--color-text-secondary, #64748B);
}

.preview-card-wrap {
  width: 100%;
}

/* Bay Allocation Map Preview */
.bay-preview-card {
  width: 100%;
}

.bay-preview-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.bay-preview-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.bay-preview-count {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-brand-primary, #2563EB);
  background: var(--color-brand-primary-light, #EAF2FF);
  padding: 2px 8px;
  border-radius: 999px;
}

.bay-grid-preview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
  gap: 8px;
  margin-bottom: 12px;
}

.bay-chip {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8px 4px;
  border-radius: 8px;
  background: var(--color-status-available-bg, #DCFCE7);
  border: 1px solid rgba(22, 163, 74, 0.25);
  gap: 2px;
}

.bay-chip__code {
  font-family: monospace;
  font-size: 12px;
  font-weight: 800;
  color: #16A34A;
}

.bay-chip__status {
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  color: #15803D;
}

.bay-chip--more {
  background: var(--color-bg-muted, #F8FAFC);
  border: 1px dashed var(--color-border-strong, #CBD5E1);
  color: var(--color-text-secondary, #64748B);
  font-size: 11px;
  font-weight: 700;
}

.bay-preview-note {
  margin: 0;
  font-size: 12px;
  color: var(--color-text-secondary, #64748B);
  line-height: 1.4;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .add-lots-page {
    padding: 16px 16px 36px 16px;
    gap: 16px;
  }
}
</style>