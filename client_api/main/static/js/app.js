let token_sent = false;

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

// Listen to messages from service worker;
let message_listener = e => {
    console.log("Service Worker sent me a message back : ", e.data);
    // call different handlers depending on the message being sent
    switch(e.data.type){
       case "auth-token": handle_auth_token_messages(e.data.message); break;
       default : break;
    }
};

navigator.serviceWorker.addEventListener('message', message_listener);



// self.addEventListener('message', e => {
//     console.log('Message sent from somewhere else',e);
// })

(function(){
    let token = localStorage.getItem('x-access-token');
    // console.log("checking token : ", token);
    if (token){
        if (!token_sent){
            send_auth_to_service_worker(token).then(() => {})
        }
    }
})();


