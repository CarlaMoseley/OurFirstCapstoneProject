function openNav() {
    document.getElementById("sidenav").style.width = "350px";
    document.body.style.backgroundColor = "rgba(0,0,0,0.5)";
    darkenElements();
}

function closeNav() {
    document.getElementById("sidenav").style.width = "0";
    document.body.style.backgroundColor = "rgb(235, 235, 235)";
    resetElements();
}

function darkenElements() {
    const header = document.getElementById("header");
    const unitInformation = document.getElementById("Unit-Information");
    const suggestedTasks = document.getElementById("Suggested-Tasks");
    const makePaymentBox = document.getElementById("make_payment-box");
    if(header && makePaymentBox){
        header.style.filter = "brightness(70%)";
        makePaymentBox.style.filter = "brightness(70%)";
    }else if(header&&unitInformation&&suggestedTasks){
        header.style.filter = "brightness(70%)";
        unitInformation.style.filter = "brightness(70%)";
        suggestedTasks.style.filter = "brightness(70%)";
    }else if(header&&suggestedTasks){
        header.style.filter = "brightness(70%)";
        suggestedTasks.style.filter = "brightness(70%)";
    }else{
        header.style.filter = "brightness(70%)";
        unitInformation.style.filter = "brightness(70%)";
    }

}

function resetElements() {
    const header = document.getElementById("header");
    const unitInformation = document.getElementById("Unit-Information");
    const suggestedTasks = document.getElementById("Suggested-Tasks");
    const makePaymentBox = document.getElementById("make_payment-box");
    if(header && makePaymentBox){
        header.style.filter = "brightness(100%)";
        makePaymentBox.style.filter = "brightness(100%)";
    }else if(header&&unitInformation&&suggestedTasks){
        header.style.filter = "brightness(100%)";
        unitInformation.style.filter = "brightness(100%)";
        suggestedTasks.style.filter = "brightness(100%)";
    }else if(header&&suggestedTasks){
        header.style.filter = "brightness(100%)";
        suggestedTasks.style.filter = "brightness(100%)";
    }else{
        header.style.filter = "brightness(100%)";
        unitInformation.style.filter = "brightness(100%)";
    }

}


function toggleDropdown() {
    var dropdown = document.getElementById("suggestedTasksDropdown");
    dropdown.style.display = (dropdown.style.display === "block") ? "none" : "block";
}

// Get the modal
var modal = document.getElementById("User-Pop-up");

// When the user clicks on the button, open the modal
function showProfile() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
function closeModal(){
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


document.addEventListener('DOMContentLoaded', function() {
    const backgroundElement = document.getElementById('header');

    function setBackgroundImage() {
        const path = window.location.pathname.split('/');
        const trimmedPath = path[1].trim().toLowerCase();
        console.log(trimmedPath)
    
        if (trimmedPath === 'tenant') {
            backgroundElement.style.backgroundImage = 'url("/static/images/tenants-profile.jpg")';
        } else if (trimmedPath === 'landlord') {
            backgroundElement.style.backgroundImage = 'url("/static/images/landlord-profile.jpg")';
        } else {
            console.log('image not found')
            return;
        }
    }


    setBackgroundImage();
});
