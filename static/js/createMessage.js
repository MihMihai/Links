function Message(msg,sender){
	this.msg = msg;
	this.sender = sender;
}

function createMessage(message, sender){
	let mesaj = $("<p>"+resizeMessage(message)+"</p>");
	let messageDiv = $("<div class='chat-body clearfix'></div>");
	let li = $("<li class='"+sender+" clearfix'></li>");
	messageDiv.append(mesaj);
	li.append(messageDiv);
	$("#messages").append(li);
	var chatBox = document.getElementById("chat_box");
	chatBox.scrollTop = chatBox.scrollHeight;
}

function resizeMessage(message){
	let messages = message.split(" ");
	for(let i=0; i<messages.length; i++){
		if(messages[i].length > 40) {
			let copyMsg = messages[i];
			messages.splice(i,1);
			for(let j=0;j<copyMsg.length;j+=20){
			//let half2 = messages[i].substr(messages[i].length/2+1, messages[i].length);
			messages.splice(i+j/20,0,copyMsg.substr(j,20));
			}
			i=i+copyMsg.length/20+1;
		}
		
	}
	return messages.join(" ");
}