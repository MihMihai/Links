const friends = {};
var imageEndpoint = "http://linkspeople.ddns.net/image/";

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
// place is friends-list or random-list
function createFriend(socket,imgSrc,name,friendshipId,place){
	var friendsList = place || "friends-list";
	var h6 = $("<h6></h6>").text(name);
	var button = $("#button_remove_friend").clone(true);
	
	button.click(function(event){
		//personalize modal
		$("#removeFriend.modal_title").text("Delete" + name + "?");
		if(place !== "random-list")
			remove(socket,name,friendshipId,0);
		else
			remove(socket,name,0,friendshipId);
		$("#removeFriend").modal("show");
		event.stopPropagation();
	});
	var imageFriend;
	if(place !== "random-list")
		imageFriend = imageEndpoint + imgSrc;
	else
		imageFriend = imgSrc;
	var img = $('<img />', {
		src: '' + imageFriend, //imageEndpoint is declared in chat.js
		alt: 'User Avatar',
		class: 'img-circle'
	});
	
	img.click(function(){
		
		$("#profile_nameFriend").text(name);
		$("#profile_imageFriend").attr('src',imageEndpoint + imgSrc);
		
		$('#showStory').modal('show');
		$("#storyPost").empty();
		showStory(friendshipId,$("#storyPost"));
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
	$("#"+friendsList).prepend(a);
}

function remove(socket,name,friendshipId,random){
	
	if(random == 0) {		
		$("#form_remove").off("submit");
		$("#form_remove").on("submit",function(){
			socket.emit("remove friend",{"chat_token":localStorage.CHAT_TOKEN,"friendship_id":friendshipId});
			delete friends[friendshipId];
			$("#removeFriend").modal("hide");
			$("#friendName").text("CHAT");
			$("#messages").html("");
			document.getElementById("sendMessageButton").disabled = true;
			document.getElementById("messageInputBox").disabled = true;
		});
	}
	else {
		$("#form_remove").off("submit");
		$("#form_remove").on("submit",function(){
			$("[id='" + random + "']").remove(); //Complicatii cu $("#" + random) :((
			delete friends[random];
			$("#removeFriend").modal("hide");
			$("#friendName").text("");
			$("#messages").html("");
			document.getElementById("sendMessageButton").disabled = true;
			document.getElementById("messageInputBox").disabled = true;
		});
	}

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
	//}
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
