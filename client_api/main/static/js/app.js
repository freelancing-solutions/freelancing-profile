
self.addEventListener('load', () => {

    let token_sent = false;
    let incoming_notifications_messages = [];

    // Dispatch messages to service worker
    let send_auth_to_service_worker = async (message )=> {
        navigator.serviceWorker.ready.then(registration => {
            registration.active.postMessage({
                type: "auth-token",
                token: message
            });
        });
        return true;
    };

    let dispatch_messages = async (message) => {
        navigator.serviceWorker.ready.then(registration => {
            registration.active.postMessage(message);
        });
        return true;
    }

    let handle_auth_token_messages = message => {
        switch(message){
            case "Token-Received": token_sent = true; break;
            case "Not-Logged-IN": token_sent = false;break;
            default:  break;
        }
    };


    let handle_auth_token_expired = message => {
        // TODO remove token from local-storage
        // send user to login and inform user the token has expired
        localStorage.removeItem('x-access-token');
        token_sent = false;
        document.location = "/login";
        console.log('User logged out authorization expired')
    };

    let handle_auth_status_messages = ({ type,status, token}) => {
        // the intent to sign-in/out is received continue signing-out/in
        if (status === "logged-out") {
            localStorage.removeItem('x-access-token');
            if (document.location.href.endsWith("/logout")){document.location = "/"}
        }
        console.log("location href: ", document.location.href)
        if ((status === "logged-in")){
            localStorage.setItem('x-access-token',token)
        }
    }

    let handle_user_messages = (data) => {
        switch (data.status){
            case "counted": {
                localStorage.setItem('visitors', data.unique_visitors)
                localStorage.setItem('return_visitors', data.return_visitors)
                localStorage.setItem('counted', 'yes')
            }break;
            case "page-view":{
                localStorage.setItem('page_views', data.page_views )
            }break;
            default: break;
        }
    }

    // Listen to messages from service worker;
    let message_listener = e => {
        console.log("Service Worker sent me a message back : ", e.data);
        // call different handlers depending on the message being sent
        switch(e.data.type){
        case "auth-token": handle_auth_token_messages(e.data.message); break;
        case "auth-token-expired": handle_auth_token_expired(e.data.message); break;
        case "notification-message": handle_notification_message(e.data.message);break;
        case "auth-status": handle_auth_status_messages(e.data);break;
        case "user-messages": handle_user_messages(e.data);break;
        default : break;
        }
        // re run notification module
        notifications.init();
    };

    let service_registration = async function(){
        let registered = await navigator.serviceWorker.register('sw.js');
        navigator.serviceWorker.addEventListener('message', message_listener);
        return registered;
    }

    // self.addEventListener('message', e => {
    //     console.log('Message sent from somewhere else',e);
    // })

    // initialize login on first load
    let init_auth_token_send = async function(){
        let token = localStorage.getItem('x-access-token');
        // console.log("checking token : ", token);
        if ((token !== "undefined") && (token !== "") && (token !== null) && (token !== "null")){
            if (!token_sent){
                send_auth_to_service_worker(token).then(() => {})
            }
        }
        return true;
    };

    let unique_visitor_send = async function(){
        await dispatch_messages({
            type: 'user-messages',status: 'count-unique',
        })
        return true;
    }
    let return_visitor_send = async function(){
        await dispatch_messages({
            type: 'user-messages',status: 'count-return',
        })
        return true;
    }
    let page_view_send = async function(){
        await dispatch_messages({
            type: 'user-messages', status: 'page-view'
        })
    }

    // ************************************************************************************//
    //  Notification Services
    let handle_notification_message = message => {
        // TODO- get hold of the header notification tab
        // TODO- send notification to header file
        incoming_notifications_messages.push(message);
    };


    let notifications = {
        notification_list : [{
            notice: "This is a notice", notice_time: '3 seconds ago', notice_link : "/notifications/first-notice"
        },{
            notice: "This is a second notice", notice_time: '2 seconds ago', notice_link : "/notifications/second-notice"
        }],

        notification_handle_temp : Handlebars.compile(`
            {{#with notifications }}
                <span class="dropdown-item dropdown-header">{{ count }} Notifications</span>

                {{#each notification_list }}
                    <div class="dropdown-divider"></div>
                    <a href="{{this.notice_link}}" class="dropdown-item">
                    <i class="fas fa-envelope mr-2"></i> {{this.notice}}
                    <span class="float-right text-muted text-sm">{{this.notice_time}}</span>
                    </a>
                {{/each}}

                <div class="dropdown-divider"></div>
                <a href="/notifications/list" class="dropdown-item dropdown-footer">See All Notifications</a>
            {{/with}}
        `),

        notification_template_dom : document.getElementById('notifications_id'),

        // initialize this module
        init: function (){
            this.fetch_notifications().then(response => {
                console.log('notifications : ', response)
                this.render().then(response => {
                })
            })
        },
        // handle each incoming notification
        handle_notification : function (){
            while (incoming_notifications_messages.length > 0){
                this.notification_list.push(incoming_notifications_messages.pop())
            }
        },
        // fetch notifications from backend server and storage , part of init
        fetch_notifications : async function(){
            let init_get ={
                method: 'GET',
                mode:'cors',
                credentials:'same-origin',
                headers: new Headers({'content-type': 'application/json'})
            }

            let request = new Request('/notifications', init_get)
            let response = await fetch(request)

            if (response.ok){
                let json_data = await response.json()
                this.notifications_list = json_data['notifications_list']
            }
        },

        // store notifications in local storage
        store_notifications : async function(){},

        // render everything with handlebars
        render : async function (){
            console.log('notifications size',this.notification_list.length);
            try{
                document.getElementById('total_notifications').innerHTML = `${this.notification_list.length}`;
                let notifications_temp = {count : this.notification_list.length, notification_list:this.notification_list}
                this.notification_template_dom.innerHTML = this.notification_handle_temp({notifications : notifications_temp})
            }catch(error){
                // we are in login pages there is no notifications or headers bars
            }
        },
    }

    service_registration().then(registered => {
        if (registered){
            init_auth_token_send().then(() => {
                // NOTE: initializing notification messaging
                notifications.init()
                console.log("service worker installed and auth initialized")
            })
            try{
                /** this really counts page views TODO- feature versions may gather more information **/
                let is_counted = localStorage.getItem('counted')
                if (is_counted === "yes"){
                    // return_visitor_send().then(response => {})
                    page_view_send().then(response => {});
                    let return_counted = localStorage.getItem('return_counted');
                    if (return_counted !== 'yes'){
                    return_visitor_send().then( response => {
                        localStorage.setItem('return_counted','yes')
                    })}
                }else{
                    unique_visitor_send().then(response => {})
                }
            }catch (e){
                page_view_send().then(response => {})
                unique_visitor_send().then(response => {})
            }
        }
    });
})