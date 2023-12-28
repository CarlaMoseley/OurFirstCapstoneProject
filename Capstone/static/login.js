//const back = document.getElementById('Back'); // Add 'const' here
//back.addEventListener('click', function goBack() {
//    window.location = '/';
//})
const signup = document.getElementById('signup');
signup.addEventListener('click', function signup() {
    const path = window.location.pathname.split('/');
    if (path[1] === 'tenant') {
        window.location = '/tenant/signup';
    } else if (path[1] === 'landlord') {
        window.location = '/landlord/signup';
    } else {
        console.log('error');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Get the background element (assuming it has an ID of 'background')
    const backgroundElement = document.body;

    // Function to extract the background image URL based on the URL parameters
    function setBackgroundImage() {
        const path = window.location.pathname.split('/');
        const trimmedPath = path[1].trim().toLowerCase(); // Trim and convert to lowercase
    
        console.log(trimmedPath);
    
        if (trimmedPath === 'tenant') {
            backgroundElement.style.backgroundImage= 'url("/static/images/tenants-start.jpg")';
        } else if (trimmedPath === 'landlord') {
            backgroundElement.style.backgroundImage= 'url("/static/images/landlord-login.jpg")';
        } else {
            // Default background image if the URL doesn't match any criteria
            return;
        }
    }

    // Call the function initially to set the background based on the current URL
    setBackgroundImage();

    // Optionally, you can also update the background image when the URL changes
    window.addEventListener('popstate', setBackgroundImage);
});

