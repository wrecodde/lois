$(document).ready(function(){
	
	$("#search-btn").on("click", function(e){
		e.preventDefault();
		
		fdb = $("#feedback")
		
		q = $("#search-box").val();
		$.ajax("http://localhost:33041/search", 
			{method: "post",
			data: {"query": q, "scope": "internal"},
			success: function(data){
				r = JSON.parse(data)
				fdb.text(r["hits"])
			}
			})
	})
})