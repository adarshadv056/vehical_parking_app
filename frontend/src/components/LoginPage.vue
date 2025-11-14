<script>
export default {
    mounted() {
        document.title = 'Vehicle Parking App - Login';
        this.clearLocalStorage();
    },
    data() {
        return {
            formData: {
                email: '',
                password: ''
            },
            message: ''
        };
    },
    methods: {
        clearLocalStorage() {
            localStorage.clear();
        },
        async loginUser() {
            this.clearLocalStorage();
            try {
                const response = await fetch('http://127.0.0.1:5000/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.formData)
                });
                const data = await response.json();
                if (response.ok) {
                    localStorage.setItem('token', data.access_token);
                    const tokenParts = data.access_token.split('.');
                    const payload = JSON.parse(atob(tokenParts[1]));
                    const userRole = payload.role;
                    if (userRole === 'admin') {
                        this.$router.push('/admin');
                    } else if (userRole === 'user') {
                        this.$router.push('/user');
                    } else {
                        this.message = 'Invalid credentials';
                    }
                } else {
                    this.message = data.message
                }

            } catch (error) {
                this.message = 'Login failed';
            }
        }
    }
};
</script>
<template>
    <div class="card shadow p-5 round"
        style="align-items: center; width: 650px;  display: flex; justify-content: center; margin:0 auto;margin-top: 100px;">
        <div>
            <div style="width: 500px;">
                <!-- <h1 class="d-flex justify-content-center text-center" >Welcome to Vehicle Parking App</h1> -->
                <h2 class="d-flex justify-content-center">Login</h2>
            </div>
            <div style="width: 500px; ">
                <form @submit.prevent="loginUser">
                    <div class="mb-3">
                        <label class="form-label me-2" for="email">Email:</label>
                        <input type="email" class="form-control" id="email" v-model="formData.email"
                            placeholder="Enter your email" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="password">Password:</label>
                        <input type="password" class="form-control" id="password" v-model="formData.password"
                            placeholder="Enter your password" required>
                    </div>
                    <div class="mb-3">
                        <input type="submit" class="btn btn-outline-dark w-100" value="Login">
                    </div>
                    <div class="mb-2 d-flex align-items-center justify-content-center">
                        New user? <router-link to="/register" class="ms-3 pointer"
                            style="text-decoration: none;">Register here</router-link>
                    </div>
                    <div v-if="message" class="alert alert-danger mt-3">
                        {{ message }}
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>