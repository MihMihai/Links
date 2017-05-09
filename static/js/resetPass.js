  window.onload = function() {
      let url = window.location.href;

      $('#form_change_pass').validator().on('submit', function(event) {
          if (event.isDefaultPrevented()) {
              // handle the invalid form...
          } else {
              event.preventDefault();
              $.ajax({
                  method: "POST",
                  url: "http://86.121.87.213/api/reset_password",
                  headers: {
                      resetToken: url.substring(45, url.length);
                  }
                  data: {
                      password: $("#forgot_password").val()
                  },
                  dataType: "json",
                  success: function(data) {
                      window.location.replace("http://linkspeople.ddns.net");
                  }
              });
          }
      });
  }
