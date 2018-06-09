function login() {
    let username = $('#username').val();
    let password = $('#password').val();

    if (username === "" || password === "") {
        $('#incorrect_login').html('Username and password must not be empty');
        $('#incorrect_login').show();
    } else {
        let userData = {
            username: $('#username').val(),
            password: $('#password').val()
        };
        $.post('/airlinemanager/ajax/login/', userData, function() {
            console.log("success")
            localStorage.setItem('user', JSON.stringify(userData));
            window.history.back();
        }).fail(function(res) {
            console.log(res);
            $('#incorrect_login').html('Incorrect username or password');
            $('#incorrect_login').show();
        });
    }

}

$().ready(function() {
    $('#incorrect_login').hide();

});