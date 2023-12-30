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

// Your existing event listeners
document.getElementById('login').addEventListener('click', function returnToLogin(e) {
    const path = window.location.pathname;
    if (path.includes('landlord')) {
        window.location = '/landlord/login';
    } else if (path.includes('tenant')) {
        window.location = '/tenant/login';
    } else {
        console.error('Wrong URL PATH or value entered');
    }
});

document.getElementById('password').addEventListener('input', checkPasswordMatch);
document.getElementById('confirmpassword').addEventListener('input', checkPasswordMatch);


document.addEventListener('DOMContentLoaded', function() {
    // Get the background element (assuming it has an ID of 'background')
    const backgroundElement = document.body;
    const container = document.querySelector('.container');

    // Function to extract the background image URL based on the URL parameters
    function setBackgroundImage() {
        const path = window.location.pathname.split('/');
        const trimmedPath = path[1].trim().toLowerCase(); // Trim and convert to lowercase
    
        console.log(trimmedPath);
    
        if (trimmedPath === 'tenant') {
            container.style.margin = "0";
            backgroundElement.style.backgroundImage = 'url("/static/images/tenant_backscript.jpg")';
        } else if (trimmedPath === 'landlord') {
            container.style.margin = "0 0 0 auto";
            backgroundElement.style.backgroundImage = 'url("/static/images/landlord_backscript.jpg")';
        } else {
            // Default background image if the URL doesn't match any criteria
            return '';
        }
    }

    // Call the function initially to set the background based on the current URL
    setBackgroundImage();

    // Optionally, you can also update the background image when the URL changes
    window.addEventListener('popstate', setBackgroundImage);

});
