var numberOfRandomFriends = 0;
function findRandomFriend(socket){	
	let jsonObj = {"chat_token":localStorage.CHAT_TOKEN};
	let jsonString = JSON.stringify(jsonObj);
	socket.emit("random chat",jsonString);
	console.log("da");
}