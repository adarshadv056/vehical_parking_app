<script>


export default {
    name: 'bookSpot',
    data() {
        return {
            formData: {
                lotId: null,
                spotId: null,
                userId: null,
                vehicleNo: ''
            },
            message: ''
        };
    },
    mounted() {
        document.title = "User - Book Parking Spot";
        const lotId = this.$route.query.lotId;
        this.formData.lotId = lotId;
        this.fetchUserInfo();
        this.fetchAvailableSpot();
    },
    methods: {
        goBack() {
            this.$router.push(`/user`);
        },
        async fetchAvailableSpot() {
            try {
                const response = await fetch(`http://localhost:5000/user/get_first_spot/${this.formData.lotId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch spot details');
                }
                const data = await response.json();
                this.formData.spotId = data.parking_spot.id;
            } catch (error) {
                console.error('Error fetching spot details:', error);
                this.message = 'Error fetching spot details. Please try again later.';
            }
        },
        async fetchUserInfo() {
            const token = localStorage.getItem('token');
            if (token) {
                const payload = JSON.parse(atob(token.split('.')[1]));
                this.formData.userId = payload.id || payload.sub || payload.user_id || payload.userId;
            }
        },
        async bookParkingSpot(spotId) {
            try {
                const response = await fetch(`http://localhost:5000/user/book_spot/${spotId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: JSON.stringify({
                        lotId: this.formData.lotId,
                        spotId: spotId,
                        userId: this.formData.userId,
                        vehicleNo: this.formData.vehicleNo.trim()
                    })
                });
                const data = await response.json();
                if (response.ok) {
                    localStorage.setItem('message', data.message);
                    this.$router.push('/user');
                } else {
                    this.message = data.message || 'Failed to book parking spot. Please try again.';
                    setTimeout(() => {
                        this.message = '';
                    }, 1000);
                }
            } catch (error) {
                console.error('Error booking parking spot:', error);
                this.message = 'No Spots Available. Please try again later.';
                setTimeout(() => {
                    this.message = '';
                }, 1000);
            }
        }
    },


};
</script>
<template>
    <div class="container-fluid justify-content-center align-items-center border  rounded shadow p-4 mt-4"
        style="width: 500px; margin-top: 80px !important;">
        <div class="row justify-content-center mb-4 ">
            <div class="col-md-12">
                <div class="bg-secondary border rounded border-secondary px-3 py-1 text-center">
                    <h3 class="text-light  mb-0">Book Parking Spot</h3>
                </div>
            </div>
        </div>
        <div v-if="message" class="alert alert-danger mt-3">
            {{ message }}
        </div>
        <div class="container">
            <form @submit.prevent="bookParkingSpot(formData.spotId)">
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="card border-0 bg-light">
                            <div class="card-body p-3">
                                <div class="row mb-3">
                                    <div class="col-5">
                                        <strong class="text-muted">Spot ID:</strong>
                                    </div>
                                    <div class="col-7">
                                        <span class="fs-5 fw-bold text-primary">{{ formData.spotId }}</span>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-5">
                                        <strong class="text-muted">Lot ID:</strong>
                                    </div>
                                    <div class="col-7">
                                        <span class="fs-5 fw-bold text-primary">{{ formData.lotId }}</span>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-5">
                                        <strong class="text-muted">User ID:</strong>
                                    </div>
                                    <div class="col-7">
                                        <span class="fs-5 fw-bold text-primary">{{ formData.userId }}</span>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-5">
                                        <strong class="text-muted">Vehicle No:</strong>
                                    </div>
                                    <div class="col-7">
                                        <input type="text" v-model="formData.vehicleNo"
                                            class="form-control  text-primary" placeholder="Enter Vehicle No" required>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="mt-4 gap-2 d-flex justify-content-center">
                    <button class="btn btn-outline-success" type="submit">Reserve</button>
                    <button class="btn btn-outline-danger" type="button" @click="goBack">Cancel</button>
                </div>
            </form>
        </div>
    </div>
</template>