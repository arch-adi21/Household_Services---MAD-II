import AdminHome from "./AdminHome.js"
import ProfessionalHome from "./ProfessionalHome.js"
import CustomerHome from "./CustomerHome.js"
import Services from "./Services.js"

export default {
    template: `
    <div class="home-container">
        <div v-if="!is_login" class="login-container d-flex flex-column align-items-center justify-content-center vh-100 text-white">
            <h1 class="mb-4 animate__animated animate__bounceInDown">Welcome to ServiceHub</h1>
            <div class="d-flex flex-column gap-3 animate__animated animate__bounceInUp">
                <router-link to="/customer-signup" class="btn btn-outline-light btn-lg px-4">Register: Customer</router-link>
                <router-link to="/login" class="btn btn-primary btn-lg px-4">Login</router-link>
                <router-link to="/service-professional-signup" class="btn btn-outline-light btn-lg px-4">Register: Professional</router-link>
            </div>
        </div>
         <div v-else>
            <div v-if="active=='false'">
                <h1 class="text-center text-danger">User Not Approved</h1>
            </div>
            <div v-else>
                <AdminHome v-if="userRole=='admin'"/>
                <ProfessionalHome v-if="userRole=='professional'"/>
                <CustomerHome v-if="userRole=='customer'"/>
                <div v-if="userRole=='admin'">
                    <Services v-for="service in services" :service="service" v-bind:key="service.id"/>
                </div>
                <div v-if="userRole=='customer'" class="d-flex flex-row">
                    <Services v-for="service in services" :service="service" v-bind:key="service.id"/>
                </div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            userRole: localStorage.getItem('role'),
            active: localStorage.getItem('active'),
            is_login: localStorage.getItem('auth-token'),
            services: []
        };
    },
    components: {
        AdminHome,
        ProfessionalHome,
        CustomerHome,
        Services
    },
    async mounted() {
        if (this.is_login) {
            try {
                const res = await fetch('/api/services', {
                    headers: {
                        'Authentication-Token': this.is_login
                    }
                });
                const data = await res.json();
                if (res.ok) {
                    console.log('Fetched services:', data);
                    this.services = data;
                } else {
                    console.error('Error fetching services:', data.message);
                }
            } catch (error) {
                console.error('Error fetching services:', error);
            }
        }
    },
};
