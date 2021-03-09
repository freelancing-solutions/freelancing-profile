/*
  Copyright 2015, 2019 Google Inc. All Rights Reserved.
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/

// Incrementing OFFLINE_VERSION will kick off the install event and force
// previously cached resources to be updated from the network.
const OFFLINE_VERSION = 1;
const CACHE_NAME = 'FREELANCE-PROFILESS';
const website_base_url = 'http://localhost';
// Customize this with a different URL if needed.

// TODO- use Flask Assets to bundle some of the adminLTE css files and js files togather,
// TODO- also bundle adminLTE Files with flask bundler...


// NOTE- Never Cache URLS that require Authorization
const CACHE_URLS = [
  '/','/about','/contact','/blog','/projects','/privacy-policy',
  '/terms-of-service','/learn-more/frontend-development','/learn-more/backend-development',
  '/hire-freelancer', '/hire-freelancer/how-to/create-freelancing-account',
  '/hire-freelancer/how-to/submit-freelance-jobs','/hire-freelancer/how-to/download-install-slack',
  '/hire-freelancer/how-to/download-install-teamviewer','/hire-freelancer/how-to/create-a-github-account',
  '/hire-freelancer/how-to/create-a-gcp-developer-account','/hire-freelancer/how-to/create-a-heroku-developer-account',
  '/hire-freelancer/expectations/communication-channels-procedures','/hire-freelancer/expectations/payments-procedures-methods',
  '/hire-freelancer/expectations/due-diligence','/hire-freelancer/expectations/handing-over-procedures','/hire-freelancer/expectations/maintenance-procedures',
  '/static/plugins/jquery/jquery.min.js','/static/plugins/bootstrap/js/bootstrap.bundle.min.js','/static/js/handlebars.js',
  '/static/js/adminlte.min.js','/static/css/adminlte.min.css','/static/css/ionicons.min.css','/static/plugins/fontawesome-free/css/all.min.css'
];


// ***********************************************************************************************//
// Global Variable to hold the value of the authorization token
let auth_token = "";

// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // // // //
// TODO= Refactor this code-- it must also contain background saving capabilities
// by syncing to the app.js for access to storage options


// NOTE: Learn how best to use this data store or remove it
let mem_store  ={
  _cache_store : [],

  init : function(){
    // initialize the store
    this.sync_from_storage(CACHE_NAME).catch(response => {
      response.forEach(cache_item => {
        this.add_to_store(cache_item.url,cache_item.response).then(response => {
          console.log("created new storage item ", response)
        })
      })
    }).catch(error => {
      console.log("error catching from storage :", error.message);
    })
  },
  is_in_store: async function( url){

    return this._cache_store.findIndex(store => store.url === url);
  },

  add_to_store: async function(url,response){
    this.is_in_store(url).then(index => {
      if (index < 0){
        this._cache_store.push({url,response})
      }
    })
  },

  fetch_from_store: async function( url){
    this.is_in_store(url).then(index => {
      if (index > 0){
        return this._cache_store[index]
      }
      return ""
    })
  },

  sync_to_storage: async function(){

  },

  sync_from_storage: async function(cache){

  },
}

mem_store.init(); 

let cache = self.caches;


// NOTE: Installing Service worker
self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    await cache.open(CACHE_NAME).then(cache => cache.addAll(CACHE_URLS));
  })());
});

// Activating Worker
self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    // Enable navigation preload if it's supported.
    // See https://developers.google.com/web/updates/2017/02/navigation-preload
    if ('navigationPreload' in self.registration) {
      await self.registration.navigationPreload.enable();
    }
  })());

  // Tell the active service worker to take control of the page immediately.
  self.clients.claim();
});

// Listening to fetch events to handle requests and Authorization

