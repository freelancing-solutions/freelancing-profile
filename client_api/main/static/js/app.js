

function setHeaders(headers){
    let access_token = localStorage.getItem('x-access-token')
    if (access_token){
        return {
            ...headers,
            'x-access-token': access_token
        }
    }else{
        return headers
    }
}


(function(){
    // Initialize app with default values 
    // Checks if user is logged in and populate the app structures

    let app = {
        init: function(){
        },
    }

})()
