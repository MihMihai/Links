const friends = {};

function Friend(name, email){
	this.name = name;
	this.email = email;
	this.messages = [];
}
function findFriendshipIdByEmail(email){
	for(var key in friends){
		if (friends[key].email == email)
			return key;
	}
	return;
}
function createFriend(socket,imgSrc,name,friendshipId){
	var h6 = $("<h6></h6>").text(name);
	var button = $("#button_remove_friend");
	button.click(function(event){
		//personalize modal
		$("#removeFriend.modal_title").text("Delete" + name + "?");
		remove(socket,name,friendshipId);
		event.stopPropagation();
	});
	var img = $('<img />', {
		src: ''+imgSrc,
		alt: 'User Avatar',
		class: 'img-circle'
	});
	var span = $("<span class='chat-img pull-left'></span>");
	span.append(img);
	var a = $("<a id="+friendshipId+" href='#'' class='list-group-item'></a>");
	let notificationMessage = $("<span class='glyphicon glyphicon-envelope messageNotification'></span>");
	span.append(img);
	a.append(span);
	a.append(h6);
	a.append(notificationMessage);
	a.append(button);
	a.click(function(){
		connectToChat(name,friendshipId);
	})
	$("#friends-list").prepend(a);
}

function remove(socket,name,friendshipId){
	let confirm = false;

	$("#form_remove").on("submit",function(){
		confirm = true;
	})

	if(confirm===true){

		socket.emit("remove friend",{"chat_token":localStorage.CHAT_TOKEN,"friendship_id":friendshipId});
		delete friends[friendshipId];

/*		$.ajax({
			method: "POST",
			url: "http://" + ip + "/api/remove_friend",
			headers: {Authorization: localStorage.TOKEN},
			data: {friendship_id: friendshipId},
			dataType: "json",
			success:  function(data){
				$("#"+friendshipId).remove();
			}
		});*/
	}
}

function connectToChat(name,friendshipId){
	document.getElementById("sendMessageButton").disabled = false;
	document.getElementById("messageInputBox").disabled = false;
	$("#friendName").text(name);
	currentFriend = friendshipId;
	$("#messages").html("");
	loadMessagesInChatBox(friendshipId);
	removeNotificationInterval(friendshipId);

}

function loadMessagesInChatBox(friendshipId){
	for(let i=0;i<friends[friendshipId].messages.length;i++){
		createMessage(friends[friendshipId].messages[i].msg,friends[friendshipId].messages[i].sender)
	}
}

function searchInFriendsList(){
	let name = $("#searchFriendInput").val().trim().toLowerCase();
	let friends = document.getElementById("friends-list").getElementsByTagName("a");

	for(let index = 0; index < friends.length; index++){
		let friend = friends[index].getElementsByTagName("h6");
		let friendName = friend[0].innerText;
		if(friendName.toLowerCase().indexOf(name)==-1)
			friends[index].style.display = "none";
		else 
			friends[index].style.display = "flex";
	}


}
