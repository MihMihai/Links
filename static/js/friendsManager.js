function FriendReq(name, email, friendship_id, avatar) {
    this.name = name;
    this.email = email;
    this.friendship_id = friendship_id;
    this.avatar = avatar;
}
function Location(latitude, longitude){
    this.latitude=latitude;
    this.longitude=longitude;
}

function AddFriend(socket, friendRequestsArray, panelContent) {

    $(currentTab).removeClass('active');
    $(currentTab + ">a").css("color", "white");
    //.css("background-color","#2C3E50");
    $('#addFriend').addClass('active');
    $('#addFriend>a').css("color", "black");
    currentTab = '#addFriend';

    while (panelContent != null && panelContent.firstChild) {
        panelContent.removeChild(panelContent.firstChild);
    }

    var container = $('<div id="container" style="min-height: 55vh; display: flex; align-items: center; justify-content: center; flex-direction: column;"></div>');

    var emailInput = $('<input id="emailValue" type="text" placeholder="Email of wanted friend">');

    $(emailInput).addClass("col-xs-12")
        .addClass("form-control")
        .css("margin-bottom", "30px");
    var addButton = $('<button type="button" class="btn btn-success btn-lg">Add friend</button>');


    container.append(emailInput);
    container.append($("<br>"));
    container.append(addButton);
    $(panelContent).append(container);


    addButton.on('click', '', function() {
        var value = $('#emailValue').val();
        socket.emit("friend request", {
            "chat_token": localStorage.CHAT_TOKEN,
            "email": value
        });

        socket.on("bad friend request",function(msg){

            alert(msg);
        });
	


    });
}

function ViewFriendRequests(socket, friendRequestsArray, panelContent) {

    $(currentTab).removeClass('active');
    $(currentTab + ">a").css("color", "white");
    //.css("background-color","#2C3E50");
    $('#friendRequests').addClass('active');
    $('#friendRequests>a').css("color", "black");
    currentTab = '#friendRequests';


    while (panelContent != null && panelContent.firstChild) {
        panelContent.removeChild(panelContent.firstChild);
    }

    for (i = 0; i < friendRequestsArray.length; i++) {
        createFriendRequestManager(socket, friendRequestsArray[i].name, friendRequestsArray[i].email, friendRequestsArray[i].friendship_id,friendRequestsArray[i].avatar);
    }



}

function createFriendRequest(imgSrc, name, friendshipId) {
    var h6 = $("<h4></h4>").text(name);
    var friendreq = $("<a id=fr" + friendshipId + " href='#'' class='list-group-item'></a>");
    friendreq.css("display", "flex")
        .css("flex-direction", "row")
        .css("align-items", "center")
        .css("position", "relative");
    let notificationMessage = $("<span class='glyphicon glyphicon-envelope messageNotification'></span>");

    h6.css("display", "inline-block")
        .css("margin-left", "10px");
    friendreq.append(h6);
    friendreq.append(notificationMessage);

    var containerForButtons = $('<div></div>');

    var acceptButton = $('<button id=btna' + friendshipId + ' type="button" class="btn btn-success">Accept</button>');
    acceptButton.css("margin-right", "20px");

    var declineButton = $('<button id=btnd' + friendshipId + ' type="button" class="btn btn-danger">Decline</button>');

    containerForButtons.append(acceptButton)
        .append(declineButton)
        .css("position", "absolute")
        .css("right", "10px")
        .css("top", "25%");

    friendreq.append(containerForButtons);
    $(panelContent).append(friendreq);
}

