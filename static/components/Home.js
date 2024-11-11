export default {
    template: `
        <div>
            <!-- Hero Section -->
            <section class="hero-section d-flex align-items-center justify-content-center">
                <div class="text-center ">
                    <h1 class="display-4 fw-bold animate__animated animate__backInDown">Find Trusted Services Near You</h1>
                    <p class="lead mt-3 animate__animated animate__backInDown">Get quick access to professional services in your area.</p>
                    <router-link to="/services" class="btn btn-primary btn-lg mt-4 animate__animated animate__bounceInUp">Explore Services</router-link>
                </div>
            </section>

            <!-- Info Section -->
            <section class="container my-5 animate__animated animate__fadeInUp">
                <div class="row">
                    <div class="col-md-4">
                        <h3>Service Providers</h3>
                        <p>Skilled professionals ready to assist you.</p>
                    </div>
                    <div class="col-md-4">
                        <h3>Customer Reviews</h3>
                        <p>Read reviews from other users.</p>
                    </div>
                    <div class="col-md-4">
                        <h3>24/7 Support</h3>
                        <p>We're here to help whenever you need it.</p>
                    </div>
                </div>
            </section>
        </div>
    `
}
