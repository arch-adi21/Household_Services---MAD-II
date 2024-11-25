export default{
    template: `
    <div>
        <h1 class="text-center text-danger animate__animated animate__fadeIn">Welcome Professional</h1>
        <h2 class="text-center text-white animate__animated animate__fadeIn">Available Service Requests</h2>
        <div class="card text-center bg-transparent" style="width: 77rem;">
            <div class="card-header animate__animated animate__fadeInLeft">
                <div class="container text-center">
                    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5">
                        <div class="col text-white">ID</div>
                        <div class="col text-white">Service Name</div>
                        <div class="col text-white">Date Of Request</div>
                        <div class="col text-white">Status</div>
                        <div class="col text-white">Action</div>
                    </div>
                </div>
            </div
        </div>
        <div class="card text-center  bg-transparent animate__animated animate__fadeInLeft" style="width: 77rem;">
            <ul class="list-group list-group-flush  bg-transparent">
                <li class="list-group-item  bg-transparent" v-for="(service_request,index) in allServiceRequests" v-if="service_request.service_status=='requested'">
                    <div class="container text-center">
                        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5">
                            <div class="col text-white">{{service_request.id}}</div>
                            <div class="col text-white" v-for="(service,index) in allServices" v-if="service.id==service_request.service_id">{{service.name}}</div>
                            <div class="col text-white">{{service_request.date_of_request}}</div>
                            <div class="col text-white">{{service_request.service_status}}</div>
                            <div class="col text-white">
                                <button class="btn btn-success" v-if="service_request.service_status!='closed'" @click="accept(service_request.id)">Accept</button>
                            </div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
    <div>
        <h2 class="text-center p-2 text-white animate__animated animate__fadeIn">Accepted Service Requests</h2>
        <div class="card text-center bg-transparent" style="width: 77rem;">
            <div class="card-header animate__animated animate__fadeInLeft">
                <div class="container text-center">
                    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5">
                        <div class="col text-white">ID</div>
                        <div class="col text-white">Service Name</div>
                        <div class="col text-white">Date Of Request</div>
                        <div class="col text-white">Status</div>
                        <div class="col text-white">Action</div>
                    </div>
                </div>
            </div
        </div>
        <div class="card text-center bg-transparent animate__animated animate__fadeInLeft" style="width: 77rem;">
            <ul class="list-group list-group-flush bg-transparent">
                <li class="list-group-item bg-transparent" v-for="(service_request,index) in allServiceRequests" v-if="service_request.service_status=='assigned' && service_request.professional_id==professional.professional_id">
                    <div class="container text-center">
                        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5">
                            <div class="col text-white">{{service_request.id}}</div>
                            <div class="col text-white" v-for="(service,index) in allServices" v-if="service.id==service_request.service_id">{{service.name}}</div>
                            <div class="col text-white">{{service_request.date_of_request}}</div>
                            <div class="col text-white">{{service_request.service_status}}</div>
                            <div class="col text-white">
                                <button class="btn btn-danger" v-if="service_request.service_status!='closed'" @click="reject(service_request.id)">Reject</button>
                            </div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
    <div>
        <h2 class="text-center p-2 text-white animate__animated animate__fadeIn">Closed Service Requests</h2>
        <div class="card text-center bg-transparent animate__animated animate__fadeInLeft" style="width: 77rem;">
            <div class="card-header">
                <div class="container text-center">
                    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5">
                        <div class="col text-white">ID</div>
                        <div class="col text-white">Service Name</div>
                        <div class="col text-white">Date Of Request</div>
                        <div class="col text-white">Rating</div>
                        <div class="col text-white">Remarks</div>
                    </div>
                </div>
            </div
        </div>
        <div class="card text-center bg-transparent animate__animated animate__fadeInLeft" style="width: 77rem;">
            <ul class="list-group list-group-flush bg-transparent">
                <li class="list-group-item bg-transparent" v-for="(service_request,index) in allServiceRequests" v-if="service_request.service_status=='closed' && service_request.professional_id==professional.professional_id">
                    <div class="container text-center">
                        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5">
                            <div class="col text-white">{{service_request.id}}</div>
                            <div class="col text-white" v-for="(service,index) in allServices" v-if="service.id==service_request.service_id">{{service.name}}</div>
                            <div class="col text-white">{{service_request.date_of_request}}</div>
                            <div class="col text-white">{{service_request.rating}}</div>
                            <div class="col text-white">{{service_request.remarks}}</div>
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
            professional: {
                "professional_id": localStorage.getItem('id')
            },
            error: null,
            customer: {
                "user_id":null
            }
        }
    },
    methods: {
        async accept(id) {
            const res = await fetch(`/api/accept/service-request/${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.professional)
            })
            const data = await res.json()
            if(res.ok){
                alert(data.message)
                location.reload()
            }
        },
        async reject(id) {
            const res = await fetch(`/api/accept/service-request/${id}`)
            const data = await res.json()
            if(res.ok){
                alert(data.message)
                location.reload()
            }
        }
    },
    async mounted() {
        const res = await fetch('/api/request/service')
        const data = await res.json()
        if(res.ok){
            this.allServiceRequests = data.service_requests
            this.allServices = data.services
        }
    }
}
