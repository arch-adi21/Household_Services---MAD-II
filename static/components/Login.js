export default{
    template: `
    <div class="login-page animate__animated animate__fadeIn">
        <div class="login-container d-flex justify-content-center align-items-center">
            <div class="login-form-container p-4 rounded shadow">
                <div class="d-flex flex-column align-items-center mb-3">
                    <router-link class="btn btn-outline-success mb-2" to="/service-professional-signup">Register as Professional</router-link>
                    <router-link class="btn btn-outline-warning" to="/customer-signup">Register as Customer</router-link>
                </div>    
                <h2 class="text-center mb-4 text-white">Login</h2>
                <form>
                    <div class="mb-3 text-white">
                        <label for="user-email" class="form-label">Email:</label>
                        <input type="email" class="form-control" id="user-email" placeholder="name@example.com" v-model="cred.email">
                    </div>
                    <div class="mb-3 text-white">
                        <label for="user-password" class="form-label">Password:</label>
                        <input type="password" class="form-control" id="user-password" v-model="cred.password">
                    </div>
                    <div class="text-center">
                        <button type="button" class="btn btn-primary w-100" @click="login">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            cred: {
                email: null,
                password: null
            },
            error: null
        }
    },
    methods: {
        async login() {
            const res = await fetch('/user-login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.cred)
            })
            const data = await res.json()
            if(res.ok){
                localStorage.setItem('auth-token', data.token)
                localStorage.setItem('role', data.role)
                localStorage.setItem('active', data.active)
                localStorage.setItem('user_id', data.id)
                localStorage.setItem('id', data.email.charAt(data.email.length - 11))
                this.$router.push({path: '/'})
            }
            else {
                this.error = data.message
            }
        }
    },
    style: `
    .login-container {
        padding: 50px;
        background-color: rgba(248, 249, 250, 0.8); /* Light background with transparency */
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        width: 100%;
    }
    .form-label {
        color: #ffffff;
    }
    .btn-primary {
        background-color: #007bff;
        border-color: #007bff;
    }
    .btn-primary:hover {
        background-color: #0056b3;
        border-color: #004085;
    }
    `
}