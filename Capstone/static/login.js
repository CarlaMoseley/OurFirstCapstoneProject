let loginButton = document.getElementById("login");

let logintask = function () {
    var inputUserName = document.getElementById("username").value;
    var inputPassword = document.getElementById("password").value;
    fetch('static/login.txt')
        .then(response => {
            if (!response.ok) {
                alert('Error');
            }
            return response.text();
        })
        .then(data => {
            var lines = data.split('\n');

            for (var i = 0; i < lines.length; i++) {
                var parts = lines[i].split(',');
                var usernameFromFile = parts[0];
                var passwordFromFile = parts[1];

                if (inputUserName === usernameFromFile && inputPassword === passwordFromFile) {
                    window.location.href = 'index';
                    return;
                }
                else (
                    alert("Incorrect Username or password")
                )
            }
        })
        .catch(error => {
            console.error('Error reading file or network error:', error);
        });
};
loginButton.addEventListener("click", logintask);