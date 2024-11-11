export default {
  template: `
    <div class="login-container">
      <div class="hero-section d-flex align-items-center justify-content-center">
        <div class="login-box animate__animated animate__fadeIn">
          <h2 class="text-center mb-4">Login</h2>
          <form @submit.prevent="login">
            <div class="form-group mb-3">
              <label for="email">Email or Username</label>
              <input type="text" v-model="emailOrUsername" id="email" class="form-control" required />
            </div>
            <div class="form-group mb-3">
              <label for="password">Password</label>
              <input type="password" v-model="password" id="password" class="form-control" required />
            </div>
            <button type="submit" class="btn btn-primary w-100">Login</button>
          </form>
          <div v-if="errorMessage" class="error-message mt-3">{{ errorMessage }}</div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      emailOrUsername: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://localhost:5000/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.emailOrUsername.includes('@') ? this.emailOrUsername : null,
            username: this.emailOrUsername.includes('@') ? null : this.emailOrUsername,
            password: this.password
          })
        });

        const data = await response.json();

        if (response.ok) {
          // Store the token and redirect to the home page
          localStorage.setItem('token', data.token);
          this.$router.push('/');
          console.log(data.token);
        } else {
          this.errorMessage = data.message;
        }
      } catch (error) {
        this.errorMessage = 'An error occurred while logging in.';
      }
    }
  },
  style: `
    .login-container {
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('/static/images/home.gif') no-repeat center center;
      background-size: cover;
      color: white;
    }
    .login-box {
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