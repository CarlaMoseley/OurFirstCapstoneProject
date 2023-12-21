document.getElementById('password').addEventListener('input', checkPasswordMatch);
document.getElementById('confirmpassword').addEventListener('input', checkPasswordMatch);

function checkPasswordMatch() {
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmpassword').value;
    var checkmarkElement = document.getElementById('passwordMatch');

    if (password === confirmPassword) {
        checkmarkElement.innerHTML = '&#10004;'; // Display checkmark
        checkmarkElement.style.color = 'green'; // Set color to green
    } else {
        checkmarkElement.innerHTML = '&#10006;'; // Display "X"
        checkmarkElement.style.color = 'red'; // Set color to red
    }
}

document.getElementById('menu').addEventListener('click', function goBack() {
    window.location = '/';
});

document.getElementById('login').addEventListener('click', function returnToLogin(e) {
    const path = window.location.pathname;
    if (path.includes('landlord')) {
        window.location = '/login/landlord';
    } else if (path.includes('tenant')) {
        window.location = '/login/tenant';
    } else {
        console.error('Wrong URL PATH or value entered');
    }
});
