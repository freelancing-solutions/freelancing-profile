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




// NOTE: Installing Service worker
self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    await caches.open(CACHE_NAME).then(cache => cache.addAll(CACHE_URLS));
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
  // self.clients.claim();
});

// Listening to fetch events to handle requests and Authorization

// TODO- consider using the fetch event handler to dispatch messages back to the page triggering the events
self.addEventListener('fetch', (event) => {

  // Checks if the request is included in our cache if yes returns the cached request
  let check_cache_hit = async event => {
    await caches.match(event.request).then(matched_response => {
      if (matched_response){return matched_response};

    });
    // await mem_store.fetch_from_store(event.request.url).then(response => {
    //   return response
    // });
    // console.log("matched response", matched_response);
  }

  // Ussually handling form data- Need to handle PUT, and DELETE
  if (event.request.method == "POST"){
    // NOTE- This handles adding auth headers to request
    event.respondWith((async () => await handle_auth_headers(event))())
  }else{

    // User Navigation Events
    if (event.request.mode === 'navigate') {
      // Handling events that are triggered by user navigating the website
      event.respondWith((async () => {
        try {
              // Return Preload or Cache or Create a fresh response
              return  await event.preloadResponse || await check_cache_hit(event) || await fetch(event.request);
              // return await handle_auth_headers(event)
          } catch (error) {
            // an error occured
            return await fetch(event.request);
          }
        })());
    }else{
        // Handling all other EVENTS - at this point DELETE PUT and etc EVENTS will end up here
        event.respondWith((async () => {
          try{
              // Return Preload or Cache or Create a fresh response
              // return  await event.preloadResponse || await check_cache_hit(event) || await handle_auth_headers(event)
              return await handle_auth_headers(event)
          }catch(error){
            console.log("errors ", error.message)
            return await fetch(event.request);
          }
        })());
    }
  }
});


// NOTE: This is where i actually insert auth headers
let handle_auth_headers = async event => {
  let headers = new Headers();
  event.request.headers.forEach((val, key) => {
    headers.append(key, val);
  });
  // Add ID token to header.
  headers.set("x-access-token", auth_token);
  console.log("Auth-Token Inserted on Headers : ", headers);

  let request = new Request(event.request.url, {
    method: event.request.method,
    headers: headers,
    mode: "no-cors",
    credentials: event.request.credentials,
    cache: event.request.cache,
    redirect:event.request.redirect,
    referrer: event.request.referrer,
    body: event.request.body,
    bodyUsed: event.request.bodyUsed,
    context: event.request.context
  });
  console.log("fetching this request");
  return await fetch(request);
}



//********************************************************************************************* */
// Message Dispatcher

let dispatch_message_to_sender = (e, message) =>  e.source.postMessage(message);

// This handler should handle all communication from the app to the
// service worker -> from the service worker to the outside world

let messages_handler = function(e){
  if (e.data && e.data.type === "auth-token"){
    if (!auth_token){
      // console.log("setting token", e.data.token);
      auth_token = e.data.token;
      dispatch_message_to_sender(e,{type: "auth-token",message: "Token-Received"})
    }else{
      dispatch_message_to_sender(e,{type: "auth-token",message: "Token-Already-Set"})
    }
  }
  console.log("Service Worker Receiving this message : ", e.data);
}

self.addEventListener('message', messages_handler);


//********************************************************************************************* *//
// PUSH Messages Handler

let push_handler = e => {
  console.log("push dispatching here");
  // let json_message = e.data.json();
  // let blob_data = e.data.blob();
  let text_message = e.data.text();
  // console.log("json", json_message);
  // console.log("blob", blob_data);
  console.log('text message', text_message);
};

// TODO- dispatch PUSH Messages to App.js push message handler
// The handler should decipher the message and decide as to where its destined
self.addEventListener('push', push_handler);



//********************************************************************************************* */
// Sync messages handlers

let sync_handler = e => {
  console.log("SYNC DISPATCHER", e);
};

self.addEventListener('sync', sync_handler);


