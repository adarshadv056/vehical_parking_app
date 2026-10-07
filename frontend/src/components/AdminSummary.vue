<script>
import { admin } from '@/api/client';
import { AppPageHeader, AppCard, AppLoadingState, KpiCard, AppButton, AppDataTable } from '@/components/ui';

export default {
  name: 'AdminSummary',
  components: {
    AppPageHeader,
    AppCard,
    AppLoadingState,
    KpiCard,
    AppButton,
    AppDataTable
  },
  data() {
    return {
      revenueChartUrl: '',
      loading: true,
      error: null,
      lots: [],
      tableColumns: [
        {
          key: 'facility',
          label: 'Parking Facility',
          render: (l) => ({
            type: 'custom',
            html: `
              <div style="display: flex; flex-direction: column; gap: 2px;">
                <span style="font-weight: 700; color: var(--color-text-primary, #111827); font-size: 14px;">${l.name}</span>
                <span style="font-size: 12px; color: var(--color-text-secondary, #64748B); display: flex; align-items: center; gap: 4px;">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                  ${l.location} &bull; ID #${l.id}
                </span>
              </div>
            `
          })
        },
        {
          key: 'tariff',
          label: 'Hourly Tariff',
          width: '130px',
          render: (l) => ({
            type: 'custom',
            html: `
              <span style="font-size: 15px; font-weight: 800; color: var(--color-text-primary, #111827);">
                ₹${Number(l.price).toFixed(0)}<span style="font-size: 11px; font-weight: 600; color: var(--color-text-secondary);">/hr</span>
              </span>
            `
          })
        },
        {
          key: 'capacity',
          label: 'Total Bays',
          width: '120px',
          render: (l) => ({
            type: 'custom',
            html: `
              <span style="font-weight: 700; font-size: 13px; color: var(--color-text-primary);">
                ${l.total_spots || l.capacity || 0} stalls
              </span>
            `
          })
        },
        {
          key: 'occupancy',
          label: 'Live Occupancy',
          width: '200px',
          render: (l) => {
            const total = l.total_spots || l.capacity || 10;
            const occupied = l.occupied_spots || 0;
            const pct = Math.min(100, Math.round((occupied / total) * 100));
            const color = pct >= 80 ? '#EF4444' : (pct >= 50 ? '#F59E0B' : '#16A34A');
            return {
              type: 'custom',
              html: `
                <div style="display: flex; flex-direction: column; gap: 5px; width: 100%;">
                  <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: 700;">
                    <span style="color: ${color};">${occupied} occupied</span>
                    <span style="color: var(--color-text-secondary);">${pct}%</span>
                  </div>
                  <div style="height: 5px; background: #E2E8F0; border-radius: 999px; overflow: hidden; width: 100%;">
                    <div style="height: 100%; width: ${pct}%; background: ${color}; border-radius: 999px;"></div>
                  </div>
                </div>
              `
            };
          }
        },
        {
          key: 'status',
          label: 'Demand Status',
          width: '150px',
          render: (l) => {
            const total = l.total_spots || l.capacity || 10;
            const occupied = l.occupied_spots || 0;
            const pct = Math.min(100, Math.round((occupied / total) * 100));
            if (pct >= 75) {
              return {
                type: 'custom',
                html: `<span style="font-size: 11px; font-weight: 700; color: #DC2626; background: #FEE2E2; padding: 3px 8px; border-radius: 999px;">High Demand</span>`
              };
            }
            if (pct >= 30) {
              return {
                type: 'custom',
                html: `<span style="font-size: 11px; font-weight: 700; color: #2563EB; background: #EAF2FF; padding: 3px 8px; border-radius: 999px;">Optimal Flow</span>`
              };
            }
            return {
              type: 'custom',
              html: `<span style="font-size: 11px; font-weight: 700; color: #16A34A; background: #DCFCE7; padding: 3px 8px; border-radius: 999px;">Available Bays</span>`
            };
          }
        }
      ]
    };
  },
  computed: {
    totalCapacity() {
      return this.lots.reduce((acc, l) => acc + (l.total_spots || l.capacity || 0), 0);
    },
    totalOccupied() {
      return this.lots.reduce((acc, l) => acc + (l.occupied_spots || 0), 0);
    },
    networkOccupancyRate() {
      if (!this.totalCapacity) return '0%';
      return `${Math.round((this.totalOccupied / this.totalCapacity) * 100)}%`;
    },
    topFacility() {
      if (!this.lots.length) return 'None';
      const sorted = [...this.lots].sort((a, b) => (b.occupied_spots || 0) - (a.occupied_spots || 0));
      return sorted[0].name;
    }
  },
  async mounted() {
    document.title = 'Revenue & Occupancy Analytics — ParkSync Admin';
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      await Promise.all([this.fetchChart(), this.fetchLots()]);
    },
    async fetchChart() {
      try {
        this.loading = true;
        this.error = null;
        const { data, error } = await admin.revenueChart();
        if (error) throw new Error(error.message);
        this.revenueChartUrl = URL.createObjectURL(data);
      } catch (error) {
        console.error('Error fetching revenue chart:', error);
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
    async fetchLots() {
      try {
        const { data } = await admin.listLots();
        if (data?.parking_lots) this.lots = data.parking_lots;
      } catch (e) {
        console.error('Error fetching lots:', e);
      }
    },
    downloadChart() {
      if (!this.revenueChartUrl) return;
      const a = document.createElement('a');
      a.href = this.revenueChartUrl;
      a.download = 'parksync_revenue_distribution_chart.png';
      a.click();
    }
  }
};
</script>

<template>
  <div class="admin-summary-page">
    <AppPageHeader
      title="Revenue &amp; Occupancy Analytics"
      subtitle="Financial performance, parking demand trends, and real-time facility yield reporting"
      :backRoute="{ name: 'AdminDashboard' }"
      :actions="[
        { label: 'Download Chart (PNG)', variant: 'primary', icon: 'DownloadIcon', onClick: downloadChart, disabled: !revenueChartUrl },
        { label: 'Refresh Data', variant: 'secondary', onClick: fetchData, loading: loading }
      ]"
    />

    <div class="admin-summary__content">
      <!-- KPI Row (4 Full Width Columns) -->
      <section class="admin-summary__kpi-grid">
        <KpiCard
          label="Tracked Facilities"
          :value="lots.length"
          suffix="garages"
          subtext="Reporting revenue metrics"
          variant="dark"
          icon="DashboardIcon"
        />
        <KpiCard
          label="Network Bay Capacity"
          :value="totalCapacity"
          suffix="bays"
          subtext="Total stalls under management"
          variant="primary"
          icon="ZapIcon"
        />
        <KpiCard
          label="Network Occupancy"
          :value="networkOccupancyRate"
          subtext="Real-time vehicle utilization"
          variant="success"
          icon="ShieldIcon"
        />
        <KpiCard
          label="Highest Demand Facility"
          :value="topFacility"
          subtext="Peak parking utilization"
          icon="MapPinIcon"
        />
      </section>

      <!-- Facility Yield Breakdown Table -->
      <section class="admin-summary__table-section">
        <AppCard>
          <template #header>
            <div class="table-card-head">
              <div>
                <h3 class="table-card-head__title">Facility Performance &amp; Tariff Breakdown</h3>
                <p class="table-card-head__desc">Real-time occupancy status, pricing tiers, and capacity distribution</p>
              </div>
              <span class="table-card-head__count">{{ lots.length }} active locations</span>
            </div>
          </template>

          <AppDataTable
            :columns="tableColumns"
            :items="lots"
            :loading="loading && !lots.length"
            emptyMessage="No facilities currently reporting metrics"
            emptyIcon="InboxIcon"
            :showPagination="lots.length > 8"
            :pageSize="8"
          />
        </AppCard>
      </section>

      <!-- Revenue Distribution Chart Frame -->
      <section class="admin-summary__chart-section">
        <AppCard class="admin-summary__chart-card">
          <template #header>
            <div class="admin-summary__chart-header">
              <div class="chart-header-left">
                <div class="chart-icon-box">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                    <line x1="18" y1="20" x2="18" y2="10"/>
                    <line x1="12" y1="20" x2="12" y2="4"/>
                    <line x1="6" y1="20" x2="6" y2="14"/>
                  </svg>
                </div>
                <div>
                  <h2 class="admin-summary__chart-title">Gross Revenue Generated by Parking Facility</h2>
                  <p class="admin-summary__chart-desc">Backend session-aggregated financial yield computed across all completed reservations</p>
                </div>
              </div>
              <AppButton
                variant="secondary"
                size="sm"
                icon="DownloadIcon"
                @click="downloadChart"
                :disabled="!revenueChartUrl"
              >
                Save Chart Image
              </AppButton>
            </div>
          </template>

          <div v-if="loading && !revenueChartUrl" class="admin-summary__loading">
            <AppLoadingState type="pulse" text="Aggregating financial report from database..." />
          </div>

          <div v-else-if="error" class="admin-summary__error">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <p>Failed to generate revenue chart: {{ error }}</p>
            <AppButton variant="secondary" size="sm" @click="fetchChart">Retry Computation</AppButton>
          </div>

          <div v-else class="admin-summary__chart-wrap">
            <img
              :src="revenueChartUrl"
              alt="Revenue by Parking Lot Chart"
              class="admin-summary__chart-image"
            />
          </div>

          <div class="admin-summary__footnote">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="16" x2="12" y2="12"/>
              <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
            <span>
              Financial data is dynamically compiled using Flask, SQLAlchemy reservation records, and Matplotlib. Metrics include all checked-out driver sessions.
            </span>
          </div>
        </AppCard>
      </section>
    </div>
  </div>
