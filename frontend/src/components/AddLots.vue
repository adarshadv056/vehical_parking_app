<script>

export default {
    name: 'AddLots',
    data() {
        return {
            formData: {
                name: '',
                location: '',
                pincode: '',
                price: '',
                capacity: ''
            },
            message: ''
        };
    },
    methods: {
        goBack() {
            this.$router.push('/admin');
        },
        async addParkingLot() {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    this.$router.push('/login')
                    return;
                }

                const response = await fetch('http://localhost:5000/admin/add_lot', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(this.formData)
                });
                const data = await response.json();
                if (response.ok) {
                    this.$router.push('/admin');
                }else{
                    this.message = data.message;
                }
                setTimeout(() => {
                    this.message = '';
                }, 1000);
            } catch (error) {
                console.error('Error:', error);
            }
        }
    },
    mounted() {
        document.title = "Add Parking Lot";
    }
};
</script>
<template>
    <div class="container-fluid justify-content-center align-items-center border  rounded shadow p-4 mt-4  "
        style="width: 500px;">
        <div class="row justify-content-center mb-4 ">
            <div class="col-md-12">
                <div class="bg-secondary border rounded border-secondary px-3 py-1 text-center">
                    <h3 class="text-light  mb-0">New Parking Lots</h3>
                </div>
            </div>
        </div>
        <div v-if="message" class="alert alert-danger mt-3">
            {{ message }}
        </div>
        <div class="container">
            <form @submit.prevent="addParkingLot">
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
                    <button class="btn btn-outline-success px-4" type="submit">Add</button>
                    <button class="btn btn-outline-danger" type="button" @click="goBack">Cancel</button>
                </div>
            </form>
        </div>
    </div>
</template>