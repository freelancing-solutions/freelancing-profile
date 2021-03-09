// // Handle reason selection
// function on_selected_select_reason(e){
//     this.freelance_job_dom_html = `
//     <div class="input-group mb-3">
//         <div class="input-group-prepend">
//                 <span class="input-group-text"> Freelance Job ID</span>
//         </div>
//         <input type="text" class="form-control" placeholder="Job ID" id="freelance_job_id">
//     </div>
//     `;
//     this.support_ticket_dom_html = `
//     <div class="input-group mb-3">
//       <div class="input-group-prepend">
//         <span class="input-group-text">Support Ticket Type</span>
//       </div>
//       <select class="form-control" id="support_ticket_type">
//         <option value="" selected="selected">--Select Ticket Type---</option>
//         <option value="payments">Payments</option>
//         <option value="refund">Refund</option>
//         <option value="freelance-job">Freelance Job</option>
//         <option value="website-functionality">Website Functionality</option>
//       </select>
//     </div>`;

//     this.additional_content_dom = document.getElementById('additional_content');
//     this.additional_content_dom.innerHTML = '';

//     if (e.target.value == 'freelance-jobs'){
//        this.additional_content_dom.innerHTML = this.freelance_job_dom_html;
//        this.additional_content_dom.classList.add('input-group mb-3');
//     }

//     if (e.target.value == 'support-ticket'){
//         this.additional_content_dom.innerHTML = this.support_ticket_dom_html;
//         this.additional_content_dom.classList.add('input-group mb-3');
//     }
// };
// // Handle Contact Submissions
// function handle_contact_form_submit(e){
//   e.preventDefault();
//   this.names_node = document.getElementById('names')
//   this.email_node = document.getElementById('email')
//   this.cell_node = document.getElementById('cell')
//   this.select_reason_node = document.getElementById('select_reason')
//   this.subject_node = document.getElementById('subject')
//   this.body_node = document.getElementById('body')
// };
// // Adding Document Onload Event Handlers to handle contact submissions and reasons selections
// this.addEventListener('load', () => {
//   document.getElementById('select_reason').addEventListener('click', on_selected_select_reason);
//   document.getElementById('contact_form').addEventListener('submit', handle_contact_form_submit);
// });
// // Removing event handlers
// document.addEventListener('close', () => {
//   console.log('select reason');
//   document.getElementById('select_reason').removeEventListener('click', on_selected_select_reason);
//   document.getElementById('contact_form').removeEventListener('submit', handle_contact_form_submit);
// });

(function(){

  let contact_form = {
      uid : '',
      names : '',
      email : '',
      reason : '',
      freelance_job_id : '',
      support_ticket_type : '',
      subject : '',
      body : '',
      access_token : localStorage.getItem('x-access-token'), // Learn how to put this in for JWT
      url : '/api/v1/contact',
      init_form : async function(){

          await this.cachedDom();
          await this.attach_handlers();

      }, // end init_form

      cachedDom: async function(){
        this.names = document.getElementById('names');
        this.email = document.getElementById('email');
        this.reason = document.getElementById('reason');
        this.subject = document.getElementById('subject')
        this.body = document.getElementById('body');
        this.message = document.getElementById('message')
        return this
    }, // end cachedDom
    attach_handlers: async function(){
      document.getElementById('contact_form').addEventListener('submit', this.submit_message);
      document.getElementById('select_reason').addEventListener('click', this.switch_reason);
    }, // end attach event handlers

    check_errors: async function(){
      let results = {is_error: false, errors:{}}
      return results
    }, // end check_errors

    submit_message : async function(e){
      e.preventDefault();
      try{
        // let errors = await this.check_errors();
        // if (errors.is_error){
        //   throw new Error('There was an error checking form')
        // }
        let message = JSON.stringify({
          'uid': this.uid,
          'names': this.names.value,
          'email': this.email.value,
          'cell': this.cell.value,
          'reason': this.select_reason.value,
          'subject': this.subject.value,
          'body': this.body.value
        });
        let token = localStorage.getItem('x-access-token');
        let headers = {};
        if (token && (token !== "undefined") && (token !== "")){
          headers = new Headers({
            'Content-Type': 'application/json',
            'x-access-token' : localStorage.getItem('x-access-token')
          })
        }else{
          headers = new Headers({
            'Content-Type': 'application/json',
            'x-access-token' : localStorage.getItem('x-access-token')
          })
        }
        let init = {
          method : "POST",
          headers: headers,
          body: message,
          mode: "cors",
          credentials: "same-origin",
          cache: "no-cache",
        }

        let request = new Request('/contact',init);
        await fetch(request).then(response => {
          if (!response.ok){
            throw new Error('There was an error communicating with backend')
          }
          return response.json();
        }).then(json => {
            // Data has been sent inform the user
            console.log(json)
            message = "Successfully created message"
            // this.reset_form(message).then(response => console.log(response))
        })
      }catch(e){
          console.log('error : ', e.message)
      }
    }, // end submit_message
    switch_reason: function(e){
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

        console.log('switching dom', e.target.value);

        this.additional_content_dom = document.getElementById('additional_content');
        this.additional_content_dom.innerHTML = '';

        if (e.target.value == 'freelance-jobs'){
          this.additional_content_dom.innerHTML = this.freelance_job_dom_html;
          this.additional_content_dom.classList.add('input-group mb-3');
        }
        if (e.target.value == 'support-ticket'){
            this.additional_content_dom.innerHTML = this.support_ticket_dom_html;

        }
    } // end switch form
  }

  // initialize form
  contact_form.init_form()

})()