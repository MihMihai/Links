var currentFriend;
var months = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];
var friendRequestsArray = [];
var imageEndpoint = "http://linkspeople.ddns.net/image/";
var currentTab;
var base64Image;
const ip = "188.25.131.242";
const linksDNS = "linkspeople.ddns.net"
var successFrRequest = "The friend request was send to acceptance/rejection! ";

function updateFriendReq() {
    if (friendRequestsArray.length > 0) {
        var number = friendRequestsArray.length.toString();
        $("#friendRequests>a").text("Friend requests " + number);
    } else $("#friendRequests>a").text("Friend requests");
}


$(document).ready(function() {
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });
});


window.onload = function() {

    $(window).unload(function() {
        socket.emit("leave", { "email": localStorage.EMAIL });
        
    });

    //refreshTokenRequest();

    $(".modal").on("show.bs.modal", function() {
        $("body").css("overflow-y", "hidden");
    });

    $(".modal").on("hide.bs.modal", function() {
        $("body").css("overflow-y", "initial");
    });


    updateFriendReq();

    setInterval(refreshTokenRequest, 45000);

    let socket = io.connect("http://" + linksDNS + "/chat");
	
	
	socket.on("details", function(data) {
        	let obj = JSON.parse(data);
			localStorage.setItem("TOKEN",obj.access_token);
			localStorage.setItem("EMAIL",obj.email);
			console.log(localStorage.TOKEN);

			socket.emit("join",{"email":localStorage.EMAIL});
			getProfile();
			getFriends();
			getFriendsRequests();
			getStory();
			setTimeout(getAllMessagesRequest,200);

   	 });
	
	
    //socket.emit("join", { "email": localStorage.EMAIL });

    socket.on("user join", function(data) {

        let friend = document.getElementById(data.friendship_id);
        friend.style.color = "#5cb85c";
        $(document.getElementById("friends-list").getElementsByTagName("a")[0]).before(friend);
    });

    socket.on("user left", function(data) {
        let friend = document.getElementById(data.friendship_id);
        friend.style.color = "black";
        $(document.getElementById("friends-list").getElementsByTagName("a")[document.getElementById("friends-list").getElementsByTagName("a").length - 1]).after(friend);
    });


    socket.on("random chat token", function(msg) {
        numberOfRandomFriends++;

        let obj = JSON.parse(msg);
        friends[obj.random_token] = new Friend();
        createFriend(socket, "http://placehold.it/50/FA6F57/fff&text=ME", "Random " + numberOfRandomFriends, obj.random_token, "random-list");
    });

    $("#randomFriendButton").click(function() {
        findRandomFriend(socket);
    });


    socket.on("msg server", function(msg) {
        try {
            let obj = JSON.parse(msg);

            if ('random_token' in obj) {
                let from = obj.from;
                let msg = obj.msg;
                //let date = obj.date; --- nu are date

				let currentDate = new Date();
				date = currentDate.today() + " " + currentDate.timeNow();
                friends[from].messages.push(new Message(msg, "left",date));
                let friendshipID = from;
                if (currentFriend == from) {
                    createMessage(msg, "left",date);
                } else if (!(messagesNotificationsIntervals.hasOwnProperty(friendshipID))) {
                    messagesNotificationsIntervals[friendshipID] = setInterval(function() {
                        createMessageNotification(friendshipID);
                        setTimeout(function() {
                            removeMessageNotification(friendshipID);
                        }, 500);
                    }, 1000);

                }
                $(document.getElementById("random-list").getElementsByTagName("a")[0]).before($("#" + friendshipID));
            } else {
                let email = obj.from;
                let mesaj = obj.msg;
				let date = obj.date;
                friendshipID = findFriendshipIdByEmail(email);
                friends[friendshipID].messages.push(new Message(mesaj, "left",date));
                if (currentFriend == friendshipID)
                    createMessage(mesaj, "left",date);
                //create message notification in friends list
                else if (!(messagesNotificationsIntervals.hasOwnProperty(friendshipID))) {
                    messagesNotificationsIntervals[friendshipID] = setInterval(function() {
                        createMessageNotification(friendshipID);
                        setTimeout(function() {
                            removeMessageNotification(friendshipID);
                        }, 500);
                    }, 1000);

                }
                $(document.getElementById("friends-list").getElementsByTagName("a")[0]).before($("#" + friendshipID));
            }

        } catch (e) {
            console.log("ERROR");
        }

    });



   //
   
//
    var panelContent = document.getElementById("panelContent");
    AddFriend(socket, friendRequestsArray, panelContent);
    currentTab = "#addFriend";



    socket.on("new friend request", function(msg) {
        try {
            //alert("new friend request");
            let obj = JSON.parse(msg);
            let from = obj.from;
            let name = obj.name;
            let friendshipId = obj.friendship_id;
            let avatar = obj.avatar;
            friendRequestsArray.push(new FriendReq(name, from, friendshipId, avatar));

            updateFriendReq();

            if (currentTab == "#friendRequests")
                createFriendRequestManager(socket, name, from, friendshipId, avatar);
        } catch (e) {
            console.log("ERROR");
        }
    });



    socket.on("status friend request", function(msg) {
        try {
            let obj = JSON.parse(msg);
            if (obj.status == 1) {
                friends[obj.friendship_id] = new Friend(obj.name, obj.from);
                createFriend(socket, obj.avatar, obj.name, obj.friendship_id);
            }
        } catch (e) {
            console.log("ERROR -- status fr req");
        }
    });

    socket.on("friend request sent", function(msg) {
        //      let successFrRequest = "The friend request was send to acceptance/rejection!";
        $("#frRequestResponse").html(successFrRequest);
        $("#sendFriendReq").modal("show");

    });

    socket.on("bad friend request", function(msg) {
        $("#frRequestResponse").html(msg);
        $('#sendFriendReq').modal('show');
    });
    /*  
        $('#sendFriendReq').on("hidden.bs.modal",function() {
            $("#frRequestResponse").html(successFrRequest);
        });

    */
    socket.on("friend removed", function(msg) {
        try {
            let obj = JSON.parse(msg);
            $("#" + obj.old_friendship_id).remove();
            //msg.message also available here
        } catch (e) {
            console.log("ERROR -- friend removed");
        }
    });

    socket.on("bad remove friend", function(msg) {
        try {
            alert(msg); //change this!! to modal/popup
        } catch (e) {
            console.log("ERROR -- bad remove friend");
        }
    });


    //send message
    //friend is a hashmap of friends, the key is friendship_id, and it has email and name
    //sendMessage is declared after window.onload
    $("#sendMessageButton").click(function() {
        sendMessage(socket);
    });

    $("#messageInputBox").keypress(function(event) {
        if (event.keyCode === 13)
            sendMessage(socket);
    });




    $("#addFriend").click(function() {

        AddFriend(socket, friendRequestsArray, panelContent);

    });
    $("#friendRequests").click(function() {
        ViewFriendRequests(socket, friendRequestsArray, panelContent);

    });

    $("#widgets").click(function() {
        Widgets(panelContent);
    });


    //MOVED: Profile Request, Friends Request and FriendsRequests Request below, each in its function

    

    

    socket.on("join", function(msg) {
        try {
            //alert("new friend request");
            let obj = JSON.parse(msg);
            let from = obj.from;
            let name = obj.name;
            let friendshipId = obj.friendship_id;
            let avatar = obj.avatar;
            friendRequestsArray.push(new FriendReq(name, from, friendshipId, avatar));

            updateFriendReq();

            if (currentTab == "#friendRequests")
                createFriendRequestManager(socket, name, from, friendshipId, avatar);
        } catch (e) {
            console.log("ERROR");
        }
    });

    document.getElementById("searchFriendInput").addEventListener("input", searchInFriendsList);

    //setTimeout(getAllMessagesRequest, 200);

    $("#logout").click(function() {
        socket.emit("leave", { "email": localStorage.EMAIL });
        localStorage.removeItem('TOKEN');
        localStorage.removeItem('CHAT_TOKEN');
        localStorage.removeItem('EMAIL');
        
    });



    $('#form_update').validator().on('submit', function(event) {
        if (event.isDefaultPrevented()) {
            // handle the invalid form...
        } else {
            event.preventDefault();
            convertAndResizeImage("settings_photo", 50, 50, function(b) {
                base64Image = b;

                $.ajax({
                    method: "POST",
                    url: "http://" + ip + "/api/update",
                    headers: { Authorization: localStorage.TOKEN },
                    data: {
                        name: $("#settings_name").val(),
                        birth_day: $("#birthDay").find(":selected").text(),
                        birth_month: $("#birthMonth").find(":selected").text(),
                        birth_year: $("#birthYear").find(":selected").text(),
                        avatar: base64Image
                    },
                    dataType: "json",
                    success: function(data) {
                        $('#updateAccount').modal('hide');
                        $("#profile_name").html($("#settings_name").val());
                        if (base64Image !== undefined) {
                            $("#profile_image").attr('src', base64Image);
                        }
                        base64Image = undefined;
                    }
                });
            });
        }
    });



    $('#form_story').on('submit', function(event) {
        if (event.isDefaultPrevented()) {
            // handle the invalid form...
        } else {
            event.preventDefault();

            convertAndResizeImage("story_photoMy", 500, 500, function(b) {

                base64Image = b;
                console.log(base64Image);

                $.ajax({
                    method: "POST",
                    url: "http://" + ip + "/api/new_story",
                    headers: { Authorization: localStorage.TOKEN },
                    data: {
                        text: $("#story_status").val(),
                        feel: $("#story_feel").find(":selected").text(),
                        image: base64Image
                    },
                    dataType: "json",
                    success: function(data) {

                        
                        $("#story_status").val("");
                        $("#story_feel").val([]);
                        $("#story_photoMy").val("");
                        base64Image = undefined;

                         $("#addedStory").empty();
                        showStory(null, $('#addedStory'));
                        var deleteButton = $('<div class="wrapper"><button type="button" class="btn btn-danger btn-lg">Delete story</button></div>');

                        setTimeout(function() {

                            $('#addedStory').append(deleteButton).css("width:auto");
                        }, 500);

                        deleteButton.on('click', '', function() {


                            $.ajax({
                                method: "POST",
                                url: "http://" + ip + "/api/delete_story",
                                headers: { Authorization: localStorage.TOKEN },
                                dataType: "json",
                                success: function(data) {

                                    $('#editStory').modal('toggle');
                                    $("#addedStory").empty();
                                }


                            });

                        });

                    }
                });

                $('#editStory').modal('toggle');


            });
        }
    });

    //MOVED: Story Requests down below in its function

	$('#form_password').validator().on('submit', function(event) {
		if (event.isDefaultPrevented()) {
			// handle the invalid form...
			} else {
			event.preventDefault();
			$.ajax({
				method: "POST",
				url: "http://" + ip + "/api/update",
				headers: { Authorization: localStorage.TOKEN },
				data: { password: $("#settings_password").val() },
				dataType: "json",
				success: function(data) {
					$("#settings_password").val("");
					$("#settings_password2").val("");
					$('#changePass').modal('hide');
				}
			});
		}
	});
	
	$('#form_deleteAccount').validator().on('submit', function(event) {
		if (event.isDefaultPrevented()) {
			// handle the invalid form...
			} else {
			event.preventDefault();
			$.ajax({
				method: "POST",
				url: "http://" + ip + "/api/delete_account",
				headers: { Authorization: localStorage.TOKEN },
				data: { email: localStorage.EMAIL },
				dataType: "json",
				success: function(data) {
					var alert = document.createElement("div");
					alert.innerHTML='<div class="alert alert-warning" role="alert"><strong>Warning!</strong> This account will be deleted. Please check your e-mail.</div>';
					document.getElementsByTagName('body')[0].append(alert);
					$('#deleteAccount').modal('hide');
				}
			});
		}
	});
	
	

}

