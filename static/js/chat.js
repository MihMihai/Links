var currentFriend;
var months = [ "January", "February", "March", "April", "May", "June", 
"July", "August", "September", "October", "November", "December" ];
var friendRequestsArray = [];
var ip = "86.121.87.213";
var currentTab;

window.onload = function(){

	setInterval(refreshTokenRequest,45000);

	let socket = io.connect("http://" + ip + "/chat");
	socket.emit("join",{"email":localStorage.EMAIL});

	$('#rightPanel>li>a').each(function() {
		$(this).css("height","100%")
			.css("color","white")
			.css("margin",0); 
			//la hover trebuie pus: #428bca;
	});
	
	var panelContent = document.getElementById("panelContent");
	AddFriend(socket,friendRequestsArray,panelContent);
	currentTab = "#addFriend";


socket.on("msg server",function(msg) {
	try{
		let obj = JSON.parse(msg);
		let email = obj.from;
		let mesaj = obj.msg;
		let friendshipID = findFriendshipIdByEmail(email);
		friends[friendshipID].messages.push(new Message(mesaj,"left"));
		if(currentFriend == friendshipID)
			createMessage(mesaj,"left");
		//create message notification in friends list
		else if(!(messagesNotificationsIntervals.hasOwnProperty(friendshipID))){
			messagesNotificationsIntervals[friendshipID] = setInterval(function(){
				createMessageNotification(friendshipID);
				setTimeout(function(){
					removeMessageNotification(friendshipID);
				},500);
			},1000);

		}
		$(document.getElementById("friends-list").getElementsByTagName("a")[0]).before($("#"+friendshipID));


	}
	catch(e){
		console.log("ERROR");
	}

});

socket.on("new friend request",function(msg){
	try {
		//alert("new friend request");
		let obj = JSON.parse(msg);
		let from = obj.from;
		let name = obj.name;
		let friendshipId = obj.friendship_id;
		friendRequestsArray.push(new FriendReq(name,from,friendshipId));
		if(currentTab == "#friendRequests")
			createFriendRequestManager(socket,name,from,friendshipId);
	}
	catch(e) {
		console.log("ERROR");
	}
});

socket.on("bad friend request",function(msg){
	alert(msg);
});

socket.on("status friend request",function(msg) {
	try  {
		let obj = JSON.parse(msg);
		if(obj.status == 1) {
			friends[obj.friendship_id] = new Friend(obj.name,obj.from);
			createFriend(socket,"http://placehold.it/50/FA6F57/fff&text=ME",obj.name,obj.friendship_id);
		}
	}
	catch(e) {
		console.log("ERROR -- status fr req");
	}
});

socket.on("friend removed",function(msg) {
	try {
		let obj = JSON.parse(msg);
		$("#" + obj.old_friendship_id).remove();
		//msg.message also available here
	}
	catch(e) {
		console.log("ERROR -- friend removed");
	}
});

socket.on("bad remove friend", function(msg) {
	try {
		alert(msg); //change this!! to modal/popup
	}
	catch(e) {
		console.log("ERROR -- bad remove friend");
	}
});


//send message
//friend is a hashmap of friends, the key is friendship_id, and it has email and name
//sendMessage is declared after window.onload
$("#sendMessageButton").click(function(){
	sendMessage(socket);
});

$("#messageInputBox").keypress(function(event){
	if(event.keyCode === 13)
		sendMessage(socket);
});




 $("#addFriend").click(function(){

	  AddFriend(socket,friendRequestsArray,panelContent);
	
 });
$("#friendRequests").click(function(){
	 ViewFriendRequests(socket,friendRequestsArray,panelContent);
	 
 });

 $("#widgets").click(function(){
	  Widgets(panelContent);
 });


$.ajax({
	method: "GET",
	url: "http://" + ip + "/api/profile",
	headers: {Authorization: localStorage.TOKEN},
	dataType: "json",
	success:  function(data){
		$("#profile_name").html(data.name);
		$("#settings_name").val(data.name);
		var birthDate = data.birthday_date.split("-");
		$("#birthDay option:contains("+ birthDate[2] + ")").attr('selected', 'selected');
		$("#birthMonth option:contains("+ months[parseInt(birthDate[1])-1] + ")").attr('selected', 'selected');
		$("#birthYear option:contains("+ birthDate[0] + ")").attr('selected', 'selected');
		localStorage.CHAT_TOKEN=data.chat_token;
	}
});

$.ajax({
			method: "GET",
			url: "http://" + ip + "/api/friend_requests",
			headers: {Authorization: localStorage.TOKEN},
			dataType: "json",
			success:  function(data){
					if(data.total > 0){
						for(let i=0;i<data.requests.length;i++){
							friendRequestsArray.push(new FriendReq(data.requests[i].name,data.requests[i].email,data.requests[i].friendship_id));
						}}}
		});

$.ajax({
	method: "GET",
	url: "http://" + ip + "/api/friends",
	headers: {Authorization: localStorage.TOKEN},
	dataType: "json",
	success:  function(data){
		if(data.total > 0){
			for(let i=0;i<data.friends.length;i++){
				friends[data.friends[i].friendship_id] = new Friend(data.friends[i].name,data.friends[i].email);
				createFriend(socket,"http://placehold.it/50/FA6F57/fff&text=ME",data.friends[i].name,data.friends[i].friendship_id);
			}
		}
	}
});

document.getElementById("searchFriendInput").addEventListener("input",searchInFriendsList);

setTimeout(getAllMessagesRequest,200);

$("#logout").click(function(){
	socket.emit("leave",{"email":localStorage.EMAIL});
	$.ajax({
		method: "POST",
		url: "http://" + ip + "/api/logout",
		headers: {Authorization: localStorage.TOKEN},
		dataType: "json",
		success:  function(data){
			localStorage.removeItem('TOKEN');
			localStorage.removeItem('CHAT_TOKEN');
			localStorage.removeItem('EMAIL');
			window.location.replace("http://linkspeople.ddns.net/");
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
				url: "http://" + ip + "/api/update",
				headers: {Authorization: localStorage.TOKEN},
				data: {name: $("#settings_name").val(),
				birth_day: $("#birthDay").find(":selected").text(),birth_month: $("#birthMonth").find(":selected").text(),birth_year: $("#birthYear").find(":selected").text()},
				dataType: "json",
				success:  function(data){
					$('#updateAccount').modal('hide');
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
				url: "http://" + ip + "/api/update",
				headers: {Authorization: localStorage.TOKEN},
				data: {password: $("#settings_password").val()},
				dataType: "json",
				success:  function(data){
					$("#settings_password").val("");
					$("#settings_password2").val("");
					$('#changePass').modal('hide');
				}
			});
		}
	});

function refreshTokenRequest(){
	$.ajax({
		method: "GET",
		url: "http://" + ip + "/api/refresh_token",
		headers: {Authorization: localStorage.TOKEN},
		dataType: "json",
		success:  function(data){
			localStorage.TOKEN = data.access_token;

		}
	});
}

function sendMessage(socket){
	if(!(/^\s*$/.test($("#messageInputBox").val()))){
		createMessage($("#messageInputBox").val(),"right");
		let jsonObj = {"to":friends[currentFriend].email,"from":localStorage.EMAIL,"msg":$("#messageInputBox").val()};
		let jsonString = JSON.stringify(jsonObj);
		socket.emit("msg user", jsonString);
		friends[currentFriend].messages.push(new Message($("#messageInputBox").val(),"right"));
		$("#messageInputBox").val("");
		$(document.getElementById("friends-list").getElementsByTagName("a")[0]).before($("#"+currentFriend));
	}
}

function getAllMessagesRequest(){
	$.ajax({
		method: "GET",
		url: "http://" + ip + "/api/messages",
		headers: {Authorization: localStorage.TOKEN},
		dataType: "json",
		success:  function(data){
			if(data.total > 0){
				for(let index = 0; index< data.conversations.length;index++){
					let friendshipID = findFriendshipIdByEmail(data.conversations[index].with);
					for(let j = 0; j< data.conversations[index].messages.length;j++)
						friends[friendshipID].messages.push(new Message(data.conversations[index].messages[j].message,
							data.conversations[index].messages[j].sender));
				}
			}
		}
	});
}
}
