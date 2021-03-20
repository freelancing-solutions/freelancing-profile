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
            console.log('using javascript to send details')
            let new_headers;
            let auth_token = localStorage.getItem('x-access-token');
            if (auth_token && (auth_token !== "undefined") && (auth_token !== "")){
                new_headers = new Headers({ 'content-type': 'application/json','x-access-token': auth_token})
            }else{
                new_headers = new Headers({ 'content-type': 'application/json'})
            }
            // keep mode as cors in order to be able to modify headers
            let init = {
                method: "POST",
                headers: new_headers,
                mode: "cors",
                cache: "no-cache",
                body: JSON.stringify({'email':this.email.value,'password':this.password.value})
              };
            let request = new Request('/login',init);
            await fetch(request).then(response => {
                return response.json()
            }).then(json => {
                try{
                    /* TODO- send message to clear service worker caches */
                    localStorage.removeItem('x-access-token');
                    localStorage.setItem('x-access-token', json['token'])
                }catch(err){
                    localStorage.setItem('x-access-token', json['token'])
                }
                document.getElementById('message').innerHTML =json['message'];

            }).catch(error => {
                    localStorage.removeItem('x-access-token');
            })
        },
    };
    login_form.init();
})();

