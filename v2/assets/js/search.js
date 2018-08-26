$(document).ready(function(){

	$("#search-btn").on("click", function(event){
		event.preventDefault();
		
		query = $("#search-box").val()
		if (query == ""){return;}
		alert("balls")
		runSearch(query)
	})
	
	function runSearch(query){
		alert("tits")
		$.ajax(
			"http://localhost:33041/search",
			{
				method: "post",
				data: {
					"query": query
				},
				success: function(){}
			}
		)
	}
	
	function parseResults(results){
		alert(results);
	}
})