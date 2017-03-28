var login_button;
var register_button;

window.onload = function(){
	$('.modal').on('hidden.bs.modal', function(){
		$(this).find('form')[0].reset();
	});

	$("#forgot_pass").click(function(){
		window.location.replace("http://linkspeople.ddns.net/forgot-password/");
	});
	
	/*login_button = document.getElementById("login_button").onclick = function(){
		event.preventDefault();
		$.post("http://188.27.105.45/api/login", {email: $("#login_email").val(), password: $("#login_password").val()}, function(data){
		console.log(data);
		}, "json")
		.fail(function() {
		alert( "error" );
	});};
	register_button = document.getElementById("register_button").onclick = function(event){
		event.preventDefault();
		$.post("http://188.27.105.45/api/signup", {name:$("#register_name").val(), email: $("#register_email").val(), password: $("#register_password").val(),
			birth_day: $("#birthDay").find(":selected").text(),birth_month: $("#birthMonth").find(":selected").text(),birth_year: $("#birthYear").find(":selected").text()}, function(data){
			console.log(data);
		}, "json")
		.fail(function() {
			alert( "error" );
		});};*/
		
		$('#form_login').validator().on('submit', function (event) {
			if (event.isDefaultPrevented()) {
				// handle the invalid form...
			} else {
				event.preventDefault();
				$.post("http://188.27.105.45/api/login", {email: $("#login_email").val(), password: $("#login_password").val()}, function(data){
					localStorage.setItem("TOKEN",data["access_token"]);
					localStorage.setItem("EMAIL",$("#login_email").val());
					console.log(localStorage.TOKEN);
					window.location.replace("http://linkspeople.ddns.net/chat/");
				}, "json")
				.fail(function() {
					$("#login_error").html("<p style='color:red;'>Invalid email or password!</p>");
				});
			}
		});
		
		$('#form_register').validator().on('submit', function (event) {
			if (event.isDefaultPrevented()) {
				// handle the invalid form...
			} else {
				event.preventDefault();
				$.post("http://188.27.105.45/api/signup", {name:$("#register_name").val(), email: $("#register_email").val(), password: $("#register_password").val(),
					birth_day: $("#birthDay").find(":selected").text(),birth_month: $("#birthMonth").find(":selected").text(),birth_year: $("#birthYear").find(":selected").text()}, function(data){
						console.log(data);
						$('#register').modal('hide');
					}, "json")
				.fail(function() {
					$("#register_mail_error").html("<p style='color:red;'>This email is already taken!</p>");
				});
			}
		});
		
		
	}


