<script>
import { userApi, auth } from '@/api/client';
import { AppPageHeader, AppDataTable, AppEmptyState, ParkingLotCard, ActiveSessionCard, KpiCard } from '@/components/ui';

const GARAGE_IMAGES = [
  'https://images.unsplash.com/photo-1506521781263-d8422e82f27a?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1562619371-b67725b6fde2?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1573348722427-f1d6819fdf98?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'
];

export default {
  name: 'UserDashboard',
  components: {
    AppPageHeader,
    AppDataTable,
    AppEmptyState,
    ParkingLotCard,
    ActiveSessionCard,
    KpiCard
  },
  data() {
    return {
      searchQuery: '',
      activeFilter: 'all',
      viewMode: 'grid', // 'grid' | 'table'
      sortBy: 'default', // 'default' | 'price_asc' | 'capacity_desc' | 'name_asc'
      parkingLots: [],
      activeSession: null,
      hasSearched: false,
      message: '',
      messageType: 'info',
      userId: '',
      searchLoading: false,
      parkingOutLoading: false,
      filterPills: [
        { id: 'all', label: 'All Garages', query: ' ' },
        { id: 'ny', label: 'Manhattan, NY', query: 'Manhattan' },
        { id: 'jersey', label: 'Jersey City', query: 'Jersey City' },
        { id: 'queens', label: 'Queens, NY', query: 'Queens' },
        { id: 'newark', label: 'Newark, NJ', query: 'Newark' }
      ]
    };
  },
  computed: {
    totalAvailableBays() {
      return this.parkingLots.reduce((acc, l) => {
        const avail = l.available_spots ?? Math.max(0, (l.total_spots || l.capacity || 0) - (l.occupied_spots || 0));
        return acc + avail;
      }, 0);
    },
    minTariff() {
      if (!this.parkingLots.length) return 0;
      return Math.min(...this.parkingLots.map(l => Number(l.price) || 0));
    },
    processedParkingLots() {
      let lots = [...this.parkingLots];
      if (this.sortBy === 'price_asc') {
        lots.sort((a, b) => Number(a.price) - Number(b.price));
      } else if (this.sortBy === 'capacity_desc') {
        lots.sort((a, b) => {
          const availA = a.available_spots ?? Math.max(0, (a.total_spots || 0) - (a.occupied_spots || 0));
          const availB = b.available_spots ?? Math.max(0, (b.total_spots || 0) - (b.occupied_spots || 0));
          return availB - availA;
        });
      } else if (this.sortBy === 'name_asc') {
        lots.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
      }
      return lots;
    },
    lotColumns() {
      return [
        {
          key: 'facility',
          label: 'Parking Facility',
          render: (i) => ({
            type: 'custom',
            html: `
              <div style="display: flex; align-items: center; gap: 14px; min-width: 240px;">
                <img
                  src="${this.getLotImage(i)}"
                  alt="${i.name}"
                  style="width: 52px; height: 52px; border-radius: 8px; object-fit: cover; flex-shrink: 0; box-shadow: 0 2px 6px rgba(0,0,0,0.08);"
                />
                <div style="display: flex; flex-direction: column; gap: 3px; min-width: 0;">
                  <span style="font-weight: 700; font-size: 14px; color: var(--color-text-primary, #111827); line-height: 1.3;">${i.name}</span>
                  <span style="font-size: 12px; color: var(--color-text-secondary, #64748B); display: flex; align-items: center; gap: 4px;">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                    ${i.location} ${i.pincode ? `&bull; ${i.pincode}` : ''}
                  </span>
                </div>
              </div>
            `
          })
        },
        {
          key: 'occupancy',
          label: 'Live Capacity',
          width: '180px',
          render: (i) => {
            const total = i.total_spots || i.capacity || 10;
            const occupied = i.occupied_spots || 0;
            const avail = i.available_spots ?? Math.max(0, total - occupied);
            const isFull = avail <= 0;
            const pct = Math.min(100, Math.round((occupied / total) * 100));
            const color = isFull ? '#EF4444' : (pct > 75 ? '#F59E0B' : '#16A34A');
            const bg = isFull ? '#FEE2E2' : (pct > 75 ? '#FEF3C7' : '#DCFCE7');
            return {
              type: 'custom',
              html: `
                <div style="display: flex; flex-direction: column; gap: 6px; width: 100%;">
                  <div style="display: flex; align-items: center; justify-content: space-between;">
                    <span style="display: inline-flex; align-items: center; gap: 4px; font-size: 11px; font-weight: 700; color: ${color}; background: ${bg}; padding: 2px 8px; border-radius: 999px;">
                      <span style="width: 5px; height: 5px; border-radius: 50%; background: ${color};"></span>
                      ${isFull ? 'Full' : `${avail} Free`}
                    </span>
                    <span style="font-size: 11px; color: var(--color-text-secondary, #64748B); font-weight: 600;">${occupied}/${total}</span>
                  </div>
                  <div style="height: 5px; border-radius: 999px; background: #E2E8F0; overflow: hidden; width: 100%;">
                    <div style="height: 100%; width: ${pct}%; background: ${color}; border-radius: 999px;"></div>
                  </div>
                </div>
              `
            };
          }
        },
        {
          key: 'tariff',
          label: 'Tariff',
          width: '120px',
          render: (i) => ({
            type: 'custom',
            html: `
              <div style="display: flex; align-items: baseline; gap: 2px;">
                <span style="font-size: 16px; font-weight: 800; color: var(--color-text-primary, #111827);">₹${Number(i.price).toFixed(0)}</span>
                <span style="font-size: 11px; color: var(--color-text-secondary, #64748B); font-weight: 600;">/hr</span>
              </div>
            `
          })
        },
        {
          key: 'amenities',
          label: 'Amenities',
          width: '160px',
          render: () => ({
            type: 'custom',
            html: `
              <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                <span style="font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; background: var(--color-bg-muted, #F8FAFC); color: var(--color-text-secondary, #64748B); border: 1px solid var(--color-border-default, #E5E7EB);">CCTV</span>
                <span style="font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; background: #EAF2FF; color: #2563EB; border: 1px solid #BFDBFE;">EV READY</span>
                <span style="font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; background: var(--color-bg-muted, #F8FAFC); color: var(--color-text-secondary, #64748B); border: 1px solid var(--color-border-default, #E5E7EB);">24/7</span>
              </div>
            `
          })
        },
        {
          key: 'action',
          label: 'Reserve Space',
          width: '140px',
          render: (i) => {
            const avail = i.available_spots ?? Math.max(0, (i.total_spots || i.capacity || 0) - (i.occupied_spots || 0));
            return {
              type: 'button',
              label: avail > 0 ? 'Reserve Bay' : 'Lot Full',
              variant: avail > 0 ? 'primary' : 'secondary',
              size: 'sm',
              disabled: avail <= 0,
              onClick: () => this.bookParkingSpot(i)
            };
          }
        }
      ];
    }
  },
  mounted() {
    document.title = 'ParkSync — Driver Mobility Console';
    this.checkForMessage();
    const payload = auth.getPayload();
    this.userId = payload?.sub;
    this.fetchActiveSession();
    this.fetchParkingLots(' '); // Default initial discovery view
  },
  methods: {
    getLotImage(lot) {
      if (lot?.image_url) return lot.image_url;
      const idx = Math.abs((Number(lot?.id) || 1) - 1) % GARAGE_IMAGES.length;
      return GARAGE_IMAGES[idx];
    },
    async fetchActiveSession() {
      try {
        const { data, error } = await userApi.getHistory();
        if (error) return;
        const active = (data.history || []).find(h => !h.leaving_time);
        this.activeSession = active || null;
      } catch (e) {
        console.error('Failed to check active session:', e);
      }
    },
    async fetchParkingLots(overrideQuery) {
      const q = typeof overrideQuery === 'string' ? overrideQuery : (this.searchQuery.trim() || ' ');
      try {
        this.searchLoading = true;
        const { data, error } = await userApi.searchLots(q);
        if (error) throw new Error(error.message);
        this.hasSearched = true;
        this.parkingLots = data.parking_lots || [];
      } catch (error) {
        console.error('Error fetching parking lots:', error);
        this.showMessage('Failed to load parking facilities', 'error');
      } finally {
        this.searchLoading = false;
      }
    },
    applyFilter(pill) {
      this.activeFilter = pill.id;
      this.searchQuery = pill.id === 'all' ? '' : pill.query;
      this.fetchParkingLots(pill.query);
    },
    bookParkingSpot(lot) {
      this.$router.push({
        path: '/user/book_spot',
        query: {
          lotId: lot.id,
          name: lot.name,
          location: lot.location,
          price: lot.price
        }
      });
    },
    async parkOut(reservationId) {
      try {
        this.parkingOutLoading = true;
        const { data, error } = await userApi.parkOut(reservationId);
        if (error) throw new Error(error.message);
        this.showMessage(data?.message || 'Checked out successfully!', 'success');
        this.activeSession = null;
        await this.fetchParkingLots();
      } catch (error) {
        console.error('Error parking out:', error);
        this.showMessage(error.message || 'Error checking out', 'error');
      } finally {
        this.parkingOutLoading = false;
      }
    },
    checkForMessage() {
      const msg = localStorage.getItem('message');
      if (msg) {
        this.showMessage(msg, 'success');
        localStorage.removeItem('message');
      }
    },
    showMessage(text, type = 'info') {
      this.message = text;
      this.messageType = type;
      setTimeout(() => {
        this.message = '';
      }, 3500);
    }
  }
};
</script>

