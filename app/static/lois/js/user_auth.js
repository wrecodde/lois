$("#signup_btn").on("click", function(event){
    event.preventDefault();
    
    data = 
    payload = {
       "user": JSON.stringify({
            "email": $("#user_email").val(),
            "username": $("#username").val(),
            "password": $("#user_password").val()
    })
<<<<<<< HEAD
    }
    
   $.ajax({
       url: "/auth/signup",
       method: "post",
       data: payload,
       success: eval_signup_response,
       error: server_error,
   })
})

$("#signin_btn").on("click", function(event){
    event.preventDefault();
    
    payload = {
        "user": JSON.stringify({
            "email": $("#user_email").val(),
            "password": $("#user_password").val()
        })
    }
    
   $.ajax({
       url: "/auth/signin",
       method: "post",
       data: payload,
       success: eval_signin_response,
       error: server_error,
   })
})

// send app messages to user as feedback
let send_feedback = function(msg, err_level="normal"){
    feedback_box = $("#feedback");

    if (err_level == "danger"){
        feedback_box.css("color", "red")
    }

    feedback_box.text(msg);
}

let eval_signup_response = function(response, status, object){
    console.log(response)
}

// evaluate auth message from server
let eval_signin_response = function(response, status, object){
	console.log(response)
}

// handle server errors
let server_error = function(msg){
    send_feedback("something went wrong. we're fixing it.")
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
=======
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
>>>>>>> new-branch
