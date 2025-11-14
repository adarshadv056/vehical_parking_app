<script>
export default {
    name: 'HomePage',
    methods: {
        goToLogin() {
            this.$router.push('/login');
        }
    }
}
</script>

<template>
    <div class="card shadow home">
        <h1 class="heading">Welcome to the Parking Management System</h1>
        <button class="btn btn-outline-secondary w-25" style="width: 25%; margin-left: auto; margin-right: auto;" @click="goToLogin">Login</button>
    </div>
</template>


<style>
.home {
    text-align: center;
    margin: 220px auto;
    width: 50%;
    padding: 30px;
    border: 1px solid black;
}
.heading {
    margin-bottom: 20px;
}
</style>