<template>
  <div class="user-dashboard">
    <!-- Header with zero top buttons (as requested) -->
    <AppPageHeader
      title="Driver Mobility Console"
      subtitle="Discover premium parking facilities, compare real-time rates, and reserve your bay"
    />

    <!-- Toast Notification Banner -->
    <transition name="fade">
      <div v-if="message" class="user-dashboard__alert" :class="`user-dashboard__alert--${messageType}`">
        <svg v-if="messageType === 'success'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
          <polyline points="22 4 12 14.01 9 11.01" />
        </svg>
        <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <span>{{ message }}</span>
      </div>
    </transition>

    <div class="user-dashboard__content">
      <!-- Live KPIs Row (Full Width Grid) -->
      <section class="user-dashboard__kpi-grid">
        <KpiCard
          label="Available Facilities"
          :value="parkingLots.length"
          suffix="garages"
          subtext="Covered &amp; EV verified"
          icon="MapPinIcon"
        />
        <KpiCard
          label="Live Open Bays"
          :value="totalAvailableBays"
          suffix="bays"
          subtext="Available right now"
          variant="primary"
          icon="ZapIcon"
        />
        <KpiCard
          label="Starting Tariff"
          :value="minTariff"
          prefix="₹"
          suffix="/hr"
          subtext="Lowest hourly rate"
          icon="ShieldIcon"
        />
        <KpiCard
          label="Current Session"
          :value="activeSession ? 1 : 0"
          suffix="active"
          :subtext="activeSession ? `Bay #${activeSession.spot_id}` : 'No active vehicle'"
          :variant="activeSession ? 'success' : 'default'"
          icon="CarIcon"
        />
      </section>

      <!-- Active Session Hero (Displayed prominently if driver is currently parked) -->
      <section v-if="activeSession" class="user-dashboard__active-wrap">
        <ActiveSessionCard
          :session="activeSession"
          :loading="parkingOutLoading"
          @park-out="parkOut"
        />
      </section>

      <!-- Parking Discovery Section -->
      <section class="user-dashboard__section">
        <div class="user-dashboard__section-header">
          <div class="user-dashboard__section-title-wrap">
            <h2 class="user-dashboard__section-title">Find &amp; Reserve Parking</h2>
            <p class="user-dashboard__section-desc">Search premium parking garages and reserve your space before arrival</p>
          </div>
          
          <div class="user-dashboard__controls-group">
            <!-- Sort Dropdown -->
            <div class="user-dashboard__sort-wrap">
              <select v-model="sortBy" class="sort-select" aria-label="Sort facilities">
                <option value="default">Default Order</option>
                <option value="price_asc">Price: Low to High</option>
                <option value="capacity_desc">Most Open Bays</option>
                <option value="name_asc">Name: A to Z</option>
              </select>
            </div>

            <!-- View Toggles (Cards vs List) -->
            <div class="user-dashboard__view-toggles">
              <button
                type="button"
                class="view-toggle-btn"
                :class="{ 'view-toggle-btn--active': viewMode === 'grid' }"
                @click="viewMode = 'grid'"
                title="Cards Grid View"
              >
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="7" height="7" rx="1.5" />
                  <rect x="14" y="3" width="7" height="7" rx="1.5" />
                  <rect x="14" y="14" width="7" height="7" rx="1.5" />
                  <rect x="3" y="14" width="7" height="7" rx="1.5" />
                </svg>
                <span>Cards</span>
              </button>
              <button
                type="button"
                class="view-toggle-btn"
                :class="{ 'view-toggle-btn--active': viewMode === 'table' }"
                @click="viewMode = 'table'"
                title="Table List View"
              >
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="8" y1="6" x2="21" y2="6" stroke-linecap="round" />
                  <line x1="8" y1="12" x2="21" y2="12" stroke-linecap="round" />
                  <line x1="8" y1="18" x2="21" y2="18" stroke-linecap="round" />
                  <line x1="3" y1="6" x2="3.01" y2="6" stroke-width="3" stroke-linecap="round" />
                  <line x1="3" y1="12" x2="3.01" y2="12" stroke-width="3" stroke-linecap="round" />
                  <line x1="3" y1="18" x2="3.01" y2="18" stroke-width="3" stroke-linecap="round" />
                </svg>
                <span>List</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Search Bar & Filter Pills -->
        <div class="user-dashboard__search-box">
          <div class="user-dashboard__search-input-wrap">
            <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              class="search-input"
              placeholder="Search garage by name, address, landmark, or pincode..."
              :disabled="searchLoading"
              @keyup.enter="fetchParkingLots"
            />
            <button
              v-if="searchQuery"
              type="button"
              class="search-clear-btn"
              @click="searchQuery = ''; fetchParkingLots(' ')"
              title="Clear search"
            >
              &times;
            </button>
            <button
              type="button"
              class="search-submit-btn"
              :disabled="searchLoading"
              @click="fetchParkingLots"
            >
              <span v-if="searchLoading" class="btn-spinner" />
              <span v-else>Search</span>
            </button>
          </div>

          <!-- Quick Discovery Pills -->
          <div class="user-dashboard__pills">
            <button
              v-for="pill in filterPills"
              :key="pill.id"
              type="button"
              class="filter-pill"
              :class="{ 'filter-pill--active': activeFilter === pill.id }"
              @click="applyFilter(pill)"
            >
              {{ pill.label }}
            </button>
          </div>
        </div>

        <!-- Results: Grid View (Cards Mode) -->
        <div v-if="viewMode === 'grid'" class="user-dashboard__lots-grid">
          <ParkingLotCard
            v-for="lot in processedParkingLots"
            :key="lot.id"
            :lot="lot"
            @book="bookParkingSpot(lot)"
          />

          <div v-if="!searchLoading && processedParkingLots.length === 0" class="user-dashboard__empty-wrap">
            <AppEmptyState
              icon="SearchIcon"
              title="No facilities found"
              description="Try adjusting your search query or clicking 'All Garages'"
              :action="{ label: 'Show All Garages', onClick: () => applyFilter(filterPills[0]), variant: 'primary' }"
            />
          </div>
        </div>

        <!-- Results: Table View (List Mode) -->
        <div v-else class="user-dashboard__lots-table">
          <AppDataTable
            :columns="lotColumns"
            :items="processedParkingLots"
            :loading="searchLoading"
            emptyMessage="No parking facilities found matching your criteria"
            emptyIcon="InboxIcon"
            :showPagination="processedParkingLots.length > 8"
            :pageSize="8"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.user-dashboard {
  width: 100%;
  max-width: 100%;
  padding: 24px 32px 48px 32px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.user-dashboard__content {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Alert Banner */
.user-dashboard__alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  border-radius: var(--radius-md, 12px);
  font-size: 14px;
  font-weight: 600;
}

.user-dashboard__alert--success {
  background: var(--color-status-available-bg, #DCFCE7);
  color: var(--color-status-available, #16A34A);
  border: 1px solid var(--color-status-available, #16A34A);
}

.user-dashboard__alert--error {
  background: var(--color-status-occupied-bg, #FEE2E2);
  color: var(--color-status-occupied, #EF4444);
  border: 1px solid var(--color-status-occupied, #EF4444);
}

.user-dashboard__alert--info {
  background: var(--color-status-info-bg, #EAF2FF);
  color: var(--color-brand-primary, #2563EB);
  border: 1px solid var(--color-brand-primary, #2563EB);
}

/* KPI Row - Full Width 4 Columns on Desktop */
.user-dashboard__kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  width: 100%;
}

@media (max-width: 1200px) {
  .user-dashboard__kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .user-dashboard__kpi-grid {
    grid-template-columns: 1fr;
  }
}

/* Active Session Wrap */
.user-dashboard__active-wrap {
  width: 100%;
}

/* Section Header & Alignment */
.user-dashboard__section {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.user-dashboard__section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  width: 100%;
}

.user-dashboard__section-title-wrap {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-dashboard__section-title {
  font-size: 20px;
  font-weight: 800;
  color: var(--color-text-primary);
  margin: 0;
  letter-spacing: -0.01em;
  line-height: 1.2;
}

.user-dashboard__section-desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.4;
}

.user-dashboard__controls-group {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.sort-select {
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid var(--color-border-default);
  background: var(--color-bg-white);
  color: var(--color-text-primary);
  font-size: 13px;
  font-weight: 600;
  outline: none;
  cursor: pointer;
  height: 38px;
  transition: border-color 0.15s ease;
}

.sort-select:focus {
  border-color: var(--color-brand-primary);
}

/* View Toggles */
.user-dashboard__view-toggles {
  display: flex;
  align-items: center;
  background: var(--color-bg-white);
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  padding: 3px;
  gap: 3px;
  height: 38px;
  box-sizing: border-box;
}

.view-toggle-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 12px;
  height: 30px;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 700;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.view-toggle-btn:hover {
  color: var(--color-text-primary);
}

.view-toggle-btn--active {
  background: var(--color-brand-primary);
  color: #FFFFFF !important;
}

/* Search Box - Full Width with Precision Alignment */
.user-dashboard__search-box {
  background: var(--color-bg-white);
  border: 1px solid var(--color-border-default);
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  width: 100%;
  box-sizing: border-box;
}

.user-dashboard__search-input-wrap {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
}

.search-icon {
  position: absolute;
  left: 14px;
  color: var(--color-text-muted);
  pointer-events: none;
}

.search-input {
  width: 100%;
  height: 44px;
  padding: 0 90px 0 42px;
  font-size: 14px;
  font-family: inherit;
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  background: var(--color-bg-muted);
  color: var(--color-text-primary);
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.15s ease, background 0.15s ease;
}

.search-input:focus {
  border-color: var(--color-brand-primary);
  background: var(--color-bg-white);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.search-clear-btn {
  position: absolute;
  right: 85px;
  background: transparent;
  border: none;
  font-size: 18px;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 4px 8px;
  line-height: 1;
}

.search-submit-btn {
  position: absolute;
  right: 5px;
  height: 34px;
  padding: 0 16px;
  font-size: 13px;
  font-weight: 700;
  color: #FFFFFF;
  background: var(--color-brand-primary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s ease;
}

.search-submit-btn:hover {
  background: var(--color-brand-primary-hover, #1D4ED8);
}

/* Filter Pills */
.user-dashboard__pills {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-pill {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid var(--color-border-default);
  background: var(--color-bg-white);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.15s ease;
}

.filter-pill:hover {
  background: var(--color-bg-muted);
  color: var(--color-text-primary);
}

.filter-pill--active {
  background: var(--color-navy-deep, #0B1220) !important;
  color: #FFFFFF !important;
  border-color: var(--color-navy-deep, #0B1220) !important;
}

/* Lots Grid - Responsive and filling full width */
.user-dashboard__lots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 24px;
  width: 100%;
}

.user-dashboard__empty-wrap {
  grid-column: 1 / -1;
  padding: 48px 0;
}

/* Lots Table - High End Full Width Card */
.user-dashboard__lots-table {
  background: var(--color-bg-white);
  border: 1px solid var(--color-border-default);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  width: 100%;
}

.btn-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  border-top-color: #ffffff;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Mobile responsive padding */
@media (max-width: 768px) {
  .user-dashboard {
    padding: 16px 16px 36px 16px;
    gap: 16px;
  }
}

@media (max-width: 640px) {
  .user-dashboard__lots-grid {
    grid-template-columns: 1fr;
  }
}
</style>