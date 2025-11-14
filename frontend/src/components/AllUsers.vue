<script>
import AdminNav from './AdminNav.vue';
export default {
    name: 'AllUsers',
    components: {
        AdminNav
    },
    mounted() {
        document.title = 'Admin Dashboard- All Users';
        this.fetchUsers();
    },
    data() {
        return {
            message: '',
            users: []
        };
    },
    methods: {
        async fetchUsers() {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://localhost:5000/admin/users', {
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
                this.users = data.users;
            } catch (error) {
                console.error('Error fetching users:', error);
                this.message = 'Failed to load users. Please try again later.';
            }
        }
    }
};
</script>
<template>
    <AdminNav />
    <div class="container-fluid mt-4 mb-5">
        <div>
            <div class="row justify-content-center mb-4">
                <div class="col-md-11">
                    <div class="border rounded border-secondary px-4 py-2 text-center">
                        <h1 class="text-secondary mb-0">Registered Users</h1>
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
                                        <th class="px-4 py-3" scope="col">Full Name</th>
                                        <th class="px-4 py-3" scope="col">Email</th>
                                        <th class="px-4 py-3" scope="col">Address</th>
                                        <th class="px-4 py-3" scope="col">Pin Code</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="user in users" :key="user.id">
                                        <td class="fw-bold text-primary px-4 py-3">{{ user.id }}</td>
                                        <td class="px-4 py-3">
                                            {{ user.username || 'N/A' }}
                                        </td>
                                        <td class="px-4 py-3">
                                            {{ user.email || 'N/A' }}
                                        </td>
                                        <td class="px-4 py-3">
                                            {{ user.address || 'N/A' }}
                                        </td>
                                        <td class="px-4 py-3">
                                            {{ user.pincode || 'N/A' }}
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
.card {
    overflow: hidden;
}
</style>