window.onunload = function(){};
$().ready(function() {
    let serializedUserData = localStorage.getItem('user');
    if (serializedUserData == null) {
        $('#logout-button').hide();
    } else {
        $('#login-button').hide();
    }

});

function logout() {
    localStorage.removeItem("user");
    $('#logout-button').hide();
    $('#login-button').show();
}