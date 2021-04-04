self.addEventListener('load', async () => {
    // document.getElementById("uptime").value;

    let msToDate = (milliseconds) =>' ' + (new Date(milliseconds)) + ' ';
    let disp_date = dtime =>msToDate(dtime).split("GMT")[0];
    let disp_num = number =>String(number).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    let elapse_time = e_time =>`${new Date(e_time).getHours()}:${new Date(e_time).getMinutes()}:${new Date(e_time).getSeconds()}`
    let disp_latent = time => `${new Date(parseFloat(time)).getMilliseconds()}`

    let render_from_doc = async () => {
        let uptime = document.getElementById("uptime").value
        let started = document.getElementById("started").value
        let total_requests = document.getElementById("total_requests").value
        let static_requests = document.getElementById("static_requests").value
        let documents_requests = document.getElementById("documents_requests").value
        let latency = document.getElementById('latency').value
        let highest_latency = document.getElementById('highest_latency').value
        let unique_visitors = document.getElementById('unique_visitors').value
        let return_visitors = document.getElementById('return_visitors').value
        let page_views = document.getElementById('page_views').value

        document.getElementById("display_uptime").innerHTML = `<span class="text text-dark"> Uptime: <em class="text-info">${elapse_time(parseInt(uptime))}</em> </span>`
        document.getElementById( "display_started").innerHTML = `<span class="text text-dark"> Server StartUp: <em class="text-info">${disp_date(parseInt(started))}</em> </span>`
        document.getElementById("display_total").innerHTML = `<span class="text text-dark"> Total: <em class="text-info">${disp_num(total_requests)}</em></span>`
        document.getElementById('display_static').innerHTML = `<span class="text text-dark"> Static Docs : <em class="text-info">${disp_num(static_requests)}</em></span>`
        document.getElementById('display_html').innerHTML = `<span class="text text-dark"> HTML Docs : <em class="text-info">${disp_num(documents_requests)}</em></span>`
        document.getElementById('display_latency').innerHTML = `<span class="text text-dark"> Request Latency : <em class="text-info">${disp_latent(latency)} ms</em></span>`
        document.getElementById('display_highest_latency').innerHTML = `<span class="text text-dark"> Highest Latency : <em class="text-info">${disp_latent(highest_latency)} ms</em></span>`
        document.getElementById('display_return_visitors').innerHTML = `<span class="text text-dark"> Return Visitors : <em class="text-info">${disp_num(return_visitors)} </em></span>`
        document.getElementById('display_unique_visitors').innerHTML = `<span class="text text-dark"> Unique Visitors : <em class="text-info">${disp_num(unique_visitors)} </em></span>`
        document.getElementById('display_page_views').innerHTML = `<span class="text text-dark"> Page Views : <em class="text-info">${disp_num(page_views)} </em></span>`
    }

    await render_from_doc()

})

