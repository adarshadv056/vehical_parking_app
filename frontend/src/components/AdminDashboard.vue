<script>
import { admin } from '@/api/client';
import { AppPageHeader, AppButton, AppBadge, KpiCard, ParkingGrid, AppEmptyState } from '@/components/ui';

const GARAGE_IMAGES = [
  'https://images.unsplash.com/photo-1506521781263-d8422e82f27a?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1562619371-b67725b6fde2?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1573348722427-f1d6819fdf98?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'
];

export default {
  name: 'AdminDashboard',
  components: { AppPageHeader, AppButton, AppBadge, KpiCard, ParkingGrid, AppEmptyState },
  data() {
    return {
      parkingLots: [],
      searchQuery: '',
      statusFilter: 'all', // 'all' | 'avail' | 'high'
      message: '',
      loading: true,
      deletingId: null
    };
  },
  computed: {
    totalLots() {
      return this.parkingLots.length;
    },
    totalCapacity() {
      return this.parkingLots.reduce((acc, l) => acc + (l.capacity || 0), 0);
    },
    totalOccupied() {
      return this.parkingLots.reduce((acc, l) => acc + (l.occupied_spots || 0), 0);
    },
    totalAvailable() {
      return Math.max(0, this.totalCapacity - this.totalOccupied);
    },
    systemOccupancyPercent() {
      if (!this.totalCapacity) return 0;
      return Math.round((this.totalOccupied / this.totalCapacity) * 100);
    },
    averageTariff() {
      if (!this.totalLots) return 0;
      const sum = this.parkingLots.reduce((acc, l) => acc + (Number(l.price) || 0), 0);
      return Math.round(sum / this.totalLots);
    },
    filteredLots() {
      return this.parkingLots.filter(lot => {
        const matchesQuery = !this.searchQuery.trim() ||
          lot.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          lot.location.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          (lot.pincode && lot.pincode.includes(this.searchQuery));
        
        if (!matchesQuery) return false;

        if (this.statusFilter === 'avail') {
          return (lot.capacity - lot.occupied_spots) > 0;
        }
        if (this.statusFilter === 'high') {
          return lot.capacity > 0 && (lot.occupied_spots / lot.capacity) >= 0.5;
        }
        return true;
      });
    }
  },
  mounted() {
    document.title = 'ParkSync — Operator Control Center';
    this.fetchParkingLots();
  },
  methods: {
    addParkingLot() {
      this.$router.push('/admin/add_lot');
    },
    getLotImage(lotId) {
      const idx = (Number(lotId) || 1) % GARAGE_IMAGES.length;
      return GARAGE_IMAGES[idx];
    },
    async fetchParkingLots() {
      try {
        this.loading = true;
        const { data, error } = await admin.listLots();
        if (error) throw new Error(error.message);
        this.parkingLots = data.parking_lots || [];
      } catch (error) {
        console.error('Error fetching parking lots:', error);
        this.message = 'Failed to load facility data';
      } finally {
        this.loading = false;
      }
    },
    async deleteParkingLot(lotId) {
      if (!confirm('Are you sure you want to remove this parking facility and all associated bays?')) {
        return;
      }
      try {
        this.deletingId = lotId;
        const { data, error } = await admin.deleteLot(lotId);
        if (error) throw new Error(error.message);
        this.message = data?.message || 'Facility deleted successfully';
        setTimeout(() => { this.message = ''; }, 3000);
        await this.fetchParkingLots();
      } catch (error) {
        console.error('Error deleting parking lot:', error);
        this.message = error.message || 'Error deleting parking lot';
      } finally {
        this.deletingId = null;
      }
    },
    editParkingLot(lotId) {
      this.$router.push(`/admin/edit_lot/${lotId}`);
    },
    handleSpotClick({ spot }) {
      if (spot.is_occupied) {
        this.$router.push(`/admin/spot_details/${spot.id}`);
      } else {
        this.$router.push(`/admin/open_spot/${spot.id}`);
      }
    }
  }
};
</script>

