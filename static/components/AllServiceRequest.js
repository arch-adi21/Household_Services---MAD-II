export default{
    template: `
    <div>
        <div class="container">
            <div class="row">
                <div class="col">
                </div>
                <div class="col">
                    <h2 class="text-center text-white animate__animated animate__fadeIn">Service Requests</h2>
                </div>
                <div class="col p-2 text-end animate__animated animate__fadeInDown">
                    <h6 class="text-primary">Download Details</h6>
                    <button class="btn btn-primary" @click='download_csv'>Export as CSV</button>
                    <span class="animate__animated animate__flipInY text-white" v-if='isWaiting'> Waiting... </span>
                </div>
            </div>
        </div>
        <div class="card text-center bg-transparent animate__animated animate__fadeInLeft" style="width: 77rem;">
            <div class="card-header">
                <div class="container text-center">
                    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-4">
                        <div class="col text-white">ID</div>
                        <div class="col text-white">Service Name</div>
                        <div class="col text-white">Date Of Request</div>
                        <div class="col text-white">Status</div>
                    </div>
                </div>
            </div
        </div>
        <div class="card text-center bg-transparent" style="width: 77rem;">
            <ul class="list-group list-group-flush bg-transparent">
                <li class="list-group-item bg-transparent" v-for="(service_request,index) in allServiceRequests">
                    <div class="container text-center">
                        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-4">
                            <div class="col text-white">{{service_request.id}}</div>
                            <div class="col text-white" v-for="(service,index) in allServices" v-if="service.id==service_request.service_id">{{service.name}}</div>
                            <div class="col text-white">{{service_request.date_of_request}}</div>
                            <div class="col text-white">{{service_request.service_status}}</div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
    `,
    data() {
        return {
            allServiceRequests: [],
            allServices: [],
            error: null,
            customer: {
                "user_id":null
            },
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
                        alert("Service Request Details Downloaded in CSV Format")
                        this.isWaiting = false
                        clearInterval(intv)
                        window.location.href = `/get-csv/${taskId}`
                    }
                }, 1000)
            }
        }
    },
    async mounted() {
        this.customer.user_id = localStorage.getItem('user_id')
        const res = await fetch('/api/request/service')
        const data = await res.json()
        if(res.ok){
            this.allServiceRequests = data.service_requests,
            this.allServices = data.services
        }
    }
}