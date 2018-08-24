$(document).ready(function(){

$("#fetchBtn").on("click", makeQuery);

let feedback = $("#feedback");

function makeQuery(e){
	e.preventDefault();
	var query = $("input#queryBox").val().toLowerCase();
	
	feedback.text("fetching...");
	$.get("/search", {"query":query}, renderHits);
}

function renderHits(response){
	r = JSON.parse(response)
	
	if (r.error){
		feedback.text("no internet connection");
		return;
	}
	
	feedback.text("");
	canvas = $("#resultsBox");
	
	r.hits.forEach(function(hit){
		// cant get the nasty button working
		return
	});
}

// close doc.ready()
});