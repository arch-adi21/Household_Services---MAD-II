export default {
    template: `
    <nav class="navbar navbar-expand-lg bg-black" style="--bs-bg-opacity: .5;">
        <div class="container-fluid">
            <a class="navbar-brand text-primary text-center h1" href="/">
                <img src="/static/images/Service-Hub-Logo.png" alt="Logo" width="30" height="25" class="d-inline-block align-text-top">
                ServiceHub
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link class="nav-link active text-white" v-if="is_login" aria-current="page" to="/">Home</router-link>
                    </li>
                    <li class="nav-item" v-if="role=='admin'">
                        <router-link class="nav-link text-white" to="/users">Users</router-link>
                    </li>
                    <li class="nav-item" v-if="role=='admin'">
                        <router-link class="nav-link text-white" to="/all-service-request">Service Requests</router-link>
                    </li>
                    <li class="nav-item" v-if="role=='customer'">
                        <router-link class="nav-link text-white" to="/service-history">Service History</router-link>
                    </li>
                    <li class="nav-item d-flex align-items-center" v-if="role=='customer'">
                        <input type="text" v-model="searchQuery" placeholder="Search Services" class="form-control search-input">
                        <button class="btn btn-primary search-button" @click="searchServices">Search</button>
                    </li>
                    <li class="nav-item text-end" v-if="active=='false'">
                        <button class="nav-link text-white" @click="logout">Back To Login</button>
                    </li>
                    <li class="nav-item text-end" v-if="is_login && active=='true'">
                        <button class="nav-link text-white" @click="logout">Logout</button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    `,
    data() {
        return {
            role: localStorage.getItem('role'),
            is_login: localStorage.getItem('auth-token'),
            active: localStorage.getItem('active'),
            searchQuery: ''
        }
    },
    methods: {
        logout() {
            localStorage.clear()
            this.$router.push('/login')
        },
        searchServices() {
            this.$router.push({ path: '/search', query: { q: this.searchQuery } })
        }
    },
    style: `
    .search-input {
        margin-right: 10px;
        border-radius: 20px;
        padding: 5px 15px;
        width: 200px;
        transition: width 0.4s ease-in-out;
    }
    .search-input:focus {
        width: 300px;
    }
    .search-button {
        border-radius: 20px;
        padding: 5px 15px;
    }
    `
}