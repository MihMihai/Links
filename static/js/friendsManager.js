
	function FriendReq(name, email, friendship_id)
	{
	this.name = name;
	this.email = email;
	this.friendship_id=friendship_id;
	}

           function AddFriend(socket,chat_token,friendRequestsArray,panelContent) {
				
				while (panelContent!=null && panelContent.firstChild) {
						panelContent.removeChild(panelContent.firstChild);
					}
				
				
				var emailInput = document.createElement('div');
				emailInput.innerHTML='<input type="text" class="name_val" placeholder="Email of wanted friend">';
				panelContent.append(emailInput);
				
				var addButton= document.createElement('div');
				addButton.innerHTML='<button type="button" class="btn btn-primary">Add friend</button>';
				panelContent.append(addButton);
				
				
				$(addButton).on('click','', function() {

						var value = $('input.name_val').val();

						socket.emit("friend request",{"chat_token":chat_token,"email":value});

						socket.on("bad friend request",function(msg){

							alert(msg);

						});

				});
		   }

            function ViewFriendRequests(socket, chat_token,friendRequestsArray,panelContent){
				
				while (panelContent!=null && panelContent.firstChild) {
						panelContent.removeChild(panelContent.firstChild);
					}

				for(i=0;i<friendRequestsArray.length;i++)
				{
					createFriendRequestManager(friendRequestsArray[i].name,friendRequestsArray[i].email);
				}

				
				socket.on("new friend request",function(msg){
					try{
						alert("new friend request");
						let obj = JSON.parse(msg);
						let from = obj.from;
						let name = obj.name;

						friendRequestsArray.push(new Friend(name, from));
						createFriendRequestManager(name,from);
			
					}
				catch(e){
				console.log("ERROR");
					}
					
				
				});
			}
			function createFriendRequestManager(name,from)
			{
				var friendreq=document.createElement('div');
				friendreq.textContent=name;
				var acceptButton= document.createElement('span');
				acceptButton.innerHTML='<button type="button" class="btn btn-primary">Accept</button>';

				var declineButton= document.createElement('span');
				declineButton.innerHTML='<button type="button" class="btn btn-primary">Decline</button>';

				friendreq.append(acceptButton);
				friendreq.append(declineButton);
				panelContent.append(friendreq);


				$(acceptButton).on('click','', function() 
				{

					var answer = confirm ("Are you want to accept the friend request?")
					if (answer)
						{
							socket.emit("response friend request",{"chat_token":chat_token,"email":from, "status":1});

							//createFriend("http://placehold.it/50/FA6F57/fff&text=ME",name,friendship_id);

							panelContent.removeChild(friendreq);
							friendRequestsArray.splice(friendRequestsArray.indexOf(new Friend(name, from)),1);
						}

				});

				$(declineButton).on('click','', function() {

					var answer = confirm ("Are you want to decline the friend request?")
					if (answer)
						{
							socket.emit("response friend request",{"chat_token":chat_token,"email":from, "status":0});
							panelContent.removeChild(friendreq);
							friendRequestsArray.splice(friendRequestsArray.indexOf(new Friend(name, from)),1);
						}
					
				});

			}

			
			function Widgets(panelContent){
                var panelContent = document.getElementById("panelContent");
				while (panelContent!=null && panelContent.firstChild) {
						panelContent.removeChild(panelContent.firstChild);
					}
            };
			