<script>
import UserNav from './UserNav.vue';
export default {
    name: 'UserDashboard',
    components: {
        UserNav
    },
    data() {
        return {
            searchQuery: '',
            searchedQuery: '',
            parkingLots: [],
            recentHistory: [],
            hasSearched: false,
            message: '',
            userId: ''
        };
    },
    mounted() {
        document.title = 'User Dashboard';
        this.checkForMessage();
        this.fetchParkingHistory();
        const token = localStorage.getItem('token');
        if (token) {
            const payload = JSON.parse(atob(token.split('.')[1]));
            this.userId = payload.user_id;
        }
    },
    methods: {
        async fetchParkingLots() {
            try {
                this.parkingLots = [];
                this.message = '';
                this.loading = true;
                this.hasSearched = false;
                this.searchedQuery = this.searchQuery;
                const token = localStorage.getItem('token');
                const response = await fetch(`http://localhost:5000/user/search_lot?query=${encodeURIComponent(this.searchQuery)}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                this.hasSearched = true;
                const data = await response.json();
                this.parkingLots = data.parking_lots;
            } catch (error) {
                console.error('Error fetching parking lots:', error);
            }
        },
        bookParkingSpot(lotId) {
            this.$router.push(`/user/book_spot?lotId=${lotId}`);
        },
        checkForMessage() {
            const message = localStorage.getItem('message');
            if (message) {
                this.message = message;
                setTimeout(() => {
                    this.message = '';
                    localStorage.removeItem('message');
                }, 1000);
            }
        },
        async fetchParkingHistory() {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://localhost:5000/user/get_history', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                // console.log('Fetching recent history', data);
                this.recentHistory = data.history;
            } catch (error) {
                console.error('Error fetching recent history:', error);
            }
        },
        formatDateTime(dateString) {
            if (!dateString) return 'N/A';
            return new Date(dateString).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
        },
        async parkOut(reservationId) {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`http://localhost:5000/user/park_out/${reservationId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ historyId: reservationId })
                });
                const data = await response.json();
                console.log('Parking out response', data);
                if (response.ok) {
                    this.message = data.message;
                    setTimeout(() => {
                        this.message = '';
                    }, 1000);
                    this.fetchParkingHistory();
                } else {
                    this.message = data.message;
                    setTimeout(() => {
                        this.message = '';
                    }, 1000);
                }
            } catch (error) {
                console.error('Error parking out:', error);
            }
        },
        async exportCSV() {
            const token = localStorage.getItem('token');
            const payload = JSON.parse(atob(token.split('.')[1]));
            const userId = payload.sub;
            try {
                const response = await fetch(`http://localhost:5000/export_csv_result/${userId}`);
                const data = await response.json();
                this.message = 'Preparing download...';

                setTimeout(() => {
                    window.location.href = `http://localhost:5000/csv_download/${data.id}`;
                    this.message = 'Parking data downloaded successfully';
                    setTimeout(() => {
                        this.message = '';
                    }, 2000);
                });

            } catch (error) {
                console.error('Error exporting CSV:', error);
                this.message = 'Something went wrong';
            }
        }
    }
};
</script>
<template>
    <UserNav />
    <div class="container-fluid mt-4 mb-5">
        <div v-if="message" class="alert alert-success mt-3">
            {{ message }}
        </div>
        <div class="row justify-content-center mb-3">
            <div class="col-md-6 d-flex flex-row align-items-center">
                <form @submit.prevent="fetchParkingLots" class="d-flex w-100">
                    <input v-model="searchQuery" type="text" class="form-control border-secondary"
                        placeholder="Search Parking Lot by Location or Pincode" />
                    <button class="btn btn-secondary mx-2" type="submit">Search</button>
                </form>
            </div>
        </div>
        <div v-if="hasSearched">
            <div class="row justify-content-center mb-4">
                <div class="col-md-11">
                    <div class="bg-light border rounded border-secondary px-4 py-2 text-center">
                        <h1 class="text-secondary mb-0">Parking Lots for "{{ searchedQuery }}"</h1>
                    </div>
                </div>
            </div>
            <div class="row justify-content-center rounded">
                <div class="col-md-11 ">
                    <div class="card shadow-sm ">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead class=" ">
                                    <tr>
                                        <th class="px-4 py-3" scope="col">ID</th>
                                        <th class="px-4 py-3" scope="col">Name</th>
                                        <th class="px-4 py-3" scope="col">Address</th>
                                        <th class="px-4 py-3" scope="col">Availability</th>
                                        <th class="px-4 py-3" scope="col">Price</th>
                                        <th class="px-4 py-3" scope="col">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="lot in parkingLots" :key="lot.id">
                                        <td class="fw-bold px-4 py-3">{{ lot.id }}</td>
                                        <td class="fw-bold px-4 py-3">{{ lot.name }}</td>
                                        <td class="px-4 py-3">
                                            {{ lot.location }}
                                        </td>
                                        <td class="px-4 py-3">
                                            {{ lot.total_spots - lot.occupied_spots }}
                                        </td>
                                        <td class="px-4 py-3">
                                            ₹{{ lot.price }} / hour
                                        </td>
                                        <td>
                                            <button @click="bookParkingSpot(lot.id)"
                                                class="btn btn-outline-primary">Park
                                                Now</button>
                                        </td>
                                    </tr>
                                    <tr v-if="parkingLots.length === 0">
                                        <td colspan="6" class="text-center py-4">No parking lots found.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <div class="row justify-content-center mb-4 mt-4">
                <div class="col-md-11">
                    <div
                        class="bg-light border rounded border-secondary px-4 py-2 text-center d-flex justify-content-center align-items-center">
                        <h1 class="text-secondary mb-0">Recent Parking History</h1>
                        <button @click="exportCSV" class="export-btn mx-3">
                            Export Parking Data as CSV
                        </button>
                    </div>
                </div>
            </div>
            <div class="row justify-content-center rounded">
                <div class="col-md-11 ">
                    <div class="card shadow-sm ">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead class=" ">
                                    <tr>
                                        <th class="px-4 py-3" scope="col">ID</th>
                                        <th class="px-4 py-3" scope="col">Lot Name</th>
                                        <th class="px-4 py-3" scope="col">Address</th>
                                        <th class="px-4 py-3" scope="col">Vehicle No</th>
                                        <th class="px-4 py-3" scope="col">Parked Time</th>
                                        <th class="px-4 py-3" scope="col">Leaving Time</th>
                                        <th class="px-4 py-3" scope="col">Total Cost</th>
                                        <th class="px-4 py-3" scope="col">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="history in recentHistory" :key="history.id">
                                        <td class="fw-bold text-primary px-4 py-3">{{ history.id }}</td>
                                        <td class="px-4 py-3">
                                            {{ history.lot_name }}
                                        </td>
                                        <td class="px-4 py-3">
                                            {{ history.location }}
                                        </td>
                                        <td class="px-4 py-3">
                                            {{ history.vehicle_number }}
                                        </td>
                                        <td class="px-4 py-3">
                                            {{ formatDateTime(history.parking_time) }}
                                        </td>
                                        <td class="px-4 py-3">
                                            {{ formatDateTime(history.leaving_time) }}
                                        </td>
                                        <td class="px-4 py-3">
                                            ₹{{ history.parking_cost }}
                                        </td>
                                        <td v-if="history.leaving_time === null">
                                            <button @click="parkOut(history.id)" class="btn btn-outline-danger">Park
                                                Out</button>
                                        </td>
                                        <td v-else>
                                            <button @click="parkOut(history.id)" class="btn btn-outline-success">Parked
                                                Out</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<style scoped>
.export-btn {
    background-color: rgba(var(--bs-secondary-rgb), var(--bs-bg-opacity));
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}

.export-btn:hover {
    background-color: rgba(var(--bs-success-rgb));
}
</style>