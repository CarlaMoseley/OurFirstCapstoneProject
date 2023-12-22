document.getElementById('login').addEventListener('click', function returnToLogin(e){
        const path = window.location.pathname;
        if(path.includes('landlord')){
            window.location = '/landlord/login';
        }else if(path.includes('tenant')){
            window.location='/tenant/login';
        }else{
            console.error('Wrong URL PATH or value entered');
        }
})
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
document.addEventListener('DOMContentLoaded', function() {
    // Get the background element (assuming it has an ID of 'background')
    const backgroundElement = document.body;
    const container = document.querySelector('.container');

    // Function to extract the background image URL based on the URL parameters
    function getBackgroundImageURL() {
        const path = window.location.pathname.split('/');
        const trimmedPath = path[1].trim().toLowerCase(); // Trim and convert to lowercase
    
        console.log(trimmedPath);
    
        if (trimmedPath === 'tenant') {
            container.style.margin = "0";
            return 'url("https://static01.nyt.com/images/2018/05/22/nyregion/22Housing-know1/merlin_138308601_7e723471-0113-4494-b301-062c5300d14a-superJumbo.jpg")';
        } else if (trimmedPath === 'landlord') {
            container.style.margin = "0 0 0 auto";
            return "url('https://cdn.viewing.nyc/assets/media/f94f15ddc02b1e30fbe6a182af19f00b/elements/0d94751f5ede2ddf294569d55fcb75cb/xl/cdd90369-3b66-48d0-8a20-c2d3b74d568b_2x.jpg')";
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
