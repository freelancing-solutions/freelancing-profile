this.addEventListener('load', () => {
  let init_get = {
      method: "GET",
      headers: { 'Content-Type': 'application/json', 'x-access-token': localStorage.getItem('x-access-token') },
      mode: "cors",
      credentials: "same-origin",
      cache: "no-cache",
  }

    // Where to place the content
    let content_html = document.getElementById('main_content');

    // Handle bars message handler
    let message_template = Handlebars.compile(`
        <div class="card bg-dark">
            <p class="card-text text-light"><em>{{ _message }}</em></p>
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

    // Display Message Template
    // TODO Add formatting for inbox message on the template
    let display_message_template = Handlebars.compile(`
        <div class="card-body">
          <div class="card-header bd-dark">
            <h3 class="card-title"> User Message</h3>
          </div>

          <form class="form-horizontal">

          </form>
        </div>
      `)
    // Handler to display Specific Message
    let showMessage = async e => {
      const contact_id = e.target.id;
      const url = `/admin/message/${contact_id}`;
      const request = new Request(url,init_get);
      try{
        const response = await fetch(request);
        const json_data = await response.json();
      if (json_data && json_data.response) {
        content_html.innerHTML = display_message_template({message : json_data.response })
      }else{
        content_html.innerHTML = message_template({_message: json_data.message })
      }
    }catch(error){
      content_html.innerHTML = message_template({_message: error.message })
    }
  };
    // Messages List template
    // TODO- this template lacks CSS Classes Add Classes for a responsive table
  let show_messages_template = Handlebars.compile(`
        <div class="card-body">
            <div class="card-header bg-dark">
              <h3 class="box-title"> Messages </h3>
            </div>
            <table>
              <theader>
                <tr>
                  <td> Names </td>
                  <td> Email </td>
                  <td> Reason </td>
                  <td> Subject </td>
                  <td> Time Sent </td>
                </tr>
              </theader>
              <tbody>
                {{#each messages }}
                  <tr>
                    <td>
                      <button class='btn btn-default btn-sm' id={{ this.contact_id}} click={e => showMessage(e)}>
                        {{ this.names }}
                      </button>
                    </td>
                    <td>{{ this.email }}</td>
                    <td>{{ this.reason }}</td>
                    <td>{{ this.subject }}</td>
                    <td>{{ this.time_created }}</td>
                  </tr>
                {{/each}}
              </tbody>
            </table>
        </div>
      `)
    // initializing request


    // Creating new databases
    document.getElementById('create_database').addEventListener('click', function(e) {

        let request = new Request('/admin/database/create', init_get);
        fetch(request).then(response => {
            if (!response.ok) {
                throw new Error('There was an error communicating with backend')
            }
            return response.json()
        }).then(json => {
            content_html.innerHTML = message_template({ _message: json.message });
        })
    });

    document.getElementById('load_database').addEventListener('click', function(e) {
        console.log('Event triggered');
        content_html.innerHTML = message_template({ _message: "Handle bars rocks - load" });
    });

    document.getElementById('reset_database').addEventListener('click', function(e) {
        console.log('Event triggered');
        content_html.innerHTML = message_template({ _message: "Handle bars rocks - reset" });
    });

    // Freelance Jobs
    document.getElementById('new_freelance_jobs').addEventListener('click', function(e) {
        let request = new Request('/admin/freelance-jobs/recent', init_get);
        fetch(request).then(response => {
            if (!response.ok) {
                throw new Error('There was an error communicating with backend')
            }
            return response.json()
        }).then(json => {
            content_html.innerHTML = freelance_jobs_template({ freelance_jobs: json })

        });
    });
    document.getElementById('all_freelance_jobs').addEventListener('click', function(e) {
        let request = new Request('/admin/freelance-jobs/all', init_get);
        fetch(request).then(response => {
            if (!response.ok) {
                throw new Error('There was an error communicating with backend')
            }
            return response.json()
        }).then(json => {
            content_html.innerHTML = freelance_jobs_template({ freelance_jobs: json })

        });
    });

    document.getElementById('add_freelance_job').addEventListener('click', function(e) {
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
                "currency": currency_dom.value,
                "budget": budget_allocated_dom.value
            });

            // console.log(json_data);
            let init_post = {
                method: "POST",
                headers: { 'Content-Type': 'application/json', 'x-access-token': localStorage.getItem('x-access-token') },
                mode: "cors",
                body: json_data,
                credentials: "same-origin",
                cache: "no-cache"
            }
            let request = new Request('/admin/freelance-job', init_post);
            fetch(request).then(response => {
                return response.json()
            }).then(json => {
                content_html.innerHTML = message_template({ _message: json.message });
            }).catch(error => {
                content_html.innerHTML = message_template({ _message: error.message });
            })
        });
    });
    // messages

    document.getElementById('new_messages').addEventListener('click', function(e){
        e.preventDefault();
        // TODO- Attach Event Handlers to open messages on Message Titles

        let request = new Request('/admin/messages', init_get);
        fetch(request).then(response => {
          return response.json()
        }).then(json_data => {
            if (json_data && json_data.messages){
                content_html.innerHTML = show_messages_template({messages : json_data.messages })
            }else{
                // This means there was an error on the server
                content_html.innerHTML = message_template({ _message: json_data.message });
            }
        }).catch(error => {
          content_html.innerHTML = message_template({ _message: error.message });
        });

    });

    document.getElementById('all_messages').addEventListener('click', function(e){
      e.preventDefault();
      const request = new Request('/admin/messages/all', init_get);
      fetch(request).then(response => {
        return response.json()
      }).then(json_data => {
          if (json_data && json_data.messages){
              content_html.innerHTML = show_messages_template({messages : json_data.messages })
          }else{
              // This means there was an error on the server
              content_html.innerHTML = message_template({ _message: json_data.message });
          }
      }).catch(error => {
        content_html.innerHTML = message_template({ _message: error.message });
      });

    })
});
