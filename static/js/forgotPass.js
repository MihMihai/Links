  window.onload = function() {
      $('#form_forgot_pass').validator().on('submit', function(event) {
          if (event.isDefaultPrevented()) {
              // handle the invalid form...
          } else {
              event.preventDefault();
              $.ajax({
                  method: "POST",
                  url: "http://"+ip+"/api/forgot_password",
                  data: {
                      email: $("#forgot_email").val()
                  },
                  dataType: "json",
                  success: function(data) {
                      $('#response').text("An email has been sent to you!");
                      $("#forgot_email").val("");
                      console.log(data);
                  },
                  error: function(XMLHttpRequest, textStatus, errorThrown) {
                      $('#response').text("Try again! Maybe the email is not correct!");
                      $("#forgot_email").val("");
                  }
              });
          }
      });
  }
