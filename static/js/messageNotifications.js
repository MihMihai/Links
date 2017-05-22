const messagesNotificationsIntervals = {};

function createMessageNotification(friendshipID){
	let friend = document.getElementById(friendshipID);
	let messageNotifications = friend.getElementsByClassName("messageNotification");
	messageNotifications[0].style.visibility = "visible";
}

function removeMessageNotification(friendshipID){
	let friend = document.getElementById(friendshipID);
	let messageNotifications = friend.getElementsByClassName("messageNotification");
	messageNotifications[0].style.visibility = "hidden";
}

function removeNotificationInterval(friendshipID){
	clearInterval(messagesNotificationsIntervals[friendshipID]);
	delete messagesNotificationsIntervals[friendshipID];
}