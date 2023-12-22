const overlay = document.getElementById('overlay');
const words = document.getElementById('words');

overlay.addEventListener('click', function off() {
    overlay.style.display = 'none';
    words.style.display= 'none';

    // Disable click event after first click
    overlay.removeEventListener('click', off);

});


const options = document.querySelectorAll('.option');
options.forEach(element => {
    element.addEventListener('click', function handleClick(event) {
        console.dir(event.currentTarget.classList)
        var buttonClicked = '';
        if (event.currentTarget.classList.contains('tenant')){
            buttonClicked = 'tenant';
        }else if(event.currentTarget.classList.contains('landlord')){
            buttonClicked = 'landlord';
        }else{
            buttonClicked = 'error'
        }
        fetch("/", {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ button: buttonClicked })
        })
        .then(response => {
            if (response.ok) {
                // Redirect to the "/login" page
                window.location.href = buttonClicked + '/login' ;
            } else {
                console.error('Failed to handle the response:', response);
            }
        })
        .catch(error => {
            console.error('Error during fetch:', error);
        });
    });
});

