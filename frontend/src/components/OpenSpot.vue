<script>

export default {
    name: 'OpenSpot',
    mounted() {
        document.title = "Vehicle Parking App - View/Delete Parking Spot";
        this.fetchSpotDetails();
    },
    data() {
        return {
            spotData: {
                id: '',
                status: ''
            },
            formData: {
                id: '',
                status: ''
            },
            message: ''
        };
    },
    methods: {
        goBack() {
            this.$router.push('/admin');
        },
        async fetchSpotDetails() {
            try {
                const token = localStorage.getItem('token');
                const spotId = this.$route.params.spotId;
                const response = await fetch(`http://localhost:5000/admin/get_spot/${spotId}`, {
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
                this.formData = {
                    id: data.spot.id,
                    status: data.spot.is_occupied ? 'Occupied' : 'Available'
                };
            } catch (error) {
                console.error('Error fetching spot details:', error);
            }
        },
        async deleteParkingSpot() {
            if (this.formData.status === 'Occupied') {
                this.message = 'Cannot delete an occupied spot';
                setTimeout(() => {
                    this.message = '';
                }, 1000);
                return;
            }
            try {
                this.message = '';
                const token = localStorage.getItem('token');
                const spotId = this.$route.params.spotId;
                const response = await fetch(`http://localhost:5000/admin/delete_spot/${spotId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                const data = await response.json();
                if (!response.ok) {
                    this.message = data.message
                }
                this.$router.push('/admin');
            } catch (error) {
                console.error('Error deleting parking spot:', error);
            }
        },
        openSpotDetails() {
            this.$router.push(`/admin/spot_details/${this.formData.id}`);
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
                    <h3 class="text-light  mb-0">View/Delete Parking Spot</h3>
                </div>
            </div>
        </div>
        <div class="container">
            <div v-if="message" class="alert alert-danger mt-3">
                {{ message }}
            </div>
            <form @submit.prevent="deleteParkingSpot">
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="card border-0 bg-light">
                            <div class="card-body p-3">
                                <div class="row mb-3">
                                    <div class="col-4">
                                        <strong class="text-muted">Spot ID:</strong>
                                    </div>
                                    <div class="col-8">
                                        <span class="fw-bold">{{ formData.id }}</span>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-4">
                                        <strong class="text-muted">Status:</strong>
                                    </div>
                                    <div class="col-8">
                                        <button :disabled="formData.status !== 'Occupied'"
                                            @click="formData.status === 'Occupied' && openSpotDetails()" :class="[ 'btn','fw-bold',
                                                formData.status === 'Occupied' ? 'text-danger' : 'text-success']"
                                            :style="{ cursor: formData.status === 'Occupied' ? 'pointer' : 'not-allowed' }">
                                            {{ formData.status }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="mt-4 gap-2 d-flex justify-content-center">
                    <button class="btn btn-outline-danger" type="submit" @click="deleteParkingSpot">Delete</button>
                    <button class="btn btn-outline-success" type="button" @click="goBack">Cancel</button>
                </div>
            </form>
        </div>
    </div>
</template>