function getProfile() {
	$.ajax({
        method: "GET",
        url: "http://" + ip + "/api/profile",
        headers: { Authorization: localStorage.TOKEN },
        dataType: "json",
        success: function(data) {
            $("#profile_name").text(data.name);
            $("#profile_nameStory").text(data.name);
            $("#settings_name").val(data.name);
            $("#profile_image").attr('src', imageEndpoint + data.avatar);
            $("#profile_imageStory").attr('src', imageEndpoint + data.avatar);

            var birthDate = data.birthday_date.split("-");
            $("#birthDay option:contains(" + birthDate[2] + ")").attr('selected', 'selected');
            $("#birthMonth option:contains(" + months[parseInt(birthDate[1]) - 1] + ")").attr('selected', 'selected');
            $("#birthYear option:contains(" + birthDate[0] + ")").attr('selected', 'selected');
            localStorage.CHAT_TOKEN = data.chat_token;
        }
    });
}

function getFriends() {
	$.ajax({
        method: "GET",
        url: "http://" + ip + "/api/friends",
        headers: { Authorization: localStorage.TOKEN },
        dataType: "json",
        success: function(data) {
            if (data.total > 0) {
                for (let i = 0; i < data.friends.length; i++) {
                    friends[data.friends[i].friendship_id] = new Friend(data.friends[i].name, data.friends[i].email, data.friends[i].online);
                    if (data.friends[i].avatar === undefined)
                        createFriend(socket, "http://placehold.it/50/FA6F57/fff&text=ME", data.friends[i].name, data.friends[i].friendship_id, "friends-list", data.friends[i].online);
                    else createFriend(socket, data.friends[i].avatar, data.friends[i].name, data.friends[i].friendship_id, "friends-list", data.friends[i].online);
                }

            }
        }
    });
}

