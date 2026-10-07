<script>
import { userApi, auth } from '@/api/client';
import { AppPageHeader, AppCard, AppButton, AppDataTable, AppEmptyState, ActiveSessionCard, KpiCard } from '@/components/ui';

export default {
  name: 'UserHistory',
  components: {
    AppPageHeader,
    AppCard,
    AppButton,
    AppDataTable,
    AppEmptyState,
    ActiveSessionCard,
    KpiCard
  },
  data() {
    return {
      history: [],
      searchQuery: '',
      filterStatus: 'all', // 'all' | 'completed' | 'active'
      loading: true,
      parkingOutLoading: false,
      exportingCSV: false,
      message: '',
      messageType: 'info',
      userId: '',
      columns: [
        {
          key: 'facility',
          label: 'Parking Facility',
          render: (i) => ({
            type: 'custom',
            html: `
              <div style="display: flex; flex-direction: column; gap: 2px;">
                <span style="font-weight: 700; color: var(--color-text-primary, #111827); font-size: 14px;">${i.lot_name || 'Downtown Facility'}</span>
                <span style="font-size: 12px; color: var(--color-text-secondary, #64748B); display: flex; align-items: center; gap: 4px;">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                  ${i.location || 'Metropolitan Hub'} &bull; Bay #${i.spot_id || '1'}
                </span>
              </div>
            `
          })
        },
        {
          key: 'vehicle',
          label: 'Vehicle Plate',
          render: (i) => ({
            type: 'custom',
            html: `
              <span style="display: inline-flex; align-items: center; gap: 5px; font-family: monospace; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 6px; background: #0B1220; color: #F8FAFC; border: 1.5px solid #CBD5E1; letter-spacing: 0.05em;">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #3B82F6;"></span>
                ${i.vehicle_number || 'VEH-0000'}
              </span>
            `
          })
        },
        {
          key: 'check_in',
          label: 'Check In',
          render: (i) => ({
            type: 'custom',
            html: `
              <div style="display: flex; flex-direction: column;">
                <span style="font-size: 13px; font-weight: 600; color: var(--color-text-primary);">${this.formatDate(i.parking_time)}</span>
                <span style="font-size: 11px; color: var(--color-text-secondary);">${this.formatTime(i.parking_time)}</span>
              </div>
            `
          })
        },
        {
          key: 'check_out',
          label: 'Check Out',
          render: (i) => {
            if (!i.leaving_time) {
              return {
                type: 'custom',
                html: `
                  <span style="display: inline-flex; align-items: center; gap: 5px; font-size: 12px; font-weight: 700; color: #16A34A; background: #DCFCE7; padding: 4px 8px; border-radius: 6px;">
                    <span style="width: 6px; height: 6px; border-radius: 50%; background: #16A34A; animation: pulse 1.5s infinite;"></span>
                    Active Now
                  </span>
                `
              };
            }
            return {
              type: 'custom',
              html: `
                <div style="display: flex; flex-direction: column;">
                  <span style="font-size: 13px; font-weight: 600; color: var(--color-text-primary);">${this.formatDate(i.leaving_time)}</span>
                  <span style="font-size: 11px; color: var(--color-text-secondary);">${this.formatTime(i.leaving_time)}</span>
                </div>
              `
            };
          }
        },
        {
          key: 'cost',
          label: 'Amount Paid',
          width: '120px',
          render: (i) => ({
            type: 'custom',
            html: `
              <span style="font-size: 15px; font-weight: 800; color: var(--color-text-primary, #111827);">
                ₹${i.parking_cost || 0}
              </span>
            `
          })
        },
        {
          key: 'action',
          label: 'Status / Action',
          width: '150px',
          render: (i) => {
            if (!i.leaving_time) {
              return {
                type: 'button',
                label: 'Park Out',
                variant: 'danger',
                size: 'sm',
                onClick: () => this.parkOut(i.id)
              };
            }
            return {
              type: 'custom',
              html: `
                <span style="display: inline-flex; align-items: center; gap: 4px; font-size: 12px; font-weight: 700; color: #2563EB; background: #EAF2FF; padding: 4px 10px; border-radius: 999px;">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                  Completed
                </span>
              `
            };
          }
        }
      ]
    };
  },
  computed: {
    activeSession() {
      return this.history.find(h => !h.leaving_time) || null;
    },
    completedSessions() {
      return this.history.filter(h => h.leaving_time);
    },
    totalSpent() {
      return this.history.reduce((acc, h) => acc + (Number(h.parking_cost) || 0), 0);
    },
    filteredHistory() {
      let result = [...this.history];
      if (this.filterStatus === 'completed') {
        result = result.filter(h => !!h.leaving_time);
      } else if (this.filterStatus === 'active') {
        result = result.filter(h => !h.leaving_time);
      }
      if (this.searchQuery.trim()) {
        const q = this.searchQuery.toLowerCase();
        result = result.filter(h =>
          (h.lot_name && h.lot_name.toLowerCase().includes(q)) ||
          (h.location && h.location.toLowerCase().includes(q)) ||
          (h.vehicle_number && h.vehicle_number.toLowerCase().includes(q))
        );
      }
      return result;
    }
  },
  mounted() {
    document.title = 'ParkSync — Parking History & Receipts';
    const payload = auth.getPayload();
    this.userId = payload?.sub;
    this.fetchHistory();
  },
  methods: {
    async fetchHistory() {
      try {
        this.loading = true;
        const { data, error } = await userApi.getHistory();
        if (error) throw new Error(error.message);
        this.history = (data.history || []).sort((a, b) => new Date(b.parking_time) - new Date(a.parking_time));
      } catch (error) {
        console.error('Error fetching parking history:', error);
        this.showMessage('Failed to load parking history', 'error');
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return '—';
      return new Date(dateStr).toLocaleDateString('en-IN', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    },
    formatTime(dateStr) {
      if (!dateStr) return '—';
      return new Date(dateStr).toLocaleTimeString('en-IN', {
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    async parkOut(reservationId) {
      try {
        this.parkingOutLoading = true;
        const { data, error } = await userApi.parkOut(reservationId);
        if (error) throw new Error(error.message);
        this.showMessage(data?.message || 'Checked out successfully!', 'success');
        await this.fetchHistory();
      } catch (error) {
        console.error('Error parking out:', error);
        this.showMessage(error.message || 'Error checking out', 'error');
      } finally {
        this.parkingOutLoading = false;
      }
    },
    async exportCSV() {
      try {
        this.exportingCSV = true;
        this.showMessage('Generating official CSV receipt report...', 'info');
        const { data, error } = await userApi.exportCSV(this.userId);
        if (error) throw new Error(error.message);
        const { data: blob } = await userApi.downloadCSV(data.filename);
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = data.filename || 'parking_receipts_report.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        this.showMessage('Receipt report downloaded successfully!', 'success');
      } catch (error) {
        console.error('Error exporting CSV:', error);
        this.showMessage('Failed to export CSV report', 'error');
      } finally {
        this.exportingCSV = false;
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
  <div class="user-history">
    <AppPageHeader
      title="Parking History &amp; Receipts"
      subtitle="Review past parking sessions, check-in timestamps, tariffs paid, and export reports"
      :actions="[
        { label: exportingCSV ? 'Exporting...' : 'Export History (CSV)', variant: 'primary', icon: 'DownloadIcon', onClick: exportCSV, disabled: exportingCSV },
        { label: 'Find Parking', variant: 'secondary', icon: 'SearchIcon', onClick: () => $router.push('/user') }
      ]"
    />

    <!-- Toast Banner -->
    <transition name="fade">
      <div v-if="message" class="user-history__alert" :class="`user-history__alert--${messageType}`">
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

    <div class="user-history__content">
      <!-- KPI Row -->
      <section class="user-history__kpi-grid">
        <KpiCard
          label="Total Expended"
          :value="totalSpent"
          prefix="₹"
          subtext="Cumulative parking tariff"
          icon="ChartIcon"
        />
        <KpiCard
          label="Completed Sessions"
          :value="completedSessions.length"
          suffix="receipts"
          subtext="Past checked-out sessions"
          icon="CheckCircleIcon"
        />
        <KpiCard
          label="Active Parking"
          :value="activeSession ? 1 : 0"
          suffix="live"
          :subtext="activeSession ? `Bay #${activeSession.spot_id}` : 'No active vehicle'"
          :variant="activeSession ? 'success' : 'default'"
          icon="CarIcon"
        />
      </section>

      <!-- Active Session Banner if Car is Parked -->
      <section v-if="activeSession" class="user-history__active-banner">
        <ActiveSessionCard
          :session="activeSession"
          :loading="parkingOutLoading"
          @park-out="parkOut"
        />
      </section>

      <!-- Main History Card & Table -->
      <section class="user-history__table-card">
        <AppCard>
          <template #header>
            <div class="user-history__card-header">
              <div class="user-history__filter-row">
                <!-- Search Filter Input -->
                <div class="user-history__search-wrap">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                  </svg>
                  <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Filter by garage, city, or plate..."
                    class="user-history__search-input"
                  />
                  <button
                    v-if="searchQuery"
                    type="button"
                    class="user-history__clear-btn"
                    @click="searchQuery = ''"
                  >
                    &times;
                  </button>
                </div>

                <!-- Status Filter Pills -->
                <div class="user-history__status-pills">
                  <button
                    type="button"
                    class="status-pill"
                    :class="{ 'status-pill--active': filterStatus === 'all' }"
                    @click="filterStatus = 'all'"
                  >
                    All ({{ history.length }})
                  </button>
                  <button
                    type="button"
                    class="status-pill"
                    :class="{ 'status-pill--active': filterStatus === 'completed' }"
                    @click="filterStatus = 'completed'"
                  >
                    Completed ({{ completedSessions.length }})
                  </button>
                  <button
                    type="button"
                    class="status-pill"
                    :class="{ 'status-pill--active': filterStatus === 'active' }"
                    @click="filterStatus = 'active'"
                  >
                    Active ({{ activeSession ? 1 : 0 }})
                  </button>
                </div>
              </div>

              <!-- Export Button inside Header -->
              <div class="user-history__export-action">
                <AppButton
                  variant="secondary"
                  size="sm"
                  icon="DownloadIcon"
                  :disabled="exportingCSV || history.length === 0"
                  @click="exportCSV"
                >
                  Download CSV
                </AppButton>
              </div>
            </div>
          </template>

          <!-- Table View -->
          <AppDataTable
            :columns="columns"
            :items="filteredHistory"
            :loading="loading"
            emptyMessage="No parking sessions found matching your criteria"
            emptyIcon="InboxIcon"
            :showPagination="filteredHistory.length > 8"
            :pageSize="8"
          />
        </AppCard>
      </section>

      <!-- Empty State if User Has Never Parked -->
      <div v-if="!loading && history.length === 0" class="user-history__empty">
        <AppEmptyState
          icon="CarIcon"
          title="No parking records found"
          description="You haven't reserved any parking bays yet. Find a garage near you and book your first spot!"
          :action="{ label: 'Find Parking', onClick: () => $router.push('/user'), variant: 'primary' }"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.user-history {
  width: 100%;
  max-width: 100%;
  padding: 24px 32px 48px 32px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.user-history__content {
  display: flex;
  flex-direction: column;
  gap: var(--space-6, 24px);
}

/* Alert Notification */
.user-history__alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  border-radius: var(--radius-md, 12px);
  font-size: 14px;
  font-weight: 600;
}

.user-history__alert--success {
  background: var(--color-status-available-bg, #DCFCE7);
  color: var(--color-status-available, #16A34A);
  border: 1px solid var(--color-status-available, #16A34A);
}

.user-history__alert--error {
  background: var(--color-status-occupied-bg, #FEE2E2);
  color: var(--color-status-occupied, #EF4444);
  border: 1px solid var(--color-status-occupied, #EF4444);
}

.user-history__alert--info {
  background: var(--color-status-info-bg, #EAF2FF);
  color: var(--color-brand-primary, #2563EB);
  border: 1px solid var(--color-brand-primary, #2563EB);
}

/* KPI Row */
.user-history__kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--space-4, 16px);
}

/* Card Header & Filters */
.user-history__card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  width: 100%;
}

.user-history__filter-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  flex: 1;
}

.user-history__search-wrap {
  position: relative;
  display: flex;
  align-items: center;
  min-width: 260px;
}

.user-history__search-wrap svg {
  position: absolute;
  left: 12px;
  color: var(--color-text-muted);
}

.user-history__search-input {
  width: 100%;
  padding: 8px 32px 8px 36px;
  font-size: 13px;
  font-family: inherit;
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  background: var(--color-bg-white);
  color: var(--color-text-primary);
  outline: none;
  transition: border-color 0.15s ease;
}

.user-history__search-input:focus {
  border-color: var(--color-brand-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.user-history__clear-btn {
  position: absolute;
  right: 8px;
  background: transparent;
  border: none;
  font-size: 16px;
  color: var(--color-text-muted);
  cursor: pointer;
}

.user-history__status-pills {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-pill {
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid var(--color-border-default);
  background: var(--color-bg-white);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.15s ease;
}

.status-pill:hover {
  background: var(--color-bg-muted);
  color: var(--color-text-primary);
}

.status-pill--active {
  background: var(--color-brand-primary) !important;
  color: #FFFFFF !important;
  border-color: var(--color-brand-primary) !important;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .user-history {
    padding: 16px 16px 36px 16px;
    gap: 16px;
  }
}

@media (max-width: 640px) {
  .user-history__kpi-grid {
    grid-template-columns: 1fr;
  }

  .user-history__search-wrap {
    min-width: 100%;
    width: 100%;
  }

  .user-history__filter-row {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
