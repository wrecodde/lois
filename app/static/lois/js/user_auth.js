// send and process requests to server
let send_auth = function(auth_payload){
    $.ajax("/auth/signin",
   {
       method: "post",
       dataType: "json",
       data: auth_payload,
       success: eval_auth,
    })
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// evaluate auth message from server
let eval_auth = function(response, status, object){
	alert(JSON.stringify(response))
}

$("#auth_btn").on("click", function prep_auth(event){
	event.preventDefault();
	
    // collect data and send to server
    user_id = $("#user_id").val()
    user_key = $("#user_key").val()
    next = $("#next_pg_url").val()
    
    payload = {
        "user": {"id": user_id, "key": user_key},
    }
    
    send_auth("bola meat")
})