<template>
  <div class="admin-dashboard">
    <AppPageHeader
      title="Operator Control Center"
      subtitle="Real-time facility occupancy, bay allocation, and infrastructure operations"
      :actions="[
        { label: 'View Reports', variant: 'secondary', icon: 'ChartIcon', onClick: () => $router.push('/admin/summary') },
        { label: 'Add Facility', variant: 'primary', icon: 'PlusIcon', onClick: addParkingLot }
      ]"
    />

    <!-- Message Alert -->
    <transition name="fade">
      <div v-if="message" class="admin-dashboard__alert">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <span>{{ message }}</span>
      </div>
    </transition>

    <div class="admin-dashboard__content">
      <!-- Control Center KPI Grid -->
      <section class="admin-dashboard__kpis">
        <KpiCard
          label="Managed Facilities"
          :value="totalLots"
          suffix="garages"
          subtext="Active in network"
          variant="dark"
          icon="DashboardIcon"
        />
        <KpiCard
          label="Total Stall Capacity"
          :value="totalCapacity"
          suffix="bays"
          subtext="Infrastructure capacity"
          icon="PlusIcon"
        />
        <KpiCard
          label="Live Occupancy"
          :value="totalOccupied"
          :suffix="`(${systemOccupancyPercent}%)`"
          :subtext="`${totalAvailable} available bays`"
          :variant="systemOccupancyPercent > 75 ? 'warning' : 'success'"
          icon="CarIcon"
        />
        <KpiCard
          label="Average Tariff"
          :value="averageTariff"
          prefix="₹"
          suffix="/hr"
          subtext="Network hourly average"
          variant="primary"
          icon="ChartIcon"
        />
      </section>

      <!-- Facility Explorer Section -->
      <section class="admin-dashboard__explorer">
        <div class="explorer-header">
          <div>
            <h2 class="explorer-title">Facility Infrastructure &amp; Bay Monitor</h2>
            <p class="explorer-sub">Click on any bay to inspect reservation records or manage stall status</p>
          </div>

          <div class="explorer-filters">
            <!-- Search -->
            <div class="explorer-search">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Filter by facility name or city..."
              />
            </div>

            <!-- Status Buttons -->
            <div class="filter-pills">
              <button
                type="button"
                class="pill-btn"
                :class="{ 'pill-btn--active': statusFilter === 'all' }"
                @click="statusFilter = 'all'"
              >
                All ({{ parkingLots.length }})
              </button>
              <button
                type="button"
                class="pill-btn"
                :class="{ 'pill-btn--active': statusFilter === 'avail' }"
                @click="statusFilter = 'avail'"
              >
                Has Open Bays
              </button>
              <button
                type="button"
                class="pill-btn"
                :class="{ 'pill-btn--active': statusFilter === 'high' }"
                @click="statusFilter = 'high'"
              >
                High Demand (>50%)
              </button>
            </div>
          </div>
        </div>

        <!-- Facility Cards Grid -->
        <div class="admin-dashboard__grid">
          <div
            v-for="lot in filteredLots"
            :key="lot.id"
            class="facility-card"
          >
            <!-- Media Banner -->
            <div class="facility-card__media">
              <img :src="getLotImage(lot.id)" :alt="lot.name" class="facility-card__img" />
              <div class="facility-card__scrim" />
              <div class="facility-card__media-content">
                <div class="facility-card__id-badge">Facility #{{ lot.id }}</div>
                <h3 class="facility-card__name">{{ lot.name }}</h3>
                <p class="facility-card__location">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
                    <circle cx="12" cy="10" r="3" />
                  </svg>
                  {{ lot.location }} • {{ lot.pincode }}
                </p>
              </div>
              <div class="facility-card__price-badge">
                ₹{{ lot.price }}<small>/hr</small>
              </div>
            </div>

            <!-- Stats Bar -->
            <div class="facility-card__stats">
              <div class="facility-stat">
                <span class="facility-stat__label">Capacity</span>
                <span class="facility-stat__val">{{ lot.capacity }} bays</span>
              </div>
              <div class="facility-stat">
                <span class="facility-stat__label">Live Free</span>
                <span class="facility-stat__val facility-stat__val--free">
                  {{ lot.capacity - lot.occupied_spots }} bays
                </span>
              </div>
              <div class="facility-stat">
                <span class="facility-stat__label">Occupancy</span>
                <AppBadge
                  :variant="lot.occupied_spots < lot.capacity ? 'available' : 'occupied'"
                  size="sm"
                >
                  {{ lot.occupied_spots }} / {{ lot.capacity }} occupied
                </AppBadge>
              </div>
            </div>

            <!-- Architectural Stall Bay Grid -->
            <div class="facility-card__grid-section">
              <div class="facility-grid-title">Live Architectural Stall Map</div>
              <ParkingGrid
                :spots="lot.spots || []"
                @spot-click="handleSpotClick"
              />
            </div>

            <!-- Actions Footer -->
            <div class="facility-card__footer">
              <AppButton variant="secondary" size="sm" @click="editParkingLot(lot.id)">
                Edit Facility
              </AppButton>
              <AppButton
                variant="danger"
                size="sm"
                :loading="deletingId === lot.id"
                @click="deleteParkingLot(lot.id)"
              >
                Delete
              </AppButton>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="!loading && filteredLots.length === 0" class="admin-dashboard__empty">
            <AppEmptyState
              icon="PlusIcon"
              title="No facilities matching your search"
              description="Adjust your filters or register a new parking garage"
              :action="{ label: 'Add Parking Facility', onClick: addParkingLot, variant: 'primary' }"
            />
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  width: 100%;
  max-width: 100%;
  padding: 24px 32px 48px 32px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.admin-dashboard__content {
  display: flex;
  flex-direction: column;
  gap: var(--space-6, 24px);
}

