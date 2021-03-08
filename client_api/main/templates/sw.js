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
const CACHE_NAME = 'FREELANCE-PROFILE';
// Customize this with a different URL if needed.

// TODO- use Flask Assets to bundle some of the adminLTE css files and js files togather,
// TODO- also bundle adminLTE Files with flask bundler...

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
'/static/js/adminlte.min.js','/static/css/adminlte.min.css','/static/css/ionicons.min.css','/static/plugins/fontawesome-free/css/all.min.css'];

let auth_token = "";



// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // // // //

// TODO= Refactor this code-- it must also contain background saving capabilities
// by syncing to the app.js for access to storage options



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

// let cache_store = [];

// let is_in_store = url => {
//   return cache_store.findIndex(store => store.url === url);
// }

// let add_to_store = (request,response) => {
//   if (is_in_store(request.url) < 0){
//     cache_store.push({
//       url:request.url,
//       response:response
//     });
//     console.log("pushed to memstore", cache_store.length);
//     return true;
//   }
//   return false;
// };

// let return_from_store = (url) => {
//   let index = is_in_store(url);
//   if(index > 0){
//     console.log("returning from memstore");
//     let c_store = cache_store[index];
//     console.log("what the hell", c_store);
//     return c_store.response;
//   }
//   return ""
// }

// // // // // // // // // // // // // // // // // // // // // // // // // // // // //

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    let cache = await caches.open(CACHE_NAME);
    // Setting {cache: 'reload'} in the new request will ensure that the response
    // isn't fulfilled from the HTTP cache; i.e., it will be from the network.
    await cache.addAll(CACHE_URLS);

  })());
});

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

self.addEventListener('fetch', (event) => {
  // We only want to call event.respondWith() if this is a navigation request
  // for an HTML page.

  let check_cache_hit = async event => {
    await caches.match(event.request).then(matched_response => {
      if (matched_response){return matched_response};
    });

    await mem_store.fetch_from_store(event.request.url).then(response => {
      return response
    });

    // console.log("matched response", matched_response);
  }

  // TODO- LOTS OF RESTRUCTURING CALLED FOR
  if (event.request.method == "POST"){
    console.log("post request");
    // TODO- add authorization
    event.respondWith((async () => {
      let response =  await handle_auth_headers(event);

      return response;
    })())
  }else{

    if (event.request.mode === 'navigate') {
      event.respondWith((async () => {
        try {
            // NOTE: its important to handle Auth here as the user is navigating to another page
            let cache_hit = await check_cache_hit(event);
            if (cache_hit){return cache_hit}

            let response =  await handle_auth(event);
            await mem_store.add_to_store(event.request.url,response);
            return response;
          } catch (error) {
            // an error occured
            return await fetch(event.request);
          }

        })());

    }else{
        event.respondWith((async () => {
          try{
            let cache_hit = await check_cache_hit(event);
            if (cache_hit){return cache_hit}

            let response = await fetch(event.request);
            await mem_store.add_to_store(event.request.url,response);
            return response;
          }catch(error){
            console.log("errors ", error.message)
            return await fetch(event.request);
          }
        })());
    }
  }

  // If our if() condition is false, then this fetch handler won't intercept the
  // request. If there are any other fetch handlers registered, they will get a
  // chance to call event.respondWith(). If no fetch handlers call
  // event.respondWith(), the request will be handled by the browser as if there
  // were no service worker involvement.
});

let handle_auth_headers = async event => {
  let headers = new Headers();
  event.request.headers.forEach((val, key) => {
    headers.append(key, val);
  });
  // Add ID token to header.
  headers.append("x-access-token", auth_token);

  let request = new Request(event.request.url, {
    method: event.request.method,
    headers: headers,
    mode: "same-origin",
    credentials: event.request.credentials,
    cache: event.request.cache,
    redirect:event.request.redirect,
    referrer: event.request.referrer,
    body: event.request.body,
    bodyUsed: event.request.bodyUsed,
    context: event.request.context
  });
  return await fetch(request);
}

// Message Dispatcher
// This handler should handle all communication from the app to the
// service worker -> from the service worker to the outside world
self.addEventListener('message', e => {
    if (e.data && e.data.type === "auth-token"){
      if (!auth_token){
        // console.log("setting token", e.data.token);
        auth_token = e.data.token;
      }else{
        // console.log("token already set",auth_token);
      }
    }
    console.log('Messages on service worker',e.data);
});

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



// Sync messages handlers

let sync_handler = e => {
  console.log("SYNC DISPATCHER", e);
};

self.addEventListener('sync', sync_handler);


