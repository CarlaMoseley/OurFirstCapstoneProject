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
    function getBackgroundImageURL() {
        const path = window.location.pathname.split('/');
        const trimmedPath = path[1].trim().toLowerCase(); // Trim and convert to lowercase
    
        console.log(trimmedPath);
    
        if (trimmedPath === 'tenant') {
            return 'url("https://cdngeneral.rentcafe.com/dmslivecafe/3/552097/the-case-building-apartment-building-exterior-view-during-sunset.jpg?crop=(0,0,300,200)&cropxunits=300&cropyunits=200&quality=85&")';
        } else if (trimmedPath === 'landlord') {
            return "url('https://images.squarespace-cdn.com/content/v1/60b66dcb82316305ed02d003/83ec98c4-c441-4e72-b52d-5a56389e1978/mike-koshet-commercial-real-estate-17.jpg')";
        } else {
            // Default background image if the URL doesn't match any criteria
            return '';
        }
    }

    // Function to set the background image based on the URL
    function setBackgroundImage() {
        const imageURL = getBackgroundImageURL();
        backgroundElement.style.backgroundImage = imageURL;
    }

    // Call the function initially to set the background based on the current URL
    setBackgroundImage();

    // Optionally, you can also update the background image when the URL changes
    window.addEventListener('popstate', setBackgroundImage);
});

