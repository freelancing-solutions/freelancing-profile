


self.addEventListener('load', () => {
    document.getElementById('logout').addEventListener('click', async e => {
        // Dispatch messages to service worker
    let send_auth_to_service_worker = async (message )=> {
        navigator.serviceWorker.ready.then(registration => {
            registration.active.postMessage(message);
        });
        return true;
    };

   // signing out by sending the message with an intent to sign-out
   let response = await send_auth_to_service_worker({type: "auth-status",status: 'sign-out'})
    });
})