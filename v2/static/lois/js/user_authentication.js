// send and process requests to server
let send_auth = function(auth_payload){
    $.ajax("/auth",
   {
       method: "post",
       dataType: "json",
       data: auth_payload,
       success: eval_auth,
    })
}

// evaluate auth message from server
let eval_auth = function(response, status, object){
	alert(JSON.stringify(response))
}

$("#auth-btn").on("click", function prep_auth(event){
	event.preventDefault();
	
    // collect data and send to server
    password = $("#auth-password").val()
    
    payload = {
        "auth_key": password,
        "next_page": next_page,
    }
    
    send_auth(payload)
})