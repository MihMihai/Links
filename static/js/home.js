var login_button;
var register_button;
var ip = "188.25.131.242";

window.onload = function() {
    $('.modal').on('hidden.bs.modal', function() {
        $(this).find('form')[0].reset();
    });
    //forgot-password button
    $("#forgot_pass").click(function() {
        window.location.replace("http://linkspeople.ddns.net/forgotpassword");
    });

    login();
    signup();
}

function login() {
    $('#form_login').validator().on('submit', function(event) {
        if (event.isDefaultPrevented()) {
            // handle the invalid form...
        } else {
            event.preventDefault();
            $.post("http://" + ip + "/api/login", { email: $("#login_email").val(), password: $("#login_password").val(), remember_me: $("#remember_me").is(":checked") }, function(data) {
                    localStorage.setItem("TOKEN", data["access_token"]);
                    localStorage.setItem("EMAIL", $("#login_email").val());

                    window.location.replace("http://linkspeople.ddns.net/chat");
                    //window.location.replace("file:///D:/documente/GitHub/Links/chat.html");
                }, "json")
                .fail(function() {
                    $("#login_error").html("<p style='color:red;'>Invalid email or password!</p>");
                });
        }
    });
}

function signup() {
    $('#form_register').validator().on('submit', function(event) {
        if (event.isDefaultPrevented()) {
            // handle the invalid form...
        } else {
            event.preventDefault();
            $.post("http://" + ip + "/api/signup", {
                    name: $("#register_name").val(),
                    email: $("#register_email").val(),
                    password: $("#register_password").val(),
                    birth_day: $("#birthDay").find(":selected").text(),
                    birth_month: $("#birthMonth").find(":selected").text(),
                    birth_year: $("#birthYear").find(":selected").text()
                }, function(data) {
                    console.log(data);
                    $('#register').modal('hide');
                }, "json")
                .fail(function() {
                    $("#register_mail_error").html("<p style='color:red;'>This email is already taken!</p>");
                });
        }
    });
}
