<script>
export default {
    methods: {
        goToHome() {
            this.$router.push('/admin');
        },
        goToUsers() {
            this.$router.push('/admin/users');
        },
        // goToSearch() {
        //     this.$router.push('/search');
        // },
        goToSummary() {
            this.$router.push('/admin/summary');
        },
        logout() {
            localStorage.removeItem('token');
            this.$router.push('/login');
        }
    }
}
</script>
<template>
    <nav class="navbar navbar-expand-lg bg-secondary mx-2 mt-2 rounded ">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
            aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <a class="navbar-brand navname text-light" @click="goToHome">Vehicle Parking App</a>
                <ul class="navbar-nav mx-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link  text-light" aria-current="page" @click="goToHome">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link  text-light" aria-current="page" @click="goToUsers">Users</a>
                    </li>
                    <!-- <li class="nav-item">
                        <a class="nav-link  text-light" aria-current="page" @click="goToSearch">Search</a>
                    </li> -->
                    <li class="nav-item">
                        <a class="nav-link  text-light" aria-current="page" @click="goToSummary">Summary</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link  text-danger-emphasis" aria-current="page" @click="logout">Logout</a>
                    </li>
                </ul>
                <a class="navbar-brand navname text-light" @click="goToHome">Welcome Admin</a>
            </div>
        </div>
    </nav>
</template>
<style scoped>
.navname {
    font-weight: bold;
    margin: 0;
    cursor: pointer;
}

/* .router-link-active {
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    font-weight: bold;
} */

.nav-link{
    cursor: pointer;
}

.nav-link:hover {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

.text-decoration-none {
    text-decoration: none !important;
}
</style>