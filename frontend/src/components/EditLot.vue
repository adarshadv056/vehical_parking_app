<script>
import { admin } from '@/api/client';
import { AppPageHeader, AppCard, AppButton, AppInput, ParkingLotCard } from '@/components/ui';

export default {
  name: 'EditLot',
  components: { AppPageHeader, AppCard, AppButton, AppInput, ParkingLotCard },
  data() {
    return {
      formData: {
        name: '',
        location: '',
        pincode: '',
        price: '',
        capacity: ''
      },
      originalData: {},
      message: '',
      loading: true,
      submitting: false
    };
  },
  computed: {
    previewLot() {
      return {
        id: this.$route.params.id,
        name: this.formData.name || 'Parking Facility',
        location: this.formData.location || 'Facility Location',
        pincode: this.formData.pincode || '10001',
        price: Number(this.formData.price) || 40,
        capacity: Number(this.formData.capacity) || 16,
        occupied_spots: 0,
        available_spots: Number(this.formData.capacity) || 16
      };
    }
  },
  async mounted() {
    document.title = 'Edit Facility — ParkSync Admin';
    await this.fetchParkingLot();
  },
  methods: {
    goBack() {
      this.$router.push('/admin');
    },
    async fetchParkingLot() {
      try {
        this.loading = true;
        const { data, error } = await admin.getLot(this.$route.params.id);
        if (error) throw new Error(error.message);
        const lot = data.parking_lot;
        this.formData = {
          name: lot.name,
          location: lot.location,
          pincode: lot.pincode,
          price: lot.price,
          capacity: lot.capacity
        };
        this.originalData = { ...this.formData };
      } catch (error) {
        console.error('Error fetching parking lot:', error);
        this.message = 'Failed to load facility data';
      } finally {
        this.loading = false;
      }
    },
    async editParkingLot() {
      try {
        this.submitting = true;
        const { error } = await admin.editLot(this.$route.params.id, this.formData);
        if (error) {
          this.message = error.message;
          return;
        }
        this.$router.push('/admin');
      } catch (error) {
        console.error('Error updating parking lot:', error);
        this.message = 'Failed to update facility';
      } finally {
        this.submitting = false;
      }
    }
  }
};
</script>

<template>
  <div class="edit-lot-page">
    <AppPageHeader
      title="Edit Parking Facility"
      :subtitle="`Update configuration for Facility #${$route.params.id}`"
      :backRoute="{ name: 'AdminDashboard' }"
    />

    <div class="edit-lot__layout">
      <!-- Form Panel -->
      <AppCard class="edit-lot__form-card">
        <template #header>
          <div class="form-card-head">
            <h3>Facility Parameters</h3>
            <p>Modify capacity, pricing, or physical address</p>
          </div>
        </template>

        <div v-if="message" class="edit-lot__alert" role="alert">
          {{ message }}
        </div>

        <form @submit.prevent="editParkingLot" class="edit-lot__form">
          <AppInput
            v-model="formData.name"
            label="Facility Name"
            placeholder="Parking Lot Name"
            required
            autocomplete="off"
          />

          <AppInput
            v-model="formData.location"
            label="Address &amp; City"
            type="textarea"
            placeholder="Parking lot address"
            required
            :rows="3"
          />

          <div class="edit-lot__form-row">
            <AppInput
              v-model="formData.pincode"
              label="Postal Code"
              placeholder="PIN code"
              required
              autocomplete="off"
            />
            <AppInput
              v-model="formData.price"
              label="Hourly Tariff (₹)"
              type="number"
              placeholder="Price per hour"
              required
              min="0"
              step="1"
            />
          </div>

          <AppInput
            v-model="formData.capacity"
            label="Maximum Bays"
            type="number"
            placeholder="Maximum spots"
            required
            min="1"
          />

          <div class="edit-lot__actions">
            <AppButton variant="secondary" size="lg" @click="goBack">Cancel</AppButton>
            <AppButton variant="primary" size="lg" type="submit" :loading="submitting">
              Save Changes
            </AppButton>
          </div>
        </form>
      </AppCard>

      <!-- Live Preview Panel -->
      <div class="edit-lot__preview-panel">
        <div class="preview-badge">Live Card Preview</div>
        <ParkingLotCard :lot="previewLot" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.edit-lot-page {
  width: 100%;
  max-width: 100%;
  padding: 24px 32px 48px 32px;
  box-sizing: border-box;
}

.edit-lot__layout {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: var(--space-6, 24px);
  margin-top: var(--space-6, 24px);
  align-items: start;
}

.form-card-head h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.form-card-head p {
  margin: 2px 0 0;
  font-size: 12px;
  color: var(--color-text-secondary, #64748B);
}

.edit-lot__alert {
  margin-bottom: var(--space-4, 16px);
  padding: var(--space-3, 12px);
  border-radius: var(--radius-md, 12px);
  background: var(--color-status-occupied-bg, #FEE2E2);
  border: 1px solid var(--color-status-occupied, #EF4444);
  color: var(--color-status-occupied, #EF4444);
  font-size: 13px;
  font-weight: 600;
}

.edit-lot__form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4, 16px);
}

.edit-lot__form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4, 16px);
}

.edit-lot__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3, 12px);
  margin-top: var(--space-4, 16px);
  padding-top: var(--space-4, 16px);
  border-top: 1px solid var(--color-border-default, #E5E7EB);
}

.edit-lot__preview-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: sticky;
  top: 90px;
}

.preview-badge {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-brand-primary, #2563EB);
}

@media (max-width: 900px) {
  .edit-lot__layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .edit-lot-page {
    padding: 16px 16px 36px 16px;
  }
}

@media (max-width: 540px) {
  .edit-lot__form-row {
    grid-template-columns: 1fr;
  }
}
</style>