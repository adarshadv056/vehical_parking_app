<script>

export default {
    mounted() {
        document.title = 'Vehicle Parking App - Register';
    },
    data() {
        return {
            formData: {
                email: '',
                password: '',
                username: '',
                address: '',
                pincode: ''
            },
            message: ''
        };
    },
    methods: {
        async registerUser() {
            try {
                const response = await fetch('http://localhost:5000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.formData)
                });
                const data = await response.json();
                console.log(data);
                this.message = data.message;
                setTimeout(() => {
                    this.message = '';
                }, 1000);
            } catch (error) {
                console.error('Registration failed:');
            }
        }
    }
};
</script>
<template>
    <div class="card shadow p-4"
        style="align-items: center; width: 650px;  display: flex; justify-content: center; margin:50px auto;">
        <div>
            <div style="width: 500px;">
                <!-- <h1 class="d-flex justify-content-center text-center">Welcome to Vehicle Parking App</h1> -->
                <h2 class="d-flex justify-content-center">Register</h2>
            </div>
            <div v-if="message" class="alert" :class="{
                        'alert-success': message.includes('successful'),
                        'alert-danger': message.includes('already exists') || message.includes('failed')
                    }">{{ message }}</div>
            <div style="width: 500px;">
                <form @submit.prevent="registerUser">
                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" class="form-control" id="email" v-model="formData.email"
                            placeholder="Enter you email" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" v-model="formData.password"
                            placeholder="Entre your password" required>
                    </div>
                    <div class="mb-3">
                        <label for="username" class="form-label">Fullname</label>
                        <input type="text" class="form-control" id="username" v-model="formData.username"
                            placeholder="Enter your fullname" required>
                    </div>
                    <div class="mb-3">
                        <label for="address" class="form-label">Address</label>
                        <input type="text" class="form-control" id="address" v-model="formData.address"
                            placeholder="Enter your address" required>
                    </div>
                    <div class="mb-3">
                        <label for="pincode" class="form-label">Pin Code</label>
                        <input type="text" class="form-control" id="pincode" v-model="formData.pincode"
                            placeholder="Enter your pin code" required>
                    </div>
                    <div class="mb-3">
                        <button type="submit" class="btn btn-outline-dark w-100">Register</button>
                    </div>
                    <div class="mb-2 d-flex align-items-center justify-content-center">Already have an account?
                        <router-link to="/login" class="ms-3" style="text-decoration: none;" @click="goToLogin">Login
                            here</router-link>
                    </div>
                    
                </form>
            </div>
        </div>
    </div>
</template>