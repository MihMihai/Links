window.onload = function(){


	var socket = io.connect('http://188.27.105.45/chat');
	
	$("#buton").click(function(){
		var message = document.getElementById("inputBox").value;
		console.log(message);
		 socket.emit('my event', {data: message});

	});

	 socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

	socket.on('message',function(msg) {
		console.log(msg);

		 document.getElementById("showBox").value = msg;
	});



	var months = [ "January", "February", "March", "April", "May", "June", 
	"July", "August", "September", "October", "November", "December" ];
	console.log(localStorage.TOKEN);
	
	$.ajax({
		method: "GET",
		url: "http://188.27.105.45/api/profile",
		headers: {Authorization: localStorage.TOKEN},
		dataType: "json",
		success:  function(data){
			$("#profile_name").html(data.name);
			$("#settings_name").val(data.name);
			var birthDate = data.birthday_date.split("-");
			$("#birthDay option:contains("+ birthDate[2] + ")").attr('selected', 'selected');
			$("#birthMonth option:contains("+ months[parseInt(birthDate[1])-1] + ")").attr('selected', 'selected');
			$("#birthYear option:contains("+ birthDate[0] + ")").attr('selected', 'selected');
		}
	});
	
	$("#logout").click(function(){
		$.ajax({
			method: "POST",
			url: "http://188.27.105.45/api/logout",
			headers: {Authorization: localStorage.TOKEN},
			dataType: "json",
			success:  function(data){
				localStorage.removeItem('TOKEN');
			}
		});
	});
	
	$('#form_update').validator().on('submit', function (event) {
		if (event.isDefaultPrevented()) {
			// handle the invalid form...
		} else {
			event.preventDefault();
			$.ajax({
				method: "POST",
				url: "http://188.27.105.45/api/update",
				headers: {Authorization: localStorage.TOKEN},
				data: {name: $("#settings_name").val(),
				birth_day: $("#birthDay").find(":selected").text(),birth_month: $("#birthMonth").find(":selected").text(),birth_year: $("#birthYear").find(":selected").text()},
				dataType: "json",
				success:  function(data){
					$('#settings').modal('hide');
					$("#profile_name").html($("#settings_name").val());
				}
			});
		}
	});

	$('#form_password').validator().on('submit', function (event) {
		if (event.isDefaultPrevented()) {
			// handle the invalid form...
		} else {
			event.preventDefault();
			$.ajax({
				method: "POST",
				url: "http://188.27.105.45/api/update",
				headers: {Authorization: localStorage.TOKEN},
				data: {password: $("#settings_password").val()},
				dataType: "json",
				success:  function(data){
					$("#settings_password").val("");
					$("#settings_password2").val("");
					$('#settings').modal('hide');
				}
			});
		}
	});

	
}

