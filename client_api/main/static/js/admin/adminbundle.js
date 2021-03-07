
this.addEventListener('load', () => {

    // Where to place the content
    let content_html = document.getElementById('main_content');

    // Handle bars message handler
    let message_template = Handlebars.compile(`
        <div class="card bg-dark">
            <p class="text-light"><em>{{ _message }}</em></p>
        </div>
    `);

    // compiles a list of freelance jobs
    let freelance_jobs_template = Handlebars.compile(`
        <div class="card bg-light">
            <ul>
                    {{#each freelance_jobs }}
                        <li>{{this.project_name}}</li>
                    {{/each}}
            </ul>
        </div>
    `);

    // Compile a form to add a new freelance job
    let add_job_template = Handlebars.compile(`
        <div class="card-body">
            <form class="form-horizontal" id="freelance_job_form">
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text"><i class="fas fa-user"> </i> </span>
                    </div>
                    <input type="text" class="form-control" placeholder="Project Name" id="project_name">
                </div>

                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text"><i class="fas fa-folder"> </i> </span>
                    </div>
                    <textarea class="form-control" placeholder="Description" id="description"></textarea>
                </div>

                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text"><i class="fas fa-calendar"> </i> </span>
                    </div>
                    <input type="text" class="form-control" placeholder="00:00" id="est_hours_to_complete">
                </div>

                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text"><i class="fas fa-credit-card"> </i> </span>
                    </div>
                    <select class="form-control" id="currency">
                        <option value="R">R (South African Rand)</option>
                        <option value="$">$ (American Dollar)</option>
                    </select>
                </div>

                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text"><i class="fas fa-credit-card"> </i> </span>
                    </div>
                    <input type="text" class="form-control" id="budget_allocated" placeholder="Budget Allocated">
                </div>
                <div class="input-group mb-3">
                    <button class="btn btn-primary" id="submit">
                        <strong>
                            <i class="fas fa-save"> </i>
                            Submit
                        </strong>
                    </button>
                </div
            </form>
        </div>
    `);

    // initializing request
    let init_get = {
        method : "GET",
        headers: {'Content-Type': 'application/json','x-access-token' : localStorage.getItem('x-access-token')},
        mode: "cors",
        credentials: "same-origin",
        cache: "no-cache",
    }

    // Creating new databases
    document.getElementById('create_database').addEventListener('click', function(e){

        let request = new Request('/admin/database/create', init_get);
        fetch(request).then(response => {
            if (!response.ok){
                throw new Error('There was an error communicating with backend')
            }
            return response.json()
        }).then(json => {
            content_html.innerHTML = message_template({ _message: json.message });
        })
    });

    document.getElementById('load_database').addEventListener('click', function(e){
        console.log('Event triggered');
        content_html.innerHTML = message_template({ _message: "Handle bars rocks - load"});
    });

    document.getElementById('reset_database').addEventListener('click', function(e){
        console.log('Event triggered');
        content_html.innerHTML = message_template({ _message: "Handle bars rocks - reset"});
    });

    document.getElementById('new_freelance_jobs').addEventListener('click', function (e){
        let request = new Request('/admin/freelance-jobs/recent', init_get);
        fetch(request).then(response => {
            if (!response.ok){
                throw new Error('There was an error communicating with backend')
            }
            return response.json()
        }).then(json => {
            content_html.innerHTML = freelance_jobs_template({freelance_jobs : json})

        });
    });
    document.getElementById('all_freelance_jobs').addEventListener('click', function (e){
        let request = new Request('/admin/freelance-jobs/all', init_get);
        fetch(request).then(response => {
            if (!response.ok){
                throw new Error('There was an error communicating with backend')
            }
            return response.json()
        }).then(json => {
            content_html.innerHTML = freelance_jobs_template({freelance_jobs : json})

        });
    });

    document.getElementById('add_freelance_job').addEventListener('click', function (e){
        // Adding form to submit a freelance job to DOM
        content_html.innerHTML = add_job_template();
        document.getElementById('freelance_job_form').addEventListener('submit', e => {
            e.preventDefault();
            console.log('Submit freelance job clicked');
            let project_name_dom = document.getElementById('project_name');
            let description_dom = document.getElementById('description');
            let hours_to_complete_dom = document.getElementById('est_hours_to_complete');
            let currency_dom = document.getElementById('currency');
            let budget_allocated_dom = document.getElementById('budget_allocated');

            let json_data = JSON.stringify({
                "project_name": project_name_dom.value,
                "description": description_dom.value,
                "est_hours_to_complete": hours_to_complete_dom.value,
                "currency":currency_dom.value,
                "budget":budget_allocated_dom.value});

            console.log(json_data);
            let init_post = {
                method : "POST",
                headers: {'Content-Type': 'application/json','x-access-token' : localStorage.getItem('x-access-token')},
                mode: "cors",
                body: json_data,
                credentials: "same-origin",
                cache: "no-cache"
            }
            let request = new Request('/admin/freelance-job',init_post);
            fetch(request).then(response => {
                if (!response.ok){
                    throw new Error('There was an error communicating with backend')
                }
                return response.json()
            }).then(json => {
                content_html.innerHTML = message_template({_message : json.message });
            });
        });
    });

});