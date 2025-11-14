<script>
import UserNav from './UserNav.vue';

export default {
    name: 'UserSummary',
    components: {
        UserNav
    },
    data() {
        return {
            //   revenueChartUrl: 'http://localhost:5000/user/revenue_chart',
            distributionChartUrl: ''
        };
    },
    mounted() {
        document.title = 'User Summary';
        this.fetchDistributionChart();
    },
    methods: {
        async fetchDistributionChart() {
            try {
                const response = await fetch('http://localhost:5000/user/lot_distribution_chart', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const blob = await response.blob();
                this.distributionChartUrl = URL.createObjectURL(blob);
            } catch (error) {
                console.error('Error fetching distribution chart:', error);
            }
        }
    },
};
</script>
<template>
    <UserNav />
    <div class="container-fluid mt-4 mb-5">
        <h1 class="text-center mb-4">User Summary</h1>

        <div class="row">
            <!-- <div class="col-md-6 text-center">
        <h4>Spending by Parking Lot</h4>
        <img :src="revenueChartUrl" alt="Revenue Chart" class="img-fluid" />
      </div> -->
            <div class="text-center">
                <!-- <h4>Most Parked Lots</h4> -->
                <img :src="distributionChartUrl" alt="Distribution Chart" class="img-fluid" />
            </div>
        </div>
    </div>
</template>
