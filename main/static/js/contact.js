
let freelance_job_dom_html = `
    <div class="input-group mb-3">
        <div class="input-group-prepend">
                <span class="input-group-text"> Freelance Job ID</span>
        </div>
        <input type="email" class="form-control" placeholder="Job ID">
    </div>
    `;
let support_ticket_dom_html = `
<div class="input-group mb-3">
<div class="input-group-prepend">
  <span class="input-group-text">Support Ticket Type</span>
</div>
  <select class="form-control" id="support_ticket_type">
    <option value="" selected="selected">--Select Ticket Type---</option>
    <option value="payments">Payments</option>
    <option value="refund">Refund</option>
    <option value="freelance-job">Freelance Job</option>
    <option value="website-functionality">Website Functionality</option>
  </select>
</div>`;

function on_selected_select_reason(e){
    console.log('event triggered', e.target.value);
    let additional_content_dom = document.getElementById('additional_content');
    additional_content_dom.innerHTML = '';

    if (e.target.value == 'freelance-jobs'){
       additional_content_dom.innerHTML = freelance_job_dom_html;
       additional_content_dom.classList.add('input-group mb-3');
    }

    if (e.target.value == 'support-ticket'){
        additional_content_dom.innerHTML = support_ticket_dom_html;
        additional_content_dom.classList.add('input-group mb-3'); 
    }
};

let select_reason_dom = document.getElementById('select_reason');
select_reason_dom.addEventListener('click', on_selected_select_reason);

console.log('this happened', select_reason_dom);