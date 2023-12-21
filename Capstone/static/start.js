const options = document.querySelectorAll('.option');
options.forEach(element => {
    element.addEventListener('click', function handleClick(event) {
        const buttonClicked = event.target.id;
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

        // Set background color to yellow
        element.setAttribute('style', 'background-color: yellow;');
    });
});
