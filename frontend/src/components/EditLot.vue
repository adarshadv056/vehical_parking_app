<script>

export default {
    name: 'EditLot',
    data() {
        return {
            formData: {
                name: '',
                location: '',
                pincode: '',
                price: '',
                capacity: ''
            },
            originalData: {},
            message: ''
        };
    },
    async mounted() {
        document.title = "Edit Parking Lot";
        await this.fetchParkingLot();
    },
    methods: {
        goBack() {
            this.$router.push('/admin');
        },
        async fetchParkingLot() {
            try {
                const token = localStorage.getItem('token');
                const lotId = this.$route.params.id;
                const response = await fetch(`http://localhost:5000/admin/get_lot/${lotId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    this.formData = {
                        name: data.parking_lot.name,
                        location: data.parking_lot.location,
                        pincode: data.parking_lot.pincode,
                        price: data.parking_lot.price,
                        capacity: data.parking_lot.capacity
                    };
                    this.originalData = { ...this.formData };
                } else {
                    console.error('Failed to fetch parking lot:', response.status);
                }
            } catch (error) {
                console.error('Error fetching parking lot:', error);
            }
        },
        async editParkingLot() {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    this.$router.push('/login')
                    return;
                }

                const response = await fetch(`http://localhost:5000/admin/edit_lot/${this.$route.params.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(this.formData)
                });

                if (response.ok) {
                    this.$router.push('/admin');
                }
                else {
                    const data = await response.json();
                    // this.$router.push('/admin');
                    this.message = data.message || 'Failed to update parking lot';
                }
                setTimeout(() => {
                    this.message = '';
                }, 2000);
            } catch (error) {
                console.error('Error updating parking lot:', error);
            }
        }
    }
};
</script>
<template>
    <div class="container-fluid justify-content-center align-items-center border  rounded shadow p-4 mt-4  "
        style="width: 500px;">
        <div class="row justify-content-center mb-4 ">
            <div class="col-md-12">
                <div class="bg-secondary border rounded border-secondary px-3 py-1 text-center  ">
                    <h3 class="text-light  mb-0">Edit Parking Lots</h3>
                </div>
            </div>
        </div>
        <div v-if="message" class="alert alert-danger">
            {{ message }}
        </div>
        <div class="container">
            <form @submit.prevent="editParkingLot">
                <div class="mb-3">
                    <label for="name" class="form-label">Parking Lot Name:</label>
                    <input type="text" class="form-control" id="name" v-model="formData.name"
                        placeholder="Enter parking lot name" required>
                </div>
                <div class="mb-3">
                    <label for="address" class="form-label">Parking Lot Address:</label>
                    <textarea class="form-control" id="address" v-model="formData.location"
                        placeholder="Enter parking lot address" required></textarea>
                </div>
                <div class="mb-3">
                    <label for="pin" class="form-label">Parking Lot Pin code:</label>
                    <input type="text" class="form-control" id="pin" v-model="formData.pincode"
                        placeholder="Enter parking lot pin code" required>
                </div>
                <div class="mb-3">
                    <label for="price" class="form-label">Price(per hour):</label>
                    <input type="number" class="form-control" id="price" v-model="formData.price"
                        placeholder="Enter parking lot price" required>
                </div>
                <div class="mb-3">
                    <label for="max-spots" class="form-label">Maximum Spots:</label>
                    <input type="number" class="form-control" id="max-spots" v-model="formData.capacity"
                        placeholder="Enter maximum spots" required>
                </div>
                <div class="mt-4 gap-2 d-flex justify-content-center">
                    <button class="btn btn-outline-success px-4" type="submit">Update</button>
                    <button class="btn btn-outline-danger" type="button" @click="goBack">Cancel</button>
                </div>
            </form>
        </div>
    </div>
</template>
