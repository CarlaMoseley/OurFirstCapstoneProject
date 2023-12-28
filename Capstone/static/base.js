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
    header.style.filter = "brightness(70%)";

    const unitInformation = document.getElementById("Unit-Information");
    unitInformation.style.filter = "brightness(70%)";

    const suggestedTasks = document.getElementById("Suggested-Tasks");
    suggestedTasks.style.filter = "brightness(70%)";

    // Add similar adjustments for other elements as needed
}

function resetElements() {
    const header = document.getElementById("header");
    header.style.filter = "brightness(100%)";

    const unitInformation = document.getElementById("Unit-Information");
    unitInformation.style.filter = "brightness(100%)";

    const suggestedTasks = document.getElementById("Suggested-Tasks");
    suggestedTasks.style.filter = "brightness(100%)";

    // Add similar adjustments for other elements as needed
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

    function getBackgroundImageURL() {
        const path = window.location.pathname.split('/');
        const trimmedPath = path[1].trim().toLowerCase();
        console.log(trimmedPath)
    
        if (trimmedPath === 'tenant') {
            return 'url("https://i.pinimg.com/originals/73/76/3a/73763a5abaefd12121f77b561b31267d.jpg")';
        } else if (trimmedPath === 'landlord') {
            console.log('read the image')
            return "url('https://i.pinimg.com/originals/e4/de/11/e4de11b369c2dc834df6fa49df8cb85e.jpg')";
        } else {
            console.log('image not found')
            return '';
        }
    }

    function setBackgroundImage() {
        console.log('inBackgroundImage')
        const imageURL = getBackgroundImageURL();
        backgroundElement.style.backgroundImage = imageURL;
    }

    setBackgroundImage();

    window.addEventListener('popstate', setBackgroundImage);
});