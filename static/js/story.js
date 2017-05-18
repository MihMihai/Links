function showStory(friendshipId, panelToAttach){
    
     if(friendshipId!=null)
	  {
		  $.ajax({
        method: "GET",
        url: "http://" + ip + "/api/story",
        headers: { Authorization: localStorage.TOKEN },
        data : {"friendship_id": friendshipId},
        dataType: "json",
        success: function(data) {
				
                addElementsToStoryPanel(data,panelToAttach);
			}
		});
	  }
	  else {
		   $.ajax({
        method: "GET",
        url: "http://" + ip + "/api/story",
        headers: { Authorization: localStorage.TOKEN },
        dataType: "json",
        success: function(data) {
                addElementsToStoryPanel(data,panelToAttach);
			}
		});
	  }
    
}

function addElementsToStoryPanel(data,panelToAttach) {
	
	var status = data.text;
	var feel = data.feel;
	var imageSrc = data.image;
	var date = data.date;
	
	var container = $('<div id="container" style="min-height: 55vh; display: flex; align-items: center; justify-content: center; flex-direction: column;"></div>');
	if(imageSrc !== undefined && imageSrc !==null)
	{   
	   var imgStory = $('<img />', {
		src: "http://linkspeople.ddns.net/stories/" + imageSrc, 
		height: 500,
		weight: 500,
		alt: ''
		});
		container.append(imgStory);
	}
	var writing="";
	
	if(status!=undefined) writing = writing + status;
    if(feel!== undefined) writing = writing + "- feeling " + feel;
	if((imageSrc == undefined || imageSrc == null) && (status == undefined || status == null) && (feel == undefined || feel == null))
			writing = "No story available";

	container.append(writing).css("font-family","'Impact', 'Charcoal', sans-serif").css("font-size","30px");

	panelToAttach.append(container);
}
