function Message(msg,sender,date){
	this.msg = msg;
	this.sender = sender;
	this.date = date;
}

/*function Message(msg,sender) {
	this.msg = msg;
	this.sender = sender;
}
*/
// For todays date;
Date.prototype.today = function () { 
    return ((this.getDate() < 10)?"0":"") + this.getDate() +"-"+(((this.getMonth()+1) < 10)?"0":"") + (this.getMonth()+1) +"-"+ this.getFullYear();
}

// For the time now
Date.prototype.timeNow = function () {
     return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes() +":"+ ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
}

function createMessage(message, sender, date){
	
	if(date === null || date === undefined) {
		let currentDate = new Date();
		date = currentDate.today() + " " + currentDate.timeNow();
//		console.log(date);
	}
	
	let mesaj = $("<p data-toggle='tooltip' style='display: flex;' " +
		"data-placement='" + (sender === "left" ? "right" : "left") + "' title='" + date + "'>"+resizeMessage(message)+"</p>");
	let messageDiv = $("<div class='chat-body clearfix'></div>");
	let li = $("<li class='"+sender+" clearfix'></li>");

	//set up emojis
//	emojify.setConfig({tag_type:'div'});

	messageDiv.append(mesaj);
	li.append(messageDiv);
	$("#messages").append(li);

	emojify.run();
	emojify.replace(message);

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