function createFriendRequestManager(socket, name, from, friendship_id, avatar) {

    createFriendRequest(avatar, name, friendship_id);

    $('#btna' + friendship_id).on('click', '', function() {

        var answer = confirm("Are you want to accept the friend request?")
        if (answer) {
            socket.emit("response friend request", {
                "chat_token": localStorage.CHAT_TOKEN,
                "email": from,
                "status": 1
            });

            createFriend(socket, avatar, name, friendship_id);

            $("#fr" + friendship_id).remove();
            //panelContent.removeChild(friendreq);
            //friendRequestsArray.splice(friendRequestsArray.indexOf(new Friend(name, from)),1);
            let posOfNewFriend = friendRequestsArray.map(friend => friend.email).indexOf(from);
            friendRequestsArray.splice(posOfNewFriend, 1);
            friends[friendship_id] = new Friend(name, from);
        }

    });

    $('#btnd' + friendship_id).on('click', '', function() {

        var answer = confirm("Are you want to decline the friend request?")
        if (answer) {
            socket.emit("response friend request", {
                "chat_token": localStorage.CHAT_TOKEN,
                "email": from,
                "status": 0
            });
            $("#fr" + friendship_id).remove();
            //panelContent.removeChild(friendreq);
            let posOfDeletedFriendReq = friendRequestsArray.map(friend => friend.email).indexOf(from);
            friendRequestsArray.splice(posOfDeletedFriendReq, 1);
            //friendRequestsArray.splice(friendRequestsArray.indexOf(new Friend(name, from)),1);
        }

    });

}


  
var right = false; 
var lastWeather = null;

function Widgets(panelContent) {




    $(currentTab).removeClass('active');
    $(currentTab + ">a").css("color", "white");
    //.css("background-color","#2C3E50");
    $('#widgets').addClass('active');
    $('#widgets>a').css("color", "black");
    currentTab = '#widgets';

    while (panelContent != null && panelContent.firstChild) {
        panelContent.removeChild(panelContent.firstChild);
    }
   

    
    var container = $('<div id="container" style="min-height: 20vh; display: flex; align-items: center; justify-content: center; flex-direction: column;"></div>');

    var locationInput = $('<input id="locationValue" type="text" placeholder="Desired location for showing weather">');
    var errorRed = $('<div id="weather_error" class="help-block with-errors"></div>');
    $(locationInput).addClass("col-xs-12").addClass("form-control");
    var searchButton = $('<button type="button" class="btn btn-success btn-lg">Search</button>');


    container.append(locationInput);
    container.append($("<br>"));
    container.append(errorRed);
    container.append(searchButton);
    container.append($("<br>"));
    $(panelContent).append(container);


     if(lastWeather!=null) panelContent.append(lastWeather);

     searchButton.on('click', '', function() {



        var val = document.getElementById("locationValue").value;

        document.getElementById("locationValue").value = "";

        returnWeatherLocation(val);

        var $this = $(this);
        var clickCount = ($this.data("click-count")||0) + 1;
         $this.data("click-count", clickCount);
        
        if (clickCount > 1 && right === true) {
            panelContent.removeChild(panelContent.lastChild);
        }

       
       
     });
     function getLocation() 
    {
    if (navigator.geolocation)
         navigator.geolocation.getCurrentPosition(showPosition);
    }

    function showPosition(position) 
    {
         
         returnWeatherLatLong(position.coords.latitude,position.coords.longitude);
       
    }

    function returnWeatherLatLong (lat, long)
    {
         $.ajax({
	        method: "GET",
	        url: "http://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&mode=html&APPID=ac3ba0c132415bb20cef3bc050715601",
	        success: function(data)
            {
                $("#weather_error").html("");
                right = true;
                var container = $('<div id="container" style="min-height: 20vh; display: flex; align-items: center; justify-content: center; flex-direction: column;"></div>');
                var weather = document.createElement('div');
                $(weather).appendTo(panelContent).html(data).css("font-size","x-large");
                lastWeather=weather;
        
            },
            error: function(){

                     right = false;
					$("#weather_error").html("<p style='color:red;'>Please insert a valid city! </p>");
            }
        });
    }
    function returnWeatherLocation(city)
    {
         $.ajax({
	        method: "GET",
	        url: "http://api.openweathermap.org/data/2.5/weather?q="+city+"&mode=html&APPID=ac3ba0c132415bb20cef3bc050715601",
	        success: function(data)
            {
                $("#weather_error").html("");
                 right = true;
                var container = $('<div id="container" style="min-height: 20vh; display: flex; align-items: center; justify-content: center; flex-direction: column;"></div>');
                var weather = document.createElement('div');
                $(weather).appendTo(panelContent).html(data).css("font-size","x-large");
                lastWeather=weather;
            },
            error: function(){
                     right = false;
					$("#weather_error").html("<p style='color:red;'>Please insert a valid city! </p>");
            }
        });
    }

   
        
    }
