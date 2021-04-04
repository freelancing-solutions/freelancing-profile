

self.addEventListener('load',async  e => {
    document.getElementById('submit').addEventListener('click', async e => {
        e.preventDefault();
        const project_category_dom = document.getElementById('project_category');
        const project_name_dom = document.getElementById('project_name');
        const description_dom = document.getElementById('description');
        const budget_dom = document.getElementById('budget');
        const est_duration_dom = document.getElementById('est_duration');
        const currency_dom = document.getElementById('currency');

        //Initializing headers for a post request
        let new_headers;
        let auth_token = localStorage.getItem('x-access-token');
        if (auth_token && (auth_token !== "undefined") && (auth_token !== "")){
            new_headers = new Headers({ 'content-type': 'application/json','x-access-token': auth_token})
        }else{
            new_headers = new Headers({ 'content-type': 'application/json'})
        }

        // keep mode as cors in order to be able to modify headers
        let init_post = {
            method: "POST",
            headers: new_headers,
            mode: "cors",
            cache: "no-cache",
            body: JSON.stringify({
                category: project_category_dom.value,
                project_name: project_name_dom.value,
                description: description_dom.value,
                budget: budget_dom.value,
                currency: currency_dom.value,
                est_duration: est_duration_dom.value
            })
          };
        let request = new Request('hire-freelancer/hire', init_post)
        let response = await fetch(request)
        let json_data = await response.json()
        document.getElementById('message').innerHTML = json_data['message']
        return false;
    })
})