</template>

<style scoped>
.admin-summary-page {
  width: 100%;
  max-width: 100%;
  padding: 24px 32px 48px 32px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.admin-summary__content {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* KPI Grid - 4 Columns */
.admin-summary__kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  width: 100%;
}

@media (max-width: 1200px) {
  .admin-summary__kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .admin-summary__kpi-grid {
    grid-template-columns: 1fr;
  }
}

/* Table Section */
.admin-summary__table-section {
  width: 100%;
}

.table-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  flex-wrap: wrap;
  gap: 12px;
}

.table-card-head__title {
  margin: 0;
  font-size: 17px;
  font-weight: 800;
  color: var(--color-text-primary, #111827);
  line-height: 1.2;
}

.table-card-head__desc {
  margin: 3px 0 0 0;
  font-size: 13px;
  color: var(--color-text-secondary, #64748B);
}

.table-card-head__count {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-brand-primary, #2563EB);
  background: var(--color-brand-primary-light, #EAF2FF);
  padding: 3px 10px;
  border-radius: 999px;
}

/* Chart Section */
.admin-summary__chart-section {
  width: 100%;
}

.admin-summary__chart-card {
  width: 100%;
}

.admin-summary__chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  width: 100%;
}

.chart-header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.chart-icon-box {
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

.admin-summary__chart-title {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: var(--color-text-primary, #111827);
  line-height: 1.2;
}

.admin-summary__chart-desc {
  margin: 3px 0 0;
  font-size: 13px;
  color: var(--color-text-secondary, #64748B);
}

.admin-summary__loading,
.admin-summary__error {
  min-height: 380px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 32px;
}

.admin-summary__error {
  color: var(--color-status-occupied, #EF4444);
  text-align: center;
}

.admin-summary__chart-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: var(--color-bg-muted, #F8FAFC);
  border-radius: 12px;
  overflow: hidden;
}

.admin-summary__chart-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.admin-summary__footnote {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--color-text-secondary, #64748B);
  padding-top: 14px;
  border-top: 1px solid var(--color-border-default, #E2E8F0);
  margin-top: 16px;
}

.admin-summary__footnote svg {
  color: var(--color-text-muted, #94A3B8);
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .admin-summary-page {
    padding: 16px 16px 36px 16px;
    gap: 16px;
  }
}
</style>