window.onload = function(){
	
	console.log(localStorage.TOKEN);
	$.ajax({
		method: "GET",
		url: "http://188.27.105.45/api/profile",
		headers: {Authorization: localStorage.TOKEN},
		dataType: "json",
		success:  function(data){
			$("#profile_name").html(data.name);
			console.log(data.name);
		}
	});
}