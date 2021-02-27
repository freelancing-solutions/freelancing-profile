// Handle reason selection
function on_selected_select_reason(e){
    this.freelance_job_dom_html = `
    <div class="input-group mb-3">
        <div class="input-group-prepend">
                <span class="input-group-text"> Freelance Job ID</span>
        </div>
        <input type="text" class="form-control" placeholder="Job ID" id="freelance_job_id">
    </div>
    `;
    this.support_ticket_dom_html = `
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

    this.additional_content_dom = document.getElementById('additional_content');
    this.additional_content_dom.innerHTML = '';

    if (e.target.value == 'freelance-jobs'){
       this.additional_content_dom.innerHTML = this.freelance_job_dom_html;
       this.additional_content_dom.classList.add('input-group mb-3');
    }

    if (e.target.value == 'support-ticket'){
        this.additional_content_dom.innerHTML = this.support_ticket_dom_html;
        this.additional_content_dom.classList.add('input-group mb-3');
    }
};
// Handle Contact Submissions
function handle_contact_form_submit(e){
  e.preventDefault();
  this.names_node = document.getElementById('names')
  this.email_node = document.getElementById('email')
  this.cell_node = document.getElementById('cell')
  this.select_reason_node = document.getElementById('select_reason')
  this.subject_node = document.getElementById('subject')
  this.body_node = document.getElementById('body')
};
// Adding Document Onload Event Handlers to handle contact submissions and reasons selections
this.addEventListener('load', () => {
  document.getElementById('select_reason').addEventListener('click', on_selected_select_reason);
  document.getElementById('contact_form').addEventListener('submit', handle_contact_form_submit);
});
// Removing event handlers
document.addEventListener('close', () => {
  console.log('select reason');
  document.getElementById('select_reason').removeEventListener('click', on_selected_select_reason);
  document.getElementById('contact_form').removeEventListener('submit', handle_contact_form_submit);
});