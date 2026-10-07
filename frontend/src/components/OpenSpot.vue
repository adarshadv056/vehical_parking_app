<script>
import { admin } from '@/api/client';
import { AppPageHeader, AppCard, AppButton, AppBadge } from '@/components/ui';

export default {
  name: 'OpenSpot',
  components: { AppPageHeader, AppCard, AppButton, AppBadge },
  data() {
    return {
      formData: { id: '', status: '' },
      message: '',
      loading: true,
      deleting: false
    };
  },
  mounted() {
    document.title = 'Stall Inspector — ParkSync Admin';
    this.fetchSpotDetails();
  },
  methods: {
    goBack() {
      this.$router.push('/admin');
    },
    async fetchSpotDetails() {
      try {
        this.loading = true;
        const { data, error } = await admin.getSpot(this.$route.params.spotId);
        if (error) throw new Error(error.message);
        const s = data.spot;
        this.formData = {
          id: s.id,
          status: s.is_occupied ? 'Occupied' : 'Available'
        };
      } catch (error) {
        console.error('Error fetching spot details:', error);
        this.message = 'Failed to load bay details';
      } finally {
        this.loading = false;
      }
    },
    async deleteParkingSpot() {
      if (this.formData.status === 'Occupied') {
        this.message = 'Cannot delete a stall with an active vehicle reservation';
        return;
      }
      if (!confirm('Are you sure you want to permanently delete this parking bay?')) {
        return;
      }
      try {
        this.deleting = true;
        const { error } = await admin.deleteSpot(this.$route.params.spotId);
        if (error) throw new Error(error.message);
        this.$router.push('/admin');
      } catch (error) {
        console.error('Error deleting parking spot:', error);
        this.message = error.message || 'Error deleting parking spot';
      } finally {
        this.deleting = false;
      }
    },
    openSpotDetails() {
      this.$router.push(`/admin/spot_details/${this.formData.id}`);
    }
  }
};
</script>

<template>
  <div class="open-spot-page">
    <AppPageHeader
      title="Parking Stall Inspector"
      :subtitle="`Stall Bay #P-${String(formData.id).padStart(2, '0')}`"
      :backRoute="{ name: 'AdminDashboard' }"
    />

    <div class="open-spot__container">
      <div v-if="message" class="open-spot__alert" role="alert">
        {{ message }}
      </div>

      <AppCard class="open-spot__card">
        <!-- Visual Stall Representation -->
        <div class="stall-banner" :class="formData.status === 'Occupied' ? 'stall-banner--occ' : 'stall-banner--avail'">
          <div class="stall-banner__icon">
            <svg v-if="formData.status === 'Occupied'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.4-1.7-1.1-2.2l-2.4-1.8H5.5L3.1 10.8C2.4 11.3 2 12.1 2 13v3c0 .6.4 1 1 1h2" />
              <circle cx="7" cy="17" r="2" />
              <path d="M9 17h6" />
              <circle cx="17" cy="17" r="2" />
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
          <span class="stall-banner__title">Stall Bay #P-{{ String(formData.id).padStart(2, '0') }}</span>
          <span class="stall-banner__status">{{ formData.status }}</span>
        </div>

        <div class="open-spot__details">
          <div class="detail-row">
            <span class="detail-label">Stall Identifier</span>
            <span class="detail-value">Bay #{{ formData.id }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Real-time Status</span>
            <AppBadge
              :variant="formData.status === 'Occupied' ? 'occupied' : 'available'"
              size="md"
            >
              {{ formData.status }}
            </AppBadge>
          </div>
          <div class="detail-row">
            <span class="detail-label">Sensor Diagnostic</span>
            <span class="detail-value detail-value--ok">Online · Operational</span>
          </div>
        </div>

        <div class="open-spot__actions">
          <AppButton variant="secondary" @click="goBack">Back to Control Center</AppButton>
          <AppButton
            v-if="formData.status === 'Occupied'"
            variant="primary"
            @click="openSpotDetails"
          >
            View Active Reservation
          </AppButton>
          <AppButton
            v-else
            variant="danger"
            :loading="deleting"
            @click="deleteParkingSpot"
          >
            Delete Bay
          </AppButton>
        </div>
      </AppCard>
    </div>
  </div>
</template>

<style scoped>
.open-spot-page {
  width: 100%;
  max-width: 100%;
  padding: 24px 32px 48px 32px;
  box-sizing: border-box;
}

.open-spot__container {
  max-width: 520px;
  margin: var(--space-6, 24px) auto 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-4, 16px);
}

.open-spot__alert {
  padding: 12px 16px;
  border-radius: var(--radius-md, 12px);
  background: var(--color-status-occupied-bg, #FEE2E2);
  border: 1px solid var(--color-status-occupied, #EF4444);
  color: var(--color-status-occupied, #EF4444);
  font-size: 13px;
  font-weight: 600;
}

.stall-banner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: var(--space-6, 24px);
  border-radius: var(--radius-md, 12px);
  margin-bottom: var(--space-5, 20px);
}

.stall-banner--avail {
  background: var(--color-status-available-bg, #DCFCE7);
  color: var(--color-status-available, #16A34A);
  border: 1px solid var(--color-status-available, #16A34A);
}

.stall-banner--occ {
  background: var(--color-status-occupied-bg, #FEE2E2);
  color: var(--color-status-occupied, #EF4444);
  border: 1px solid var(--color-status-occupied, #EF4444);
}

.stall-banner__icon {
  width: 44px;
  height: 44px;
}

.stall-banner__icon svg {
  width: 100%;
  height: 100%;
}

.stall-banner__title {
  font-size: 18px;
  font-weight: 800;
  font-family: var(--font-family-mono, monospace);
}

.stall-banner__status {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.open-spot__details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: var(--space-6, 24px);
}

.detail-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--color-border-default, #E5E7EB);
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary, #64748B);
}

.detail-value {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.detail-value--ok {
  color: var(--color-status-available, #16A34A);
  font-weight: 600;
}

.open-spot__actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: var(--space-4, 16px);
  border-top: 1px solid var(--color-border-default, #E5E7EB);
}

@media (max-width: 768px) {
  .open-spot-page {
    padding: 16px 16px 36px 16px;
  }
}
</style>