from flask import escape, abort


def contact_endpoint(request):
    # For more information about CORS and CORS preflight requests, see
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    # for more information.

    # Set CORS headers for preflight requests
    if request.method == 'OPTIONS':
        # Allows GET requests from origin https://mydomain.com with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': 'https://www.pocket-money.site',
            'Access-Control-Allow-Methods': 'POST,GET,PUT,DELETE,OPTIONS',
            'Access-Control-Allow-Headers': 'Authorization, Origin, Accept, Content-Type, X-Requested-With, '
                                            'X-CSRF-Token',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return '', 204, headers
    else:
        pass

    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
    else:
        return {"status": False, "payload": {}, "error": "JSON is Invalid"}

    if request_json and 'uid' in request_json:
        uid = request_json['uid']
    else:
        return {"status": False, "payload": {}, "error": "User ID not specified"}

    if request_json and 'auth' in request_json:
        auth = request_json['auth']
    else:
        return {"status": False, "payload": {}, "error": "Request not Authorized"}

    if request.method == "GET":
        if request_json and "contact_id" in request_json:
            contact_id = request_json["contact_id"]
        else:
            return {"status": False, "payload": {}, "error": "Contact ID not specified"}

        if is_user(auth=auth) and (uid == auth):
            return Support().fetch_message_by_contact_id(uid=uid, contact_id=contact_id)
        else:
            return {"status": False, "payload": {}, "error": "Bad Request"}

    elif request.method == "PUT":
        uid = request_json["uid"]
        auth = request_json["auth"]
        if is_user(auth=auth) and (uid == auth):
            return Support().update_message(message=request_json)
        else:
            return {"status": False, "payload": {}, "error": "Bad Request"}

    elif request.method == "POST":
        uid = request_json["uid"]
        auth = request_json["auth"]
        if is_user(auth=auth) and (uid == auth):
            return Support().new_contact(contact=request_json)
        else:
            return {"status": False, "payload": {}, "error": "Bad Request"}

    elif request.method == "DELETE":
        uid = request_json["uid"]
        auth = request_json["auth"]
        contact_id = request_json["contact_id"]
        if is_user(auth=auth) and (uid == auth):
            return Support().remove_contact(contact_id=contact_id, uid=uid)
        else:
            return {"status": False, "payload": {}, "error": "Bad Request"}

    else:
        return {"status": False, "payload": {}, "error": "Bad Request"}
