function showStory(friendshipId, panelToAttach){
    
     $.ajax({
        method: "GET",
        url: "http://" + ip + "/api/story",
        headers: { Authorization: localStorage.TOKEN },
        data : {"friendship_id": friendshipId},
        dataType: "json",
        success: function(data) {
            
              
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
                var writing=null;
                
                if(feel!== undefined && status!=undefined) writing = status + "- feeling " + feel;
                else  if(status!=undefined) writing = status;
                else if(feel!== undefined) writing = feel;

                container.append(writing).css("font-family","'Impact', 'Charcoal', sans-serif").css("font-size","30px");

                panelToAttach.append(container);
                
                

			}
	});
    
}