.admin-dashboard__alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  border-radius: var(--radius-md, 12px);
  background: var(--color-brand-primary-light, #EAF2FF);
  border: 1px solid var(--color-brand-primary, #2563EB);
  color: var(--color-brand-primary, #2563EB);
  font-size: 14px;
  font-weight: 600;
}

/* KPIs */
.admin-dashboard__kpis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--space-4, 16px);
}

/* Explorer Section */
.admin-dashboard__explorer {
  display: flex;
  flex-direction: column;
  gap: var(--space-5, 20px);
}

.explorer-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.explorer-title {
  margin: 0;
  font-size: 22px;
  font-weight: 800;
  color: var(--color-text-primary, #111827);
  letter-spacing: -0.01em;
}

.explorer-sub {
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--color-text-secondary, #64748B);
}

.explorer-filters {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.explorer-search {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--color-bg-card, #FFFFFF);
  border: 1px solid var(--color-border-default, #E2E8F0);
  border-radius: var(--radius-md, 10px);
  padding: 8px 12px;
  min-width: min(260px, 100%);
}

.explorer-search svg {
  color: var(--color-text-muted, #94A3B8);
}

.explorer-search input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 13px;
  color: var(--color-text-primary, #111827);
  width: 100%;
}

.filter-pills {
  display: flex;
  align-items: center;
  gap: 6px;
}

.pill-btn {
  padding: 8px 14px;
  border-radius: var(--radius-pill, 9999px);
  border: 1px solid var(--color-border-default, #E5E7EB);
  background: var(--color-bg-card, #FFFFFF);
  color: var(--color-text-secondary, #64748B);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.pill-btn:hover {
  border-color: var(--color-border-strong, #CBD5E1);
  color: var(--color-text-primary, #111827);
}

.pill-btn--active {
  background: var(--color-navy-deep, #0B1220);
  border-color: var(--color-navy-deep, #0B1220);
  color: #FFFFFF;
}

/* Facility Grid */
.admin-dashboard__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
  gap: var(--space-6, 24px);
}

.facility-card {
  background: var(--color-bg-card, #FFFFFF);
  border: 1px solid var(--color-border-default, #E5E7EB);
  border-radius: var(--radius-xl, 20px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.facility-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg, 0 12px 24px rgba(15, 23, 42, 0.08));
}

.facility-card__media {
  position: relative;
  width: 100%;
  height: 160px;
  background: var(--color-navy-deep, #0B1220);
  overflow: hidden;
}

.facility-card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.facility-card__scrim {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(11, 18, 32, 0.2) 0%, rgba(11, 18, 32, 0.85) 100%);
}

.facility-card__media-content {
  position: absolute;
  bottom: 12px;
  left: 16px;
  right: 16px;
  color: #FFFFFF;
}

.facility-card__id-badge {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #93C5FD;
}

.facility-card__name {
  margin: 2px 0 0;
  font-size: 18px;
  font-weight: 800;
  color: #FFFFFF;
}

.facility-card__location {
  margin: 2px 0 0;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #CBD5E1;
}

.facility-card__price-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  padding: 4px 10px;
  border-radius: var(--radius-md, 8px);
  font-size: 16px;
  font-weight: 800;
  color: var(--color-brand-primary, #2563EB);
}

.facility-card__price-badge small {
  font-size: 11px;
  color: var(--color-text-secondary, #64748B);
  font-weight: 600;
}

.facility-card__stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 12px 16px;
  background: var(--color-bg-muted, #F8FAFC);
  border-bottom: 1px solid var(--color-border-default, #E5E7EB);
}

.facility-stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.facility-stat__label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--color-text-muted, #94A3B8);
}

.facility-stat__val {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.facility-stat__val--free {
  color: var(--color-status-available, #16A34A);
}

.facility-card__grid-section {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.facility-grid-title {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-secondary, #64748B);
}

.facility-card__footer {
  padding: 12px 16px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid var(--color-border-default, #E5E7EB);
  background: var(--color-bg-card, #FFFFFF);
}

.admin-dashboard__empty {
  grid-column: 1 / -1;
  padding: var(--space-8, 32px);
  background: var(--color-bg-card, #FFFFFF);
  border: 1px solid var(--color-border-default, #E5E7EB);
  border-radius: var(--radius-lg, 16px);
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 16px 16px 36px 16px;
    gap: 16px;
  }
}

@media (max-width: 640px) {
  .admin-dashboard__grid {
    grid-template-columns: 1fr;
  }
  .explorer-search {
    width: 100%;
    min-width: 100%;
  }
}
</style>