function showStory(friendshipId){
    
     $.ajax({
        method: "GET",
        url: "http://" + ip + "/api/story",
        headers: { Authorization: localStorage.TOKEN },
        data : friendshipId,
        dataType: "json",
        success: function(data) {
            
               
                var status = data.text;
                var feel = data.feel;
                var imageSrc = data.image;
                var date = data.date;
                
                var container = $('<div id="container" style="min-height: 55vh; display: flex; align-items: center; justify-content: center; flex-direction: column;"></div>');
	            if(imageSrc !== undefined && imageSrc !==null)
                {   
                   /* var imgStory = $('<img />', {
		            src: "http://linkspeople.ddns.net/image/" + imageSrc, 
                    height: 100,
                    weight: 100,
		            alt: ''
	                });

                    container.append(imgStory);*/
                }
                
                if(feel!== undefined) container.append(status + "- feeling " + feel);
                else  container.append(status);

                $("#storyPost").append(container);
                

			}
	});
    
}