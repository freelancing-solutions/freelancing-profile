let token_sent = false;
let send_auth_to_service_worker = async (message )=> {
    if (navigator.serviceWorker.ready){
        navigator.serviceWorker.controller.postMessage({
            type: "auth-token",
            token: message
        })
        return true;
    }
    return false;
};

(function(){
    let token = localStorage.getItem('x-access-token');
    console.log("checking token : ", token);
    if (token){
        if (!token_sent){
            send_auth_to_service_worker(token).then(response => {
                if (response){
                    token_sent = true;
                }
            })
        }
    }
})();

let message_listener = e => {
    console.log("Messages are being dispatched", e.data);
};

this.addEventListener('message', message_listener);