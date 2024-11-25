export default{
    template: `
    <div class="d-flex justify-content-center animate__animated animate__fadeIn" style="margin-top: 25vh">
        <div class="login-form-container mb-3 p-5" style="width: 40rem;">    
            <h2 class="text-center p-1 text-white">Service Professional Signup</h2>
            <div class="text-danger">{{error}}</div>
            <form>
                <div class="row mb-3">
                    <label for="user-email" class="col-sm-2 col-form-label text-white">Email:</label>
                    <div class="col-sm-10">
                        <input type="email" class="form-control" id="user-email" placeholder="name@example.com" v-model="cred.email">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="user-password" class="col-sm-2 col-form-label text-white">Password:</label>
                    <div class="col-sm-10">
                        <input type="password" class="form-control" id="user-password" v-model="cred.password">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="user-fullname" class="col-sm-2 col-form-label text-white">Fullname:</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="user-fullname" v-model="cred.full_name">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="user-service" class="col-sm-2 col-form-label text-white">Service:</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="user-service" v-model="cred.service">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="user-experience" class="col-sm-2 col-form-label text-white">Experience:</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="user-experience" v-model="cred.experience">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="user-address" class="col-sm-2 col-form-label text-white">Address:</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="user-address" v-model="cred.address">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="user-pincode" class="col-sm-2 col-form-label text-white">Pincode:</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="user-pincode" v-model="cred.pincode">
                    </div>
                </div>
                <div class="text-center">
                    <button class="btn btn-primary mt-2" @click="register">Register</button>
                </div>
            </form>
            <router-link class="nav-link text-center text-warning p-1" to="/login">Login Here</router-link>
        </div>
    </div>
    `,
    data() {
        return {
            cred: {
                email: null,
                password: null,
                full_name: null,
                service: null,
                experience: null,
                address: null,
                pincode: null
            },
            error: null
        }
    },
    methods: {
        async register() {
            const res = await fetch('/api/professionals', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.cred)
            })
            const data = await res.json()
            if(res.ok){
                alert(data.message)
                this.$router.push({path: '/login'})
            }
            else {
                this.error = data.message
            }
        }
    }
}