function getFriendsRequests() {
	$.ajax({
        method: "GET",
        url: "http://" + ip + "/api/friend_requests",
        headers: { Authorization: localStorage.TOKEN },
        dataType: "json",
        success: function(data) {
            if (data.total > 0) {
                for (let i = 0; i < data.requests.length; i++) {
                    friendRequestsArray.push(new FriendReq(data.requests[i].name, data.requests[i].email, data.requests[i].friendship_id, data.requests[i].avatar));
                }
                updateFriendReq();
            }
        }
    });
}

function getStory() {
	$.ajax({
        method: "GET",
        url: "http://" + ip + "/api/story",
        headers: { Authorization: localStorage.TOKEN },
        dataType: "json",
        success: function(data) {
				if(data.text!=null || data.image!=null || data.feel!=null)
					{

						 $("#addedStory").empty();
						addElementsToStoryPanel(data,$('#addedStory'));

						var deleteButton = $('<div class="wrapper"><button type="button" class="btn btn-danger btn-lg" class="form-group">Delete story</button></div>');

						 setTimeout(function(){
							 
							$('#addedStory').append(deleteButton).css("width:auto");
						 },100);
						
						deleteButton.on('click', '', function() {


								 $.ajax({
            					method: "POST",
           						 url: "http://" + ip + "/api/delete_story",
           						 headers: { Authorization: localStorage.TOKEN },
           						 dataType: "json",
            					success: function(data) {

									
									$('#editStory').modal('toggle');
									 $("#addedStory").empty();
									}
							});

						});
					}

		}
	});
}

