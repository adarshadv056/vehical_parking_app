<script>
import { admin } from '@/api/client';
import { AppPageHeader, AppCard, AppButton, AppBadge } from '@/components/ui';

export default {
  name: 'SpotDetails',
  components: { AppPageHeader, AppCard, AppButton, AppBadge },
  data() {
    return {
      formData: {
        spotId: '',
        customerId: '',
        vehicleNo: '',
        parkingTime: '',
        estimatedCost: ''
      },
      loading: true
    };
  },
  mounted() {
    document.title = 'Reservation Details — ParkSync Admin';
    this.fetchReservations();
  },
  methods: {
    goBack() {
      this.$router.push(`/admin/open_spot/${this.$route.params.spotId}`);
    },
    formatDateTime(dateString) {
      if (!dateString) return '—';
      return new Date(dateString).toLocaleString('en-IN', {
        dateStyle: 'medium',
        timeStyle: 'short'
      });
    },
    async fetchReservations() {
      try {
        this.loading = true;
        const { data, error } = await admin.getReservation(this.$route.params.spotId);
        if (error) throw new Error(error.message);
        const r = data.reservation;
        this.formData = {
          spotId: r.spot_id,
          customerId: r.user_id,
          vehicleNo: r.vehicle_number,
          parkingTime: r.parking_time,
          estimatedCost: r.parking_cost
        };
      } catch (error) {
        console.error('Error fetching spot details:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<template>
  <div class="spot-details-page">
    <AppPageHeader
      title="Active Bay Reservation"
      :subtitle="`Occupant record for Stall Bay #P-${String($route.params.spotId).padStart(2, '0')}`"
      :backRoute="{ name: 'OpenSpot', params: { spotId: $route.params.spotId } }"
    />

    <div class="spot-details__container">
      <AppCard class="spot-details__card">
        <!-- Vehicle Hero Header -->
        <div class="occupant-hero">
          <div class="occupant-hero__left">
            <span class="occupant-hero__label">Parked Vehicle</span>
            <div class="license-plate">
              <span class="license-plate__ind">IND</span>
              <span class="license-plate__text">{{ formData.vehicleNo || 'MH 12 AB 4410' }}</span>
            </div>
          </div>
          <AppBadge variant="occupied" size="lg">Occupied</AppBadge>
        </div>

        <div class="spot-details__grid">
          <div class="info-cell">
            <span class="info-label">Stall Identifier</span>
            <span class="info-val info-val--bay">Bay #{{ formData.spotId }}</span>
          </div>

          <div class="info-cell">
            <span class="info-label">Driver User ID</span>
            <span class="info-val">User #{{ formData.customerId }}</span>
          </div>

          <div class="info-cell">
            <span class="info-label">Entry / Check-in</span>
            <span class="info-val">{{ formatDateTime(formData.parkingTime) }}</span>
          </div>

          <div class="info-cell">
            <span class="info-label">Accrued Tariff</span>
            <span class="info-val info-val--cost">₹{{ formData.estimatedCost }}</span>
          </div>

          <div class="info-cell info-cell--full">
            <span class="info-label">Access Method</span>
            <span class="info-val">Digital Reservation &amp; Plate Recognition</span>
          </div>
        </div>

        <div class="spot-details__actions">
          <AppButton variant="secondary" @click="goBack">Close Inspector</AppButton>
        </div>
      </AppCard>
    </div>
  </div>
</template>

<style scoped>
.spot-details-page {
  width: 100%;
  max-width: 100%;
  padding: 24px 32px 48px 32px;
  box-sizing: border-box;
}

.spot-details__container {
  max-width: 520px;
  margin: var(--space-6, 24px) auto 0;
}

.occupant-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--color-navy-deep, #0B1220);
  padding: var(--space-5, 20px);
  border-radius: var(--radius-md, 12px);
  margin-bottom: var(--space-6, 24px);
  color: #FFFFFF;
}

.occupant-hero__left {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.occupant-hero__label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  color: #94A3B8;
  letter-spacing: 0.05em;
}

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
  font-size: 14px;
  letter-spacing: 0.08em;
}

.license-plate__ind {
  background: #2563EB;
  color: #FFFFFF;
  padding: 1px 4px;
  border-radius: 3px;
  font-size: 9px;
  margin-right: 6px;
  font-weight: 900;
}

.spot-details__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4, 16px);
  margin-bottom: var(--space-6, 24px);
}

.info-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  background: var(--color-bg-muted, #F8FAFC);
  border-radius: 8px;
  border: 1px solid var(--color-border-default, #E5E7EB);
}

.info-cell--full {
  grid-column: 1 / -1;
}

.info-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-secondary, #64748B);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.info-val {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.info-val--bay {
  font-family: var(--font-family-mono, monospace);
  color: var(--color-brand-primary, #2563EB);
}

.info-val--cost {
  color: var(--color-status-available, #16A34A);
  font-size: 16px;
}

.spot-details__actions {
  display: flex;
  justify-content: flex-end;
  padding-top: var(--space-4, 16px);
  border-top: 1px solid var(--color-border-default, #E5E7EB);
}

@media (max-width: 768px) {
  .spot-details-page {
    padding: 16px 16px 36px 16px;
  }
}

@media (max-width: 480px) {
  .spot-details__grid {
    grid-template-columns: 1fr;
  }
}
</style>