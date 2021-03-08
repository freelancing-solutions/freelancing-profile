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
                body: JSON.stringify({'email':this.email.value,'password':this.password.value})
              };
            let request = new Request('/login',init);
            await fetch(request).then(response => {
                return response.json()
            }).then(json => {
                try{
                    localStorage.removeItem('x-access-token');
                    localStorage.setItem('x-access-token', json['token'])
                }catch(err){
                    localStorage.setItem('x-access-token', json['token'])
                }
                document.getElementById('message').innerHTML =json['message'];

            }).catch(error => {

            })
        },
    };
    login_form.init();
})()