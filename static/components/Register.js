export default {
  template: `
    <div class="register-container">
      <div class="hero-section d-flex align-items-center justify-content-center">
        <div class="register-box animate__animated animate__fadeIn">
          <h2 class="text-center mb-4">Register</h2>
          <form @submit.prevent="register">
            <div class="form-group mb-3">
              <label for="username">Username</label>
              <input type="text" v-model="username" id="username" class="form-control" required />
            </div>
            <div class="form-group mb-3">
              <label for="email">Email</label>
              <input type="email" v-model="email" id="email" class="form-control" required />
            </div>
            <div class="form-group mb-3">
              <label for="password">Password</label>
              <input type="password" v-model="password" id="password" class="form-control" required />
            </div>
            <div class="form-group mb-3">
              <label for="role">Role</label>
              <select v-model="role" id="role" class="form-control" required>
                <option value="2">Customer</option>
                <option value="3">Service Provider</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary w-100">Register</button>
          </form>
          <div v-if="errorMessage" class="error-message mt-3">{{ errorMessage }}</div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      username: '',
      email: '',
      password: '',
      role: '',
      errorMessage: ''
    };
  },
  methods: {
    async register() {
      try {
        const response = await fetch('http://localhost:5000/api/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password,
            role_id: this.role
          })
        });

        const data = await response.json();

        if (response.ok) {
          // Redirect to the login page
          this.$router.push('/login');
        } else {
          this.errorMessage = data.message;
        }
      } catch (error) {
        this.errorMessage = 'An error occurred while registering.';
      }
    }
  },
  style: `
    .register-container {
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('/static/images/home.gif') no-repeat center center;
      background-size: cover;
      color: white;
    }
    .register-box {
      background: rgba(255, 255, 255, 0.9);
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      width: 100%;
      max-width: 400px;
    }
    .error-message {
      color: red;
    }
  `
};