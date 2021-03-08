(function() {
    let login_form = {
        email : '',
        password : '',
        url : '/login',
        init : async function(){
                await this.cacheDom();
                await this.attach_handlers();
        },
        attach_handlers: async function(){
            document.getElementById('signin_form').addEventListener('submit', this.do_login)
        },
        cacheDom: async function(){
            this.email = $('#email');
            this.password = $('#password');
        },
        do_login: async function(e){
            e.preventDefault();
            let init = {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                mode: "cors",
                credentials: "same-origin",
                cache: "no-cache",
                body: JSON.stringify({'username':this.email.value,'password':this.password.value})
              };
            let request = new Request('/login',init);
            await fetch(request).then(response => {
                if (!response.ok){
                    console.log(response.text())
                }else{
                    return response.json()
                }
            }).then(json => {
                localStorage.removeItem('x-access-token');
                localStorage.setItem('x-access-token', json['token'])
                send_auth_to_service_worker(json['token']).then( response => {
                });

                document.getElementById('message').innerHTML =`
                    <div class="card">
                        <p class="card-text mr-2 ml-2 mb-2 mt-2">Your account was created and you where successfully logged in</p>
                    </div>
                `;

            })
        },
    };
    login_form.init();
})()