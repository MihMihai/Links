
	function FriendReq(name, email, friendship_id)
	{
	this.name = name;
	this.email = email;
	this.friendship_id=friendship_id;
	}

           function AddFriend(socket,chat_token,friendRequestsArray,panelContent) {
			   
				$(currentTab).removeClass('active');
				$(currentTab + ">a").css("color","white");
				$('#addFriend').addClass('active');
				$('#addFriend>a').css("color","black");
				currentTab = '#addFriend';
				
				while (panelContent!=null && panelContent.firstChild) {
						panelContent.removeChild(panelContent.firstChild);
					}
				
				var container = $('<div id="container" style="min-height: 55vh; display: flex; align-items: center; justify-content: center; flex-direction: column;"></div>');
				
				var emailInput = $('<input id="emailValue" type="text" placeholder="Email of wanted friend">');
				
				$(emailInput).addClass("col-xs-12")
							.addClass("form-control")
							.css("margin-bottom","30px");
				var addButton= $('<button type="button" class="btn btn-success">Add friend</button>');
				

				container.append(emailInput);
				container.append($("<br>"));
				container.append(addButton);
				$(panelContent).append(container);

				
				addButton.on('click','', function() {
						var value = $('#emailValue').val();
						socket.emit("friend request",{"chat_token":chat_token,"email":value});
				});
		   }

            function ViewFriendRequests(socket, chat_token,friendRequestsArray,panelContent){
				
				$(currentTab).removeClass('active');
				$(currentTab + ">a").css("color","white");
				$('#friendRequests').addClass('active');
				$('#friendRequests>a').css("color","black");
				currentTab = '#friendRequests';
				
				
				while (panelContent!=null && panelContent.firstChild) {
						panelContent.removeChild(panelContent.firstChild);
					}

				for(i=0;i<friendRequestsArray.length;i++)
				{
					createFriendRequestManager(friendRequestsArray[i].name,friendRequestsArray[i].email);
				}

				
				
			}
			
			function createFriendRequest(imgSrc,name,friendshipId){
				var h6 = $("<h4></h4>").text(name);
				var friendreq = $("<a id="+friendshipId+" href='#'' class='list-group-item'></a>");
				friendreq.css("display","flex")
						.css("flex-direction","row")
						.css("align-items","center")
						.css("position","relative");
				let notificationMessage = $("<span class='glyphicon glyphicon-envelope messageNotification'></span>");

				h6.css("display","inline-block")
					.css("margin-left","10px");
				friendreq.append(h6);
				friendreq.append(notificationMessage);

				var containerForButtons = $('<div></div>');

				var acceptButton= $('<button id=btna' + friendshipId + ' type="button" class="btn btn-success">Accept</button>');
				acceptButton.css("margin-right","20px");

				var declineButton= $('<button id=btnd' + friendshipId + ' type="button" class="btn btn-danger">Decline</button>');
				
				containerForButtons.append(acceptButton)
									.append(declineButton)
									.css("position","absolute")
									.css("right","10px")
									.css("top","25%"); //odd i know :|

				friendreq.append(containerForButtons);
				$(panelContent).append(friendreq);
			}
			
			function createFriendRequestManager(name,from,friendship_id)
			{
				
				createFriendRequest("http://placehold.it/50/FA6F57/fff&text=ME",name,friendship_id);

				$('#btna' + friendship_id).on('click','', function() 
				{

					var answer = confirm ("Are you want to accept the friend request?")
					if (answer)
					{
						socket.emit("response friend request",{"chat_token":chat_token,"email":from, "status":1});

						createFriend("http://placehold.it/50/FA6F57/fff&text=ME",name,friendship_id);

						$("#" + friendship_id).remove();
						//panelContent.removeChild(friendreq);
						//friendRequestsArray.splice(friendRequestsArray.indexOf(new Friend(name, from)),1);
						let posOfNewFriend = friendRequestsArray.map(friend => friend.email).indexOf(from);
						friendRequestsArray.splice(posOfNewFriend,1);
						friends[friendship_id] = new Friend(name,from);
					}

				});

				$('#btnd' + friendship_id).on('click','', function() {

					var answer = confirm ("Are you want to decline the friend request?")
					if (answer)
					{
						socket.emit("response friend request",{"chat_token":chat_token,"email":from, "status":0});
						$("#" + friendship_id).remove();
						//panelContent.removeChild(friendreq);
						let posOfDeletedFriendReq = friendRequestsArray.map(friend => friend.email).indexOf(from);
						friendRequestsArray.splice(posOfDeletedFriendReq,1);
						//friendRequestsArray.splice(friendRequestsArray.indexOf(new Friend(name, from)),1);
					}
					
				});

			}

			
			function Widgets(panelContent){
				
				$(currentTab).removeClass('active');
				$(currentTab + ">a").css("color","white");
				$('#widgets').addClass('active');
				$('#widgets>a').css("color","black");
				currentTab = '#widgets';
				
				
                var panelContent = document.getElementById("panelContent");
				while (panelContent!=null && panelContent.firstChild) {
						panelContent.removeChild(panelContent.firstChild);
					}
            };
			