import {
  createRouter,
  createWebHistory
} from 'vue-router';
import HomePage from '../components/HomePage.vue';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import AllUsers from '../components/AllUsers.vue';
import AddLots from '../components/AddLots.vue';
import EditLot from '../components/EditLot.vue';
import OpenSpot from '../components/OpenSpot.vue';
import SpotDetails from '../components/SpotDetails.vue';
import UserDashboard from '../components/UserDashboard.vue';
import BookSpot from '../components/BookSpot.vue';
import AdminSummary from '../components/AdminSummary.vue';
import UserSummary from '../components/UserSummary.vue';

const routes = [{
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: {
      requiresAuth: true,
      role: 'admin'
    }
  },
  {
    path: '/admin/users',
    name: 'AllUsers',
    component: AllUsers,
    meta: {
      requiresAuth: true,
      role: 'admin'
    }
  },
  {
    path: '/admin/add_lot',
    name: 'AddParkingLot',
    component: AddLots,
    meta: {
      requiresAuth: true,
      role: 'admin'
    }
  },
  {
    path: '/admin/edit_lot/:id',
    name: 'EditParkingLot',
    component: EditLot,
    meta: {
      requiresAuth: true,
      role: 'admin'
    }
  },
  {
    path: '/admin/open_spot/:spotId',
    name: 'OpenSpot',
    component: OpenSpot,
    meta: {
      requiresAuth: true,
      role: 'admin'
    }
  },
  {
    path: '/admin/spot_details/:spotId',
    name: 'SpotDetails',
    component: SpotDetails,
    meta: {
      requiresAuth: true,
      role: 'admin'
    }
  },
  {
    path:'/admin/summary',
    name: 'AdminSummary',
    component: AdminSummary,
    meta: {
      requiresAuth: true,
      role: 'admin'
    }
  },
  {
    path: '/user',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: {
      requiresAuth: true,
      role: 'user'
    }
  },
  {
    path: '/user/book_spot',
    name: 'BookSpot',
    component: BookSpot,
    meta: {
      requiresAuth: true,
      role: 'user'
    }
  },
  {
    path: '/user/summary',
    name: 'UserSummary',
    component: UserSummary,
    meta: {
      requiresAuth: true,
      role: 'user'
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (to.meta.requiresAuth && !token) {
    next('/login');
    return;
  }
  if (token && to.meta.role) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const userRole = payload.role;
    if (to.meta.role !== userRole) {
      next('/login');
      return;
    }
  }
  next();
});


export default router;