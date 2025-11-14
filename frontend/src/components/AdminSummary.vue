<script>
import AdminNav from './AdminNav.vue';
export default {
  name: 'AdminSummary',
  components: {
    AdminNav
  },
  data() {
    return {
      revenueChartUrl: '',
      // statusChartUrl: ''
    };
  },
  mounted() {
    this.revenueChartUrl = 'http://localhost:5000/admin/revenue_chart';
    // this.statusChartUrl = 'http://localhost:5000/admin/spot_status_chart';
  }
};
</script>

<template>
  <AdminNav />
  <div class="container-fluid mt-4 mb-5">
    <h1 class="text-center">Admin Summary</h1>

    <div class="row">
      <div class="text-center">
        <!-- <h3>Revenue by Parking Lot</h3> -->
        <img :src="revenueChartUrl" alt="Revenue Chart" class="img-fluid" />
      </div>
      <!-- <div class="col-md-6 text-center">
        <h3>Parking Spot Status</h3>
        <img :src="statusChartUrl" alt="Spot Status Chart" class="img-fluid" />
      </div> -->
    </div>
  </div>
</template>
