window.onload=function(){

            $("#addFriend").click(function() {
				
				var panelContent = document.getElementById("panelContent");
				while (panelContent.firstChild) {
						panelContent.removeChild(panelContent.firstChild);
					}
				
				
				var emailInput = document.createElement('div');
				emailInput.innerHTML='<input type="text" placeholder="Email of wanted friend">';
				panelContent.append(emailInput);
				
				var addButton= document.createElement('div');
				addButton.innerHTML='<button type="button" class="btn btn-primary">Add friend</button>';
				panelContent.append(addButton);
				
				
				$(addButton).on('click', '', function() {
						//add - trimis cerere de prietenie
						
				});
			});   

            $("#friendRequests").click(function(){
				
				var panelContent = document.getElementById("panelContent");
				while (panelContent.firstChild) {
						panelContent.removeChild(panelContent.firstChild);
					}
					
				
                
            });
			
			$("#widgets").click(function(){
                var panelContent = document.getElementById("panelContent");
				while (panelContent.firstChild) {
						panelContent.removeChild(panelContent.firstChild);
					}
            });
			
}