function refreshTokenRequest() {
    $.ajax({
        method: "GET",
        url: "http://" + ip + "/api/refresh_token",
        headers: { Authorization: localStorage.TOKEN },
        dataType: "json",
        success: function(data) {
            localStorage.TOKEN = data.access_token;

        }
    });

}

function sendMessage(socket) {
    let jsonObj;
    let jsonString;
    if (!(/^\s*$/.test($("#messageInputBox").val()))) {
        createMessage($("#messageInputBox").val(), "right"); //nu are al 3-lea param => undefined. E ok
        let currentDate = new Date();
		date = currentDate.today() + " " + currentDate.timeNow();
		if (currentFriend.length > 100) {
			
            jsonObj = { "random_token": currentFriend, "from": localStorage.EMAIL, "random": "1", "msg": $("#messageInputBox").val() };
            jsonString = JSON.stringify(jsonObj);
            socket.emit("msg user", jsonString);
            friends[currentFriend].messages.push(new Message($("#messageInputBox").val(), "right",date));
            $("#messageInputBox").val("");
            $(document.getElementById("random-list").getElementsByTagName("a")[0]).before($("#" + currentFriend));

        } else {
            jsonObj = { "to": friends[currentFriend].email, "from": localStorage.EMAIL, "msg": $("#messageInputBox").val() };
            jsonString = JSON.stringify(jsonObj);
            socket.emit("msg user", jsonString);
            friends[currentFriend].messages.push(new Message($("#messageInputBox").val(), "right",date));
            $("#messageInputBox").val("");
            $(document.getElementById("friends-list").getElementsByTagName("a")[0]).before($("#" + currentFriend));
        }
    }
}

function getAllMessagesRequest() {
    $.ajax({
        method: "GET",
        url: "http://" + ip + "/api/messages",
        headers: { Authorization: localStorage.TOKEN },
        dataType: "json",
        success: function(data) {
            if (data.total > 0) {
                for (let index = 0; index < data.conversations.length; index++) {
                    let friendshipID = findFriendshipIdByEmail(data.conversations[index].with);
                    for (let j = 0; j < data.conversations[index].messages.length; j++)
                        friends[friendshipID].messages.push(new Message(data.conversations[index].messages[j].message,
                            data.conversations[index].messages[j].sender,
                            data.conversations[index].messages[j].date));
                }
                $('[data-toggle="tooltip"]').tooltip();
            }
        }
    });
}


function convertAndResizeImage(inputFileId, width, height, callback) {

    if (document.getElementById(inputFileId).files.length > 0) {
        let file = document.getElementById(inputFileId).files[0];
        let img = document.createElement("img");
        let canvas = document.createElement('canvas');
        let reader = new FileReader();
        reader.onload = function() {
            //console.log('RESULT', reader.result);
            img.src = reader.result;
            //base64Image = reader.result;
            img.onload = function() {
                let ctx = canvas.getContext("2d");
                ctx.drawImage(img, 0, 0);
                canvas.width = width;
                canvas.height = height;
                ctx = canvas.getContext("2d");
                ctx.drawImage(img, 0, 0, width, height);
                //base64Image = canvas.toDataURL("image/png");
                //console.log(base64Image);
                let conv = canvas.toDataURL("image/png");
                //console.log(conv);
                //base64Image = conv;
                //console.log(base64Image);
                callback(conv);
            };
        };
        reader.readAsDataURL(file);
    } else callback(undefined);
}
