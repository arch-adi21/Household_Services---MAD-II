export default{
    template: `
    <div>
        <h1 class="text-danger text-center animate__animated animate__fadeIn">Welcome Admin</h1>
        <h2 class="text-center text-white animate__animated animate__fadeIn">Services</h2>
        <div class="d-flex justify-content-center p-1 animate__animated animate__fadeInLeft">
            <button type="button" class="btn btn-success"><router-link class="nav-link p-1" to="/create-service">+ New Service</router-link></button>
        </div>
        <div class="card text-center bg-transparent animate__animated animate__backInLeft" style="width: 77rem;">
            <div class="card-header  bg-transparent">
                <div class="container text-center  bg-transparent">
                    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5  bg-transparent">
                        <div class="col text-white h5">ID</div>
                        <div class="col text-white h5">Service Name</div>
                        <div class="col text-white h5">Base Price (Rs.)</div>
                        <div class="col text-white h5">Time Required</div>
                        <div class="col text-white h5">Action</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            isWaiting: false
        }
    },
    methods: {
        async download_csv() {
            this.isWaiting = true
            const res = await fetch('/download-csv')
            const data = await res.json()
            if (res.ok) {
                const taskId = data['task-id']
                const intv = setInterval(async () => {
                    const csv_res = await fetch(`/get-csv/${taskId}`)
                    if(csv_res.ok){
                        this.isWaiting = false
                        clearInterval(intv)
                        window.location.href = `/get-csv/${taskId}`
                    }
                }, 1000)
            }
        }

    }
}