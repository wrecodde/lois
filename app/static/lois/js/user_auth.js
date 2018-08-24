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

// evaluate auth message from server
let eval_auth = function(response, status, object){
	alert(JSON.stringify(response))
}

$("#auth_btn").on("click", function prep_auth(event){
	event.preventDefault();
	
    // collect data and send to server
    user_id = $("#user_id").val()
    user_key = $("#user_key").val()
    next_page = $("#next_pg_url").val()
    
    payload = {
        "user": "burger",
        "next_page": next_page,
    }
    
    send_auth(payload)
})