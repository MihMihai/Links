const messagesNotificationsIntervals = {};

function createMessageNotification(friendshipID){
	let friend = document.getElementById(friendshipID);
	let messageNotifications = document.getElementsByClassName("messageNotification");
	for(let index = 0; index< messageNotifications.length; index++){
		messageNotifications[index].style.visibility = "visible";
	}

	
}

function removeMessageNotification(friendshipID){
	let friend = document.getElementById(friendshipID);
	let messageNotifications = document.getElementsByClassName("messageNotification");
	for(let index = 0; index< messageNotifications.length; index++){
		messageNotifications[index].style.visibility = "hidden";
	}
}

function removeNotificationInterval(friendshipID){
	clearInterval(messagesNotificationsIntervals[friendshipID]);
	delete messagesNotificationsIntervals[friendshipID];
}