$(document).ready(function(){

$(".saveBtn").on("click", function(){
	var target = $(this).val();
	var feedback = $(this).siblings(".saveStatus");
	$.get("/save", {"story_url":target}, function(){feedback.text("saving")}).
		done(function(){
			feedback.addClass("text-success")
			feedback.text("saved")}).
		fail(function(){
			feedback.addClass("text-danger")
			feedback.text("failed")});
});


$(".deleteBtn").on("click", function(){
	var trash = confirm("trash this story?")
	if (trash){
		var story_id = $(this).val()
		$.ajax(story_id, {method: "delete", 
		complete: function(){window.location="/stories"}
		});
	}else{
		return
	}
});

$("#closeBtn").on("click", function(){
	$.ajax("/auth", {method: "post", 
		data: {"session": "close"},
		complete: function(){window.location="/"}
		})
});

// close doc.ready()
});