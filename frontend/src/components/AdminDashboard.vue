<script>
import AdminNav from './AdminNav.vue';
export default {
    name: 'AdminDashboard',
    mounted() {
        document.title = 'Vehicle Parking App - Admin Dashboard';
        this.fetchParkingLots();
    },
    components: {
        AdminNav
    },
    data() {
        return {
            parking_Lots: [],
            message: ''
        };
    },
    methods: {
        addParkingLot() {
            this.$router.push('/admin/add_lot');
        },
        async fetchParkingLots() {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://localhost:5000/admin/get_lots', {
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
                this.parking_Lots = data.parking_lots;
            } catch (error) {
                console.error('Error fetching parking lots:', error);
            }
        },
        async deleteParkingLot(lotId) {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`http://localhost:5000/admin/delete_lot/${lotId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                const data = await response.json();
                if (!response.ok) {
                    // throw new Error('Network response was not ok');
                    this.message = data.message;
                }
                else {
                    this.message = data.message;
                }
                setTimeout(() => {
                    this.message = '';
                }, 1500); // Clear message after 2 seconds
                this.fetchParkingLots(); // Refresh the list after deletion
            } catch (error) {
                console.error('Error deleting parking lot:', error);
            }
        },
        editParkingLot(lotId) {
            this.$router.push(`/admin/edit_lot/${lotId}`);
        },
        openSpot(spotId) {
            this.$router.push(`/admin/open_spot/${spotId}`);
        }
    }
};
</script>
<template>
    <AdminNav />
    <div class="admin-dashboard container-fluid mt-4 mb-5">
        <div>
            <div class="row justify-content-center mb-4">
                <div class="col-md-11">
                    <div class="border rounded border-secondary px-4 py-2 text-center">
                        <h1 class="text-secondary mb-0">Parking Lots</h1>
                    </div>
                </div>
            </div>

            <div class="row justify-content-center">
                <div class="col-md-10">
                    <div v-if="message" class="alert alert-danger">
                        {{ message }}
                    </div>
                    <div class="row">
                        <div v-for="lot in parking_Lots" :key="lot.id" class="col-md-6 col-lg-4 mb-4">
                            <div class="card border-secondary h-100">
                                <div
                                    class="card-header bg-secondary text-white d-flex  justify-content-between align-items-center">
                                    <div>
                                        <h5 class="mb-0">#{{ lot.id }} {{ lot.name }}</h5>
                                    </div>
                                    <div class="rounded d-flex gap-2" role="group">
                                        <button @click="editParkingLot(lot.id)"
                                            class="btn btn-sm btn-success ">Edit</button>
                                        <button @click="deleteParkingLot(lot.id)"
                                            class="btn btn-sm btn-danger">Delete</button>
                                    </div>
                                </div>
                                <div class="text-center mb-2 mt-2">
                                    <span class="text-muted fs-6">(Occupied: {{ lot.occupied_spots }}/{{ lot.capacity
                                        }})</span>
                                </div>
                                <hr class="my-0 border-2" style="height: 1px; background-color: #dee2e6;" />
                                <!-- </div> -->
                                <!-- <div class="card-body"> -->
                                <div class="d-flex flex-wrap justify-content-center gap-2 p-3 bg-light rounded-bottom">
                                    <div
                                        class="d-flex flex-wrap justify-content-center gap-2 p-3 bg-light rounded-bottom">
                                        <div @click="openSpot(spot.id)" style="cursor: pointer;" v-for="(spot, index) in lot.spots" :key="index"
                                            :class="['spot rounded px-3 py-2 text-white d-flex align-items-center justify-content-center', spot.is_occupied ? 'bg-danger' : 'bg-success']">
                                            {{ spot.is_occupied ? 'O' : 'A' }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="text-center mt-4">
                            <button @click="addParkingLot" class="btn btn-secondary btn-lg px-5 py-3">
                                + Add Parking Lot
                            </button>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>