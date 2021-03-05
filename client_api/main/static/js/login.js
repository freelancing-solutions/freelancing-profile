'use strict';


(function() {
    let login_form = {
        email : '',
        password : '',
        url : '/login',
        init : async function(){
                console.log('Code initialized');
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
                method: "post",
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
                localStorage.setItem('x-access-token', json['token'])
            })
        },
    };
    login_form.init();
})()