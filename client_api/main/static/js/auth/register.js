this.addEventListener('load', function() {

    const message_dom = document.getElementById('message_content');
    // jshint ignore:line
    let message_template = Handlebars.compile(`                 
                <div class="card-header bg-{{ _category }}">
                    <span class="alert">{{ _message }}</span>
                </div>                
    `);
    let send_auth_to_service_worker = async (message )=> {
        navigator.serviceWorker.ready.then(registration => {
            registration.active.postMessage({
                type: "auth-token",
                token: message
            });
        });
        return true;
    };

    const submit_handler = async e => {
        e.preventDefault();
        const surname_dom = document.getElementById('surname')
        const names_dom = document.getElementById('names');
        const email_dom = document.getElementById('email');
        const cell_dom = document.getElementById('cell');
        const password_dom = document.getElementById('password');
        const match_password_dom = document.getElementById('password_match');

        if (password_dom.value === match_password_dom.value) {
            auth_token = localStorage.getItem('x-access-token');
            let new_headers;
            if ((auth_token !== "undefined") && (auth_token !== "")){
                new_headers = new Headers({ 'content-type': 'application/json','x-access-token': auth_token})
            }else{
                new_headers = new Headers({ 'content-type': 'application/json'})
            }
            // keep mode as cors in order to be able to modify headers
            let json_data = JSON.stringify({'surname': surname_dom.value,
                                            'names':names_dom.value,
                                            'email':email_dom.value,
                                            'cell':cell_dom.value,
                                            'password':password_dom.value});
            const init_post = {
                method: "POST",
                headers: new_headers,
                mode: "cors",
                body: json_data,
                credentials: "same-origin",
                cache: "no-cache"
            };
            const request = new Request('/register',init_post);
            const response = await fetch(request);
            const response_data = await response.json()
            message_dom.innerHTML = message_template({_message : response_data['message']});
            if (response.ok && response_data['token']){
                localStorage.removeItem('x-access-token');
                localStorage.setItem('x-access-token', response_data['token']);
                const service_worker_response = await send_auth_to_service_worker(response_data['token']);
            }
    }
    }

    document.getElementById('register_button').addEventListener('click',submit_handler);

});


