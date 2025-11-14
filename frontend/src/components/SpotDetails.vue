<script>

export default {
    name: 'OpenSpot',
    mounted() {
        document.title = "Vehicle Parking App - View/Delete Parking Spot";
        this.fetchReservations();
    },
    data() {
        return {
            formData: {
                spotId: '',
                customerId: '',
                vehicleNo: '',
                parkingTime: '',
                estimatedCost: '',
            }
        };
    },
    methods: {
        goBack() {
            this.$router.push(`/admin/open_spot/${this.formData.spotId}`);
        },
        formatDateTime(dateString) {
            if (!dateString) return 'N/A';
            return new Date(dateString).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
        },
        async fetchReservations() {
            try {
                const token = localStorage.getItem('token');
                const spotId = this.$route.params.spotId;
                const response = await fetch(`http://localhost:5000/admin/get_reservations/${spotId}`, {
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
                console.log('Fetched reservation data:', data);
                const reservation = data.reservation;
                this.formData = {
                    spotId: reservation.spot_id,
                    customerId: reservation.user_id,
                    vehicleNo: reservation.vehicle_number,
                    parkingTime: reservation.parking_time,
                    estimatedCost: reservation.parking_cost
                };
            } catch (error) {
                console.error('Error fetching spot details:', error);
            }
        }
    },

};
</script>
<template>
    <div class="container-fluid justify-content-center align-items-center border  rounded shadow p-4"
        style="width: 500px; margin-top: 125px;">
        <div class="row justify-content-center mb-4 ">
            <div class="col-md-12">
                <div class="bg-secondary border rounded border-secondary px-3 py-1 text-center">
                    <h3 class="text-light  mb-0">Occupied Parking Spot Details</h3>
                </div>
            </div>
        </div>
        <div class="container">
            <form @submit.prevent="deleteParkingSpot">
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="card border-0 bg-light">
                            <div class="card-body p-3">
                                <div class="row mb-3">
                                    <div class="col-5">
                                        <strong class="text-muted">Spot ID:</strong>
                                    </div>
                                    <div class="col-7">
                                        <span>{{ formData.spotId }}</span>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-5">
                                        <strong class="text-muted">Customer ID:</strong>
                                    </div>
                                    <div class="col-7">
                                        <span>{{ formData.customerId }}</span>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-5">
                                        <strong class="text-muted">Vehical No:</strong>
                                    </div>
                                    <div class="col-7">
                                        <span>{{ formData.vehicleNo }}</span>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-5">
                                        <strong class="text-muted">Parking Time:</strong>
                                    </div>
                                    <div class="col-7">
                                        <span>{{ formatDateTime(formData.parkingTime) }}</span>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-5">
                                        <strong class="text-muted">Est Parking Cost:</strong>
                                    </div>
                                    <div class="col-7">
                                        <span>₹{{ formData.estimatedCost }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="mt-4 gap-2 d-flex justify-content-center">
                    <button class="btn btn-outline-success" type="button" @click="goBack">Close</button>
                </div>
            </form>
        </div>
    </div>
</template>