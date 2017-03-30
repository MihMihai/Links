const messagesNotificationsIntervals = {};

function createMessageNotification(friendshipID){
	let friend = document.getElementById(friendshipID);
	let heading = friend.getElementsByTagName("h6");
	$(heading).after("<span class='glyphicon glyphicon-envelope'></span>");
	//heading[0].innerHTML += "<span class='glyphicon glyphicon-envelope'></span>";
}

function removeMessageNotification(friendshipID){
	let friend = document.getElementById(friendshipID);
	let spans = friend.getElementsByTagName("span");
	$(spans[1]).remove();
	
}

function removeNotificationInterval(friendshipID){
	clearInterval(messagesNotificationsIntervals[friendshipID]);
	delete messagesNotificationsIntervals[friendshipID];
}