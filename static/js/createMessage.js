function Message(msg,sender){
	this.msg = msg;
	this.sender = sender;
}

function createMessage(message, sender){
	let mesaj = $("<p>"+message+"</p>");
	let messageDiv = $("<div class='chat-body clearfix'></div>");
	let li = $("<li class='"+sender+" clearfix'></li>");
	messageDiv.append(mesaj);
	li.append(messageDiv);
	$("#messages").append(li);

}

