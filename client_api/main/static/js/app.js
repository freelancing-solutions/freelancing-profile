
this.addEventListener('load', () => {

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

    let handle_auth_token_messages = message => {
        switch(message){
            case "Token-Received": token_sent = true; break;
            default : break;
        }
    };


    let handle_auth_token_expired = message => {
        // TODO remove token from local-storage
        // send user to login and inform user the token has expired
        localStorage.setItem('x-access-token',"");
        token_sent = false;
        document.location = "/login";
    };

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
            this.fetch_notifications().then(response => 
                this.render().then(respnse => {
                })
            )
        },
        // handle each incoming notification
        handle_notification : function (){
            while (incoming_notifications_messages.length > 0){
                this.notification_list.push(incoming_notifications_messages.pop())
            }
        },

        // fetch notifications from backend server and storage , part of init
        fetch_notifications : async function(){},

        // store notifications in local storage
        store_notifications : async function(){},

        // render everything with handlebars
        render : async function (){
            console.log('notifications size',this.notification_list.length);
            document.getElementById('total_notifications').innerHTML = this.notification_list.length;
            let notifications_temp = {count : this.notification_list.length, notification_list:this.notification_list}
            this.notification_template_dom.innerHTML = this.notification_handle_temp({notifications : notifications_temp})
        },
    }

    // Listen to messages from service worker;
    let message_listener = e => {
        console.log("Service Worker sent me a message back : ", e.data);
        // call different handlers depending on the message being sent
        switch(e.data.type){
        case "auth-token": handle_auth_token_messages(e.data.message); break;
        case "auth-token-expired": handle_auth_token_expired(e.data.message); break;
        case "notification-message": handle_notification_message(e.data.message);break;
        default : break;
        }
        // re run notification module
        notifications.init();
    };

    navigator.serviceWorker.addEventListener('message', message_listener);

    // self.addEventListener('message', e => {
    //     console.log('Message sent from somewhere else',e);
    // })

    // initialize login on first load
    (function(){
        let token = localStorage.getItem('x-access-token');
        // console.log("checking token : ", token);
        if (token){
            if (!token_sent){
                send_auth_to_service_worker(token).then(() => {})
            }
        }
    })();

    // initialize notifications
    notifications.init()

})