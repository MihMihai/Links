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
function createFriend(imgSrc,name,friendshipId){
	var h6 = $("<h6></h6>").text(name);
	var button = $("<button type='button' class='close pull-right clearfix'>&times;</button>");
	button.click(function(event){
		remove(name,friendshipId);
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

function remove(name,friendshipId){
	let result = window.confirm("Are you sure you want to delete "+ name+"?");
	if(result===true){
		$.ajax({
			method: "POST",
			url: "http://188.27.105.45/api/remove_friend",
			headers: {Authorization: localStorage.TOKEN},
			data: {friendship_id: friendshipId},
			dataType: "json",
			success:  function(data){
				$("#"+friendshipId).remove();
			}
		});
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