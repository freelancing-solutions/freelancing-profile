

self.addEventListener('load',async e => {
    let response_message = document.getElementById('response_message');
    let title = document.getElementById('title');
    let article = document.getElementById('article');
    let draft = document.getElementById('draft');

    document.getElementById('publish').addEventListener('click', async e => {
        e.preventDefault();
        auth_token = localStorage.getItem('x-access-token')
        let init_post = {
            method:"POST",
            headers: new Headers({'content-type': 'application/json', 'x-access-token': auth_token}),
            mode:"cors",
            body:JSON.stringify({title:title.value, article: article.value,draft: draft.value, is_published:true}),
            credentials: "same-origin",
            cache:"no-cache"
        }
        let request = new Request('/blog/editor', init_post);
        let response = await fetch(request);
        let json_data = await response.json()
        if (response.ok){
            response_message.innerHTML = `<span class="text-info">${json_data['message']}</span>`
        }else{
            response_message.innerHTML = `<span class="text-warning">${json_data['message']}</span>`
        }
        return false;
    });

    document.getElementById('save').addEventListener('click', async e =>{
        e.preventDefault();

        return false;
    });


});