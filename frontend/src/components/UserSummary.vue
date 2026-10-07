<script>
import { userApi } from '@/api/client';
import { AppPageHeader, AppCard, AppLoadingState, KpiCard, AppButton } from '@/components/ui';

export default {
  name: 'UserSummary',
  components: { AppPageHeader, AppCard, AppLoadingState, KpiCard, AppButton },
  data() {
    return {
      distributionChartUrl: '',
      loadingChart: true,
      chartError: null,
      history: [],
      loadingHistory: true
    };
  },
  computed: {
    totalSessions() {
      return this.history.length;
    },
    totalSpent() {
      return this.history.reduce((acc, h) => acc + (Number(h.parking_cost) || 0), 0);
    },
    favoriteGarage() {
      if (!this.history.length) return 'None yet';
      const counts = {};
      this.history.forEach(h => {
        const name = h.lot_name || 'Garage';
        counts[name] = (counts[name] || 0) + 1;
      });
      let fav = 'None';
      let maxCount = 0;
      Object.entries(counts).forEach(([name, c]) => {
        if (c > maxCount) {
          maxCount = c;
          fav = name;
        }
      });
      return fav;
    }
  },
  mounted() {
    document.title = 'ParkSync — Driver Analytics';
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.fetchChart();
      this.fetchHistory();
    },
    async fetchChart() {
      try {
        this.loadingChart = true;
        this.chartError = null;
        const { data, error } = await userApi.lotDistributionChart();
        if (error) throw new Error(error.message);
        this.distributionChartUrl = URL.createObjectURL(data);
      } catch (error) {
        console.error('Error fetching distribution chart:', error);
        this.chartError = error.message;
      } finally {
        this.loadingChart = false;
      }
    },
    async fetchHistory() {
      try {
        this.loadingHistory = true;
        const { data, error } = await userApi.getHistory();
        if (error) throw new Error(error.message);
        this.history = data.history || [];
      } catch (error) {
        console.error('Error fetching user history:', error);
      } finally {
        this.loadingHistory = false;
      }
    },
    downloadChart() {
      if (!this.distributionChartUrl) return;
      const a = document.createElement('a');
      a.href = this.distributionChartUrl;
      a.download = 'my_parking_distribution.png';
      a.click();
    }
  }
};
</script>

<template>
  <div class="user-summary-page">
    <AppPageHeader
      title="Driver Analytics &amp; Insights"
      subtitle="Overview of your parking trends, distribution across garages, and expenses"
      :backRoute="{ name: 'UserDashboard' }"
      :actions="[
        { label: 'Download Chart', variant: 'secondary', icon: 'DownloadIcon', onClick: downloadChart, disabled: !distributionChartUrl }
      ]"
    />

    <div class="user-summary__content">
      <!-- KPI Row -->
      <div class="user-summary__kpis">
        <KpiCard
          label="Total Bookings"
          :value="totalSessions"
          suffix="sessions"
          subtext="Lifetime mobility trips"
          icon="CarIcon"
        />
        <KpiCard
          label="Total Expenses"
          :value="totalSpent"
          prefix="₹"
          subtext="Total parking fees settled"
          variant="primary"
          icon="ChartIcon"
        />
        <KpiCard
          label="Top Frequented Garage"
          :value="favoriteGarage"
          subtext="Highest parking frequency"
          icon="MapPinIcon"
        />
      </div>

      <!-- Chart Card Frame -->
      <AppCard class="user-summary__chart-card">
        <template #header>
          <div class="user-summary__chart-header">
            <div>
              <h2 class="user-summary__chart-title">Parking Lot Distribution</h2>
              <p class="user-summary__chart-desc">Breakdown of your parking sessions across city facilities</p>
            </div>
            <AppButton variant="secondary" size="sm" icon="DownloadIcon" @click="downloadChart" :disabled="!distributionChartUrl">
              Save Chart
            </AppButton>
          </div>
        </template>

        <div v-if="loadingChart" class="user-summary__loading">
          <AppLoadingState type="pulse" text="Generating analytics chart..." />
        </div>

        <div v-else-if="chartError" class="user-summary__error">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <p>Failed to generate distribution chart: {{ chartError }}</p>
          <AppButton variant="secondary" size="sm" @click="fetchChart">Retry</AppButton>
        </div>

        <div v-else class="user-summary__chart-wrap">
          <img :src="distributionChartUrl" alt="Parking Distribution Chart" class="user-summary__chart-img" />
        </div>
      </AppCard>
    </div>
  </div>
</template>

<style scoped>
.user-summary-page {
  width: 100%;
  max-width: 100%;
  padding: 24px 32px 48px 32px;
  box-sizing: border-box;
}

.user-summary__content {
  display: flex;
  flex-direction: column;
  gap: var(--space-6, 24px);
  margin-top: var(--space-6, 24px);
}

.user-summary__kpis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-4, 16px);
}

.user-summary__chart-card {
  width: 100%;
}

.user-summary__chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.user-summary__chart-title {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

.user-summary__chart-desc {
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--color-text-secondary, #64748B);
}

.user-summary__loading,
.user-summary__error {
  min-height: 320px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: var(--space-8, 32px);
}

.user-summary__error {
  color: var(--color-status-occupied, #EF4444);
}

.user-summary__chart-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4, 16px);
  background: var(--color-bg-muted, #F8FAFC);
  border-radius: var(--radius-md, 12px);
}

.user-summary__chart-img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
}

@media (max-width: 768px) {
  .user-summary-page {
    padding: 16px 16px 36px 16px;
  }
}

@media (max-width: 640px) {
  .user-summary__kpis {
    grid-template-columns: 1fr;
  }
}
</style>