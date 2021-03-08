this.addEventListener('load', function() {

    let message_template = Handlebars.compile(
        `
            <div class="card-text">
                <p>{{ _message }}</p>
            </div>
        `);

    let message_dom = document.getElementById('message_content');

    document.getElementById('register_form').addEventListener('submit', e => {
        e.preventDefault();
        let names_dom = document.getElementById('names');
        let email_dom = document.getElementById('email');
        let password_dom = document.getElementById('password');
        let match_password_dom = document.getElementById('password_match');

        if (password_dom.value == match_password_dom.value) {
            let json_data = JSON.stringify({'email':email_dom.value,'names':names_dom.value,'password':password_dom.value});
            let init_post = {
                method: "POST",
                headers: { 'Content-Type': 'application/json', 'x-access-token': localStorage.getItem('x-access-token') },
                mode: "cors",
                body: json_data,
                credentials: "same-origin",
                cache: "no-cache"
            };
            let request = new Request('/register',init_post);
            fetch(request).then(response => {
                if (!response.ok){throw new Error("error login in")}
                return response.json();
            }).then(json => {
                localStorage.removeItem('x-access-token');
                localStorage.setItem('x-access-token', json['token']);
                send_auth_to_service_worker(json['token']).then( response => {

                });

                message_dom.innerHTML = message_template({_message : 'Your account was created and you where successfully logged in'})

            }).catch(error => {
                message_dom.innerHTML = message_template({_message : 'There was an error creating an account'})
            })


        } else {
            alert('passwords do not match');
        }

    });


});