// TODO- consider using the fetch event handler to dispatch messages back to the page triggering the events
self.addEventListener('fetch', (event) => {

  // Checks if the request is included in our cache if yes returns the cached request
  let check_cache_hit = async event => {  
    let matched_response = cache.match(event.request);
    if (matched_response){return matched_response}else{await cache.add(event.request); return false}
  }
          // handling fetch events
          request_url = String(event.request.url);
          // console.log('request url', request_url);

          if (event.request.method == "POST"){
            // NOTE- This handles adding auth headers to request
            return event.respondWith( (async () => await fetch(event.request))())
          }
          if  (event.request.method == "DELETE"){
            // NOTE- This handles adding auth headers to request
            return event.respondWith( (async () => await fetch(event.request))())
          }
          if (event.request.method == "PUT"){
            // NOTE- This handles adding auth headers to request
            return event.respondWith( (async () => await fetch(event.request))())
          }
          // if its service worker request fetch a fresh copy
          if  ((event.request.method == "GET") && (request_url.includes('sw.js'))) {
            return event.respondWith( (async () => await fetch(event.request))())
          }
          // if its for static assets fetch first from cache if failed fetch fresh copy
          if ((event.request.method == "GET") && (request_url.includes('static'))){
            return event.respondWith((async () => {return  await event.preloadResponse || await check_cache_hit(event) || await fetch(event.request)})())
          }
          // if its a GET request to another domain fetch a fresh copy
          // if its service worker request fetch a fresh copy
          if ((event.request.method == "GET") && (!request_url.includes(website_base_url))){
            return event.respondWith( (async () => await fetch(event.request))())
          }
          // all other requests fetch securely from backend
          return event.respondWith((async () => {return  await handle_auth_headers(event)})())
});


// NOTE: This is where i actually insert auth headers
let handle_auth_headers = async event => {
  let headers = new Headers();
  event.request.headers.forEach((val, key) => {
    headers.append(key, val);
  });
  // Add ID token to header.
  headers.append("x-access-token", auth_token);
  console.log("Auth-Token Inserted on Headers : ", auth_token);
  // always user cors in order to enable headers modification
  let request = new Request(event.request.url, {
    method: event.request.method,
    headers: headers,
    mode: "cors",
    credentials: event.request.credentials,
    cache: event.request.cache,
    redirect:event.request.redirect,
    referrer: event.request.referrer,
    body: event.request.body,
    bodyUsed: event.request.bodyUsed,
    context: event.request.context
  });
  console.log("fetching this request securely", request.url);
  return await fetch(request);
}

//********************************************************************************************* */
// Message Dispatcher
let messaging = {

  // This handler should handle all communication from the app to the
  // service worker -> from the service worker to the outside world
  messages_handler : function(e){
    this.dispatch_message_to_sender = function(e, message){e.source.postMessage(message)};

    if (e.data && e.data.type === "auth-token"){
        // console.log("setting token", e.data.token);
      auth_token = e.data.token;
      if ((auth_token !== "") && (auth_token !== "undefined")){
        this.dispatch_message_to_sender(e,{type: "auth-token",message: "Token-Received"})
      }else{
        auth_token = "";
        this.dispatch_message_to_sender(e,{type: "auth-token",message: "Not-Logged-IN"})
      }
    }
    console.log("Service Worker Receiving this message : ", e.data);
  },


  //********************************************************************************************* *//
  // PUSH Messages Handler
  push_handler : function(e){
    console.log("push dispatching here");
    // let json_message = e.data.json();
    // let blob_data = e.data.blob();
    let text_message = e.data.text();
    // console.log("json", json_message);
    // console.log("blob", blob_data);
    console.log('text message', text_message);
  },

  // TODO- dispatch PUSH Messages to App.js push message handler
  // The handler should decipher the message and decide as to where its destined
  //********************************************************************************************* */
  // Sync messages handlers
  sync_handler : function(e){
    console.log("SYNC DISPATCHER", e);
  },

  init : function(){
    self.addEventListener('message', this.messages_handler);
    self.addEventListener('sync', this.sync_handler);
    self.addEventListener('push', this.push_handler)
  }
}

